import time, json, chromadb
class EpisodicMemory:
    def __init__(self, p="./memory_store"): self.c=chromadb.PersistentClient(path=p); self.col=self.c.get_or_create_collection("episodic")
    def add(self, u, a, g): self.col.add(documents=[f"{u}|{a}"], metadatas=[{"timestamp":time.time(),"user":u,"assistant":a,"gauges":json.dumps(g)}], ids=[str(time.time())])
    def get_relevant_context(self, q): return ""
    def to_list(self, n=10): return []
