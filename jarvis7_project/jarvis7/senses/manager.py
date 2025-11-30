import os
from pathlib import Path
from ..world_model.state import WorldModel

class SensorManager:
    def __init__(self, world_model: WorldModel):
        self.wm = world_model
        self.root = Path(os.environ.get("JARVIS_FILE_ROOT", "."))

    def scan_environment(self):
        try:
            for item in self.root.iterdir():
                if item.is_dir():
                    status = "dormant"
                    if (item / "requirements.txt").exists(): status = "active"
                    self.wm.update_project(item.name, str(item), status)
        except Exception as e: print(f"[Senses] Scan error: {e}")
