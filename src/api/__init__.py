from .tools import router as tools_router
from .resources import router as resources_router

__all__ = ["tools_router", "resources_router"]

try:
    # Tools metadata for discovery (minimal)
    from . import tools as _tools_mod
    TOOLS = getattr(_tools_mod, "TOOLS", [])
except Exception:
    TOOLS = []
