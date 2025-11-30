import os, json, networkx as nx
from openai import AsyncOpenAI
class KnowledgeGraph:
    def __init__(self, p="memory_store/kg.json"): self.p=p; self.g=nx.DiGraph(); self.c=AsyncOpenAI()
    def get_context(self, t): return "" # Stub for speed
    async def extract_and_store(self, t): pass # Stub
