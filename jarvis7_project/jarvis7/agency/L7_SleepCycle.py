import os
import json
import hashlib
import tempfile
import docker
from openai import OpenAI
from .L7_SkillGovernance import SkillGovernance

class SleepCycleManager:
    def __init__(self, skill_dir="./learned_skills", log="L7_trace_history.json"):
        self.skill_dir = skill_dir
        self.log = os.path.abspath(log)
        self.client = OpenAI()
        self.docker = docker.from_env()
        self.governance = SkillGovernance(skill_dir)

    def consolidate(self):
        print("💤 SLEEP CYCLE START")
        if not os.path.exists(self.skill_dir): os.makedirs(self.skill_dir)
        if not os.path.exists(self.log): return 0
        try:
            with open(self.log, 'r') as f: logs = [json.loads(line) for line in f if line.strip()]
            patterns = self._analyze(logs)
            count = 0
            for p in patterns:
                if any(p['id'] in f for f in os.listdir(self.skill_dir)): continue
                code = self._dream(p)
                if code and self._sandbox(code):
                    self.governance.register_skill(p['intent'], f"skill_{p['id']}.py", code, p)
                    print(f"✨ SKILL ACQUIRED: skill_{p['id']}.py")
                    count += 1
            return count
        except: return 0

    def _analyze(self, logs):
        chains = {}
        for l in logs:
            tools = [t['tool'] for t in l['tool_chain'] if t['status'] == 'success']
            if not tools: continue
            sig = "|".join(tools)
            if sig not in chains: chains[sig] = {'count':0, 'ex':[]}
            chains[sig]['count'] += 1
            chains[sig]['ex'].append(l['user_query'])
        return [{"id":hashlib.md5(k.encode()).hexdigest()[:6], "intent":f"auto_{k.replace('|','_')}", "steps":k.split("|"), "examples":v['ex'][:3]} for k,v in chains.items() if v['count']>=2]

    def _dream(self, p):
        prompt = f"Write Python function 'execute' for tool chain: {p['steps']}. Contexts: {p['examples']}. Define specific typed args (NO **kwargs). Output code only."
        try:
            res = self.client.chat.completions.create(model="gpt-4o", messages=[{"role":"system","content":prompt}])
            return res.choices[0].message.content.replace("```python","").replace("```","").strip()
        except: return ""

    def _sandbox(self, code):
        try:
            with tempfile.TemporaryDirectory() as td:
                with open(os.path.join(td,"t.py"),"w") as f: f.write(f"{code}\nif __name__=='__main__': print('OK')")
                self.docker.containers.run("python:3.11-slim", "python /app/t.py", volumes={td:{'bind':'/app','mode':'rw'}}, network_mode="none", remove=True)
            return True
        except: return False
