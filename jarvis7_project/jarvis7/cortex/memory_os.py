import time
import tiktoken
from typing import List, Dict
from dataclasses import dataclass
from ..memory.episodic import EpisodicMemory
from ..memory.graph import KnowledgeGraph
from ..config import CONTEXT_MODE, TIER4_PAGE_SIZE

@dataclass
class MemoryBlock:
    content: str
    role: str
    timestamp: float
    locked: bool = False

class ContextKernel:
    def __init__(self, state_module):
        self.state = state_module
        self.encoder = tiktoken.get_encoding("cl100k_base")
        self.working_memory: List[MemoryBlock] = []
        self.episodic = EpisodicMemory()
        self.graph = KnowledgeGraph()
        self.boot_block = ""

    def set_boot_sequence(self, prompt: str): self.boot_block = prompt

    def add_interaction(self, role: str, content: str, locked: bool = False):
        block = MemoryBlock(content, role, time.time(), locked)
        self.working_memory.append(block)
        if role in ["user", "assistant"]:
            self.state.log_episode(content, content if role=="assistant" else "")

    def render(self) -> List[Dict[str, str]]:
        if CONTEXT_MODE == "tier5": return self._render_infinite()
        return self._render_paged()

    def _render_infinite(self):
        msgs = [{"role": "system", "content": self.boot_block}]
        for b in self.working_memory: msgs.append({"role": b.role, "content": b.content})
        return msgs

    def _render_paged(self):
        current_tokens = 0
        compiled_msgs = []
        sys_msg = {"role": "system", "content": self.boot_block}
        compiled_msgs.append(sys_msg)
        current_tokens += len(self.encoder.encode(self.boot_block))

        temp_buffer = []
        evicted = False
        
        for block in reversed(self.working_memory):
            count = len(self.encoder.encode(block.content))
            if block.locked or (current_tokens + count < TIER4_PAGE_SIZE):
                temp_buffer.append({"role": block.role, "content": block.content})
                current_tokens += count
            else:
                evicted = True
        
        if evicted:
            compiled_msgs.append({"role": "system", "content": "SYSTEM ALERT: Old memories paged to disk. Use 'mem_read_log' to retrieve."})
            
        compiled_msgs.extend(reversed(temp_buffer))
        return compiled_msgs

    def mount_page(self, page_index: int, page_size: int = 10) -> str:
        full = self.episodic.to_list(n=1000)
        start = page_index * page_size
        if start >= len(full): return "End of logs."
        slice_data = full[start : start + page_size]
        return "\n".join([f"[{time.ctime(x['timestamp'])}] {x['user_text']} -> {x['assistant_text']}" for x in slice_data])
