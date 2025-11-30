import time
from typing import Dict
from .gwt import GlobalWorkspace
from ..values import ValueSystem
from ..memory.episodic import EpisodicMemory

class JarvisState:
    def __init__(self):
        self.valence, self.arousal, self.entropy = 0.0, 0.0, 0.5
        self.last_update = time.time()
        self.episode_start = time.time()
        self._cached_gauges = {}

        self.gwt = GlobalWorkspace()
        self.values = ValueSystem()
        self.memory = EpisodicMemory()

    def update(self, stimulus_intensity=0.0):
        dt = time.time() - self.last_update
        self.last_update = time.time()
        self.arousal = max(0.0, self.arousal - (0.05 * dt))
        self.entropy = min(1.0, max(0.0, self.entropy + (0.01 * dt)))
        self.arousal = min(1.0, self.arousal + stimulus_intensity)
        self._compute_10d()

    @property
    def gauges(self): return self._cached_gauges

    def _compute_10d(self):
        duration = min(1.0, (time.time()-self.episode_start)/300)
        self._cached_gauges = {
            "Axis_0_Time": round(duration, 3),
            "Axis_1_Novelty": round(self.entropy, 3),
            "Axis_2_Focus": round((1-self.entropy)*(0.5+self.arousal*0.5), 3),
            "Axis_3_Urgency": round(self.arousal, 3),
            "Axis_9_Social": round((self.valence+1)/2, 3)
        }

    def log_episode(self, u, a): self.memory.add(u, a, self.gauges)
    def snapshot(self): return {"gauges": self.gauges, "gwt": self.gwt.to_dict()}
