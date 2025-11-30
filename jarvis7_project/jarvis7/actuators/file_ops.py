import os
from pathlib import Path

class FileActuator:
    def __init__(self):
        self.root = Path(os.environ.get("JARVIS_FILE_ROOT", ".")).resolve()

    def write_file(self, path: str, content: str) -> str:
        """Overwrite file content safely."""
        target = (self.root / path).resolve()
        if not str(target).startswith(str(self.root)): return "Error: Path traversal blocked."
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            return f"Successfully wrote {len(content)} chars to {path}"
        except Exception as e: return f"Write Error: {e}"
