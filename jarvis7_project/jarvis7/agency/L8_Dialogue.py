import asyncio
import json
from openai import AsyncOpenAI
from ..cortex.memory_os import ContextKernel
from ..agency.L4_Action import ToolRegistry
from ..agency.L6_StyleMatrix import StyleMatrix
from ..agency.L7_TraceLog import TraceLogger
from ..agency.L7_SleepCycle import SleepCycleManager
from ..world_model.state import WorldModel
from ..goals.manager import GoalManager
from ..actuators.file_ops import FileActuator

class DialogueEngine:
    def __init__(self, state):
        self.state = state
        self.client = AsyncOpenAI()
        self.kernel = ContextKernel(state)
        self.tools = ToolRegistry(state, self.kernel)
        self.styles = StyleMatrix()
        self.tracer = TraceLogger()
        self.sleep_manager = SleepCycleManager()
        
        # Body
        self.world_model = WorldModel()
        self.goals = GoalManager()
        self.actuators = FileActuator()
        
        # Register Body Tools (Type Hints enable schema generation)
        self.tools.register("act_write_file", self.actuators.write_file, "Write file content.")
        self.tools.register("goal_add", self.goals.add_goal, "Add goal.")
        self.tools.register("goal_list", lambda: self.goals.render(), "List goals.")

    async def chat_async(self, text):
        self.tracer.start_episode()
        self.state.gwt.add_stimulus("user", text)
        self.state.update(0.5)
        self.kernel.add_interaction("user", text)
        asyncio.create_task(self.kernel.graph.extract_and_store(text))

        boot = f"""
        IDENTITY: Jarvis 7.5
        STATE: {self.state.gauges}
        {self.world_model.render()}
        {self.goals.render()}
        KNOWLEDGE: {self.kernel.graph.get_context(text)}
        GWT: {self.state.gwt.get_context()}
        STYLE: {self.styles.resolve(self.state.gauges).get('system_injection','')}
        """
        self.kernel.set_boot_sequence(boot)
        msgs = self.kernel.render()

        try:
            res = await self.client.chat.completions.create(model="gpt-4o", messages=msgs, tools=self.tools.definitions, tool_choice="auto")
            msg = res.choices[0].message
            if msg.tool_calls:
                self.kernel.add_interaction("assistant", str(msg.tool_calls))
                msgs.append(msg)
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    out = self.tools.execute(tc.function.name, **args)
                    self.tracer.log_tool_usage(tc.function.name, args, out)
                    msgs.append({"role":"tool","tool_call_id":tc.id,"name":tc.function.name,"content":out})
                    self.kernel.add_interaction("function", f"Result {tc.function.name}: {out}")
                    self.sleep_manager.governance.update_metrics(tc.function.name, "Error" not in out)
                
                res = await self.client.chat.completions.create(model="gpt-4o", messages=msgs)
                reply = res.choices[0].message.content
            else:
                reply = msg.content
        except Exception as e:
            reply = f"Error: {e}"

        self.kernel.add_interaction("assistant", reply)
        self.tracer.end_episode(text, reply)
        
        if self.state.gauges.get("Axis_3_Urgency", 1.0) < 0.15:
            new = await asyncio.to_thread(self.sleep_manager.consolidate)
            if new > 0:
                self.tools.load_learned_skills()
            
        return {"response": reply, "gauges": self.state.gauges}
