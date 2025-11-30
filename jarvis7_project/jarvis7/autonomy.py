import asyncio
from .senses.manager import SensorManager

class AutonomyLoop:
    def __init__(self, world_model, goals):
        self.sensor_mgr = SensorManager(world_model)
        self.goals = goals
        self.running = False

    async def start(self):
        print("[Autonomy] Heartbeat started.")
        self.running = True
        while self.running:
            try:
                self.sensor_mgr.scan_environment()
                await asyncio.sleep(60)
            except: await asyncio.sleep(60)

    def stop(self): self.running = False
