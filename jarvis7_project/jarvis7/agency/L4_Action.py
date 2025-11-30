import json
import os
import inspect
import importlib.util
from pathlib import Path
from typing import Callable

class ToolRegistry:
    def __init__(self, state, kernel):
        self.state = state
        self.kernel = kernel
        self._tools = {}
        self._schemas = {}
        self.file_root = Path(os.environ.get("JARVIS_FILE_ROOT", ".")).resolve()
        self.skill_root = Path(os.environ.get("JARVIS_SKILL_ROOT", "./learned_skills")).resolve()

        self.register("list_files", self._list_files, "List files.")
        self.register("read_file", self._read_file, "Read file content.")
        self.register("mem_recall", self._mem_recall, "Semantic search.")
        self.register("mem_read_log", self._mem_read_log, "Read raw logs.")

        self.load_learned_skills()

    def register(self, name: str, func: Callable, desc: str, manual_schema: dict = None):
        self._tools[name] = func
        func.__doc__ = desc
        if manual_schema: self._schemas[name] = manual_schema
        else: self._schemas[name] = self._generate_schema_from_func(func)

    def load_learned_skills(self):
        reg = self.skill_root / "skills_registry.json"
        if not reg.exists(): return
        try:
            with open(reg) as f: registry = json.load(f)
            for file, meta in registry.items():
                path = self.skill_root / file
                if not path.exists(): continue
                spec = importlib.util.spec_from_file_location(meta['intent'], path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "execute"):
                    self.register(meta['intent'], mod.execute, f"Auto-skill: {meta['intent']}")
        except: pass

    def _generate_schema_from_func(self, func):
        try: sig = inspect.signature(func)
        except: return {"type":"object", "properties":{}}
        params = {"type":"object", "properties":{}, "required":[]}
        for n, p in sig.parameters.items():
            if n in ["self", "kwargs"]: continue
            pt = "string"
            if p.annotation == int: pt = "integer"
            if p.annotation == float: pt = "number"
            params["properties"][n] = {"type": pt}
            if p.default == inspect.Parameter.empty: params["required"].append(n)
        return params

    @property
    def definitions(self):
        return [{"type":"function","function":{"name":n,"description":f.__doc__,"parameters":self._schemas[n]}} for n,f in self._tools.items()]

    def execute(self, name, **kwargs):
        if name in self._tools:
            try: return str(self._tools[name](**kwargs))
            except Exception as e: return f"Error: {e}"
        return "Unknown tool"

    # Core Impls with Type Hints
    def _list_files(self, subdir: str = ""): return [str(p.name) for p in (self.file_root/subdir).glob("*")]
    def _read_file(self, path: str):
        t = self.file_root / path
        if not str(t).startswith(str(self.file_root)): return "Access Denied"
        if not t.exists(): return "Not found"
        return t.read_text(errors='replace')[:2000]
    def _mem_recall(self, query: str): return self.state.memory.get_relevant_context(query)
    def _mem_read_log(self, page_index: int): return self.kernel.mount_page(int(page_index))
