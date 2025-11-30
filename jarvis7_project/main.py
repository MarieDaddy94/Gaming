import os
import asyncio
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from jarvis7.dashboard.api import app as dashboard_app
from jarvis7.dashboard.api import engine 
from jarvis7.autonomy import AutonomyLoop

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[BOOT] Starting Autonomy Loop...")
    loop = AutonomyLoop(engine.world_model, engine.goals)
    task = asyncio.create_task(loop.start())
    yield
    print("[SHUTDOWN] Stopping Autonomy Loop...")
    loop.stop()
    await task

dashboard_app.router.lifespan_context = lifespan

if __name__ == "__main__":
    os.makedirs("./learned_skills", exist_ok=True)
    os.makedirs("./memory_store", exist_ok=True)
    
    os.environ.setdefault("JARVIS_FILE_ROOT", ".")
    os.environ.setdefault("JARVIS_SKILL_ROOT", "./learned_skills")

    print("[BOOT] Jarvis 7.5 Corporeal Initializing on http://0.0.0.0:8000 ...")
    uvicorn.run(dashboard_app, host="0.0.0.0", port=8000)
