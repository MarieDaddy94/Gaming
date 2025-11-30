from collections import deque
from dataclasses import dataclass
from openai import OpenAI

@dataclass
class Stimulus:
    channel: str
    content: str
    salience: float

class GlobalWorkspace:
    def __init__(self, max_raw=10):
        self.max_raw = max_raw
        self._raw = deque()
        self._summary = []
        self.client = OpenAI()

    def add_stimulus(self, ch, content, sal=1.0):
        self._raw.append(Stimulus(ch, content, sal))
        if len(self._raw) > self.max_raw: self._compress()

    def _compress(self):
        chunk = [self._raw.popleft() for _ in range(5) if self._raw]
        if not chunk: return
        txt = "\n".join([f"{s.channel}: {s.content}" for s in chunk])
        try:
            res = self.client.chat.completions.create(
                model="gpt-4o", messages=[{"role":"system","content":f"Summarize:\n{txt}"}]
            )
            self._summary.append(res.choices[0].message.content)
            if len(self._summary)>10: self._summary.pop(0)
        except: pass

    def get_context(self) -> str:
        mt = "RECENT SUMMARY:\n" + "\n".join(self._summary)
        st = "IMMEDIATE:\n" + "\n".join([f"[{s.channel}] {s.content}" for s in self._raw])
        return f"{mt}\n\n{st}"

    def to_dict(self): return {"raw": [s.content for s in self._raw], "summary": self._summary}
