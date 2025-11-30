import json
import os
import time
import tempfile
from dataclasses import dataclass, field, asdict
from typing import Dict

@dataclass
class ProjectState:
    name: str
    path: str
    status: str 
    last_scan: float = 0.0

@dataclass
class FinancialState:
    pnl_today: float = 0.0
    open_positions: int = 0
    risk_level: str = "low" 

@dataclass
class WorldState:
    user_name: str = "Anthony"
    location: str = "Montgomery, AL"
    projects: Dict[str, ProjectState] = field(default_factory=dict)
    finances: FinancialState = field(default_factory=FinancialState)
    system_health: str = "nominal"
    last_updated: float = field(default_factory=time.time)

class WorldModel:
    def __init__(self, persistence_path="memory_store/world_model.json"):
        self.path = os.path.abspath(persistence_path)
        self.state = WorldState()
        self._load()

    def update_project(self, name: str, path: str, status: str = "active"):
        self.state.projects[name] = ProjectState(name, path, status, time.time())
        self._atomic_save()

    def render(self) -> str:
        proj_str = ", ".join([f"{p.name}({p.status})" for p in self.state.projects.values()])
        return (
            f"WORLD CONTEXT:\n"
            f"- Projects: {proj_str if proj_str else 'None scanned'}\n"
            f"- Finance: PnL=${self.state.finances.pnl_today:.2f}\n"
            f"- System: {self.state.system_health}"
        )

    def _atomic_save(self):
        try:
            dir_name = os.path.dirname(self.path)
            with tempfile.NamedTemporaryFile('w', delete=False, dir=dir_name) as tf:
                json.dump(asdict(self.state), tf, indent=2)
                tempname = tf.name
            os.replace(tempname, self.path)
        except Exception as e: print(f"[WorldModel] Save Error: {e}")

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path) as f:
                    data = json.load(f)
                    self.state.finances = FinancialState(**data.get("finances", {}))
                    for k, v in data.get("projects", {}).items():
                        self.state.projects[k] = ProjectState(**v)
            except: pass
