from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from ..jarvis_core.state import JarvisState
from ..agency.L8_Dialogue import DialogueEngine

app = FastAPI()
state = JarvisState()
engine = DialogueEngine(state)

class ChatRequest(BaseModel): text: str

@app.post("/chat")
async def r(p: ChatRequest): return await engine.chat_async(p.text)

@app.websocket("/ws/chat")
async def w(s: WebSocket):
    await s.accept()
    try:
        while True: await s.send_json(await engine.chat_async(await s.receive_text()))
    except: pass

@app.get("/", response_class=HTMLResponse)
def ui(): return "<html><body><h1>Jarvis 7.5 Corporeal</h1><script>var w=new WebSocket('ws://'+location.host+'/ws/chat');w.onmessage=e=>console.log(JSON.parse(e.data))</script></body></html>"
