import json
import os
import uuid
import time
import tempfile
from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class Goal:
    id: str
    description: str
    priority: str
    status: str
    created_at: float
    deadline: Optional[float] = None

class GoalManager:
    def __init__(self, path="memory_store/goals.json"):
        self.path = os.path.abspath(path)
        self.goals: List[Goal] = []
        self._load()

    def add_goal(self, description: str, priority: str = "med", deadline: float = 0.0) -> str:
        gid = str(uuid.uuid4())[:8]
        dl = deadline if deadline > 0 else None
        g = Goal(gid, description, priority, "pending", time.time(), dl)
        self.goals.append(g)
        self._atomic_save()
        return gid

    def render(self) -> str:
        active = [g for g in self.goals if g.status in ["active", "pending"]]
        if not active: return "GOALS: No active goals."
        lines = ["ACTIVE GOALS:"]
        for g in sorted(active, key=lambda x: x.priority):
            lines.append(f"- [{g.priority.upper()}] {g.description} (ID: {g.id})")
        return "\n".join(lines)

    def _atomic_save(self):
        try:
            dir_name = os.path.dirname(self.path)
            with tempfile.NamedTemporaryFile('w', delete=False, dir=dir_name) as tf:
                json.dump([asdict(g) for g in self.goals], tf, indent=2)
                tempname = tf.name
            os.replace(tempname, self.path)
        except: pass

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path) as f: self.goals = [Goal(**g) for g in json.load(f)]
            except: pass
