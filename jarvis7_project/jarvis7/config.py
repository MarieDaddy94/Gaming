import os
# "tier4" = Agentic Paging | "tier5" = Infinite Context
CONTEXT_MODE = os.environ.get("JARVIS_CONTEXT_MODE", "tier4")
TIER4_PAGE_SIZE = 12000 
