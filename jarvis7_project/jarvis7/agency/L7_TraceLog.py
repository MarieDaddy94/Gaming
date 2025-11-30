import json
import time
import os
from dataclasses import dataclass, asdict
from typing import List, Any

@dataclass
class TraceItem:
    tool: str
    args: str
    result: str
    status: str
    timestamp: float

class TraceLogger:
    def __init__(self, log_file="L7_trace_history.json"):
        self.log_file = os.path.abspath(log_file)
        self.current_trace = []

    def start_episode(self): self.current_trace = []
    
    def log_tool_usage(self, tool, args, res, error=False):
        self.current_trace.append(TraceItem(tool, str(args), str(res)[:500], "error" if error else "success", time.time()))

    def end_episode(self, query, reply):
        if not self.current_trace: return
        data = {"timestamp":time.time(), "user_query":query, "final_response":reply, "tool_chain":[asdict(x) for x in self.current_trace]}
        try:
            with open(self.log_file, "a") as f: f.write(json.dumps(data)+"\n")
        except: pass
