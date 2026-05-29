from fastapi import FastAPI, Depends
from typing import List, Dict
from src.api import tools as api_tools
from src.api import resources as api_resources
from src.db.session import SessionLocal
from src.schemas.pydantic_models import MCPTool, MCPResource
from pathlib import Path

app = FastAPI()


def register_mcp(app: FastAPI):
    """Synchronous registration of routers and discovery endpoints.

    This ensures the routes are present at import time so OpenAPI can be
    generated without running the ASGI server.
    """
    # Include routers that implement tool/resource behaviour
    app.include_router(api_tools.router, prefix="/api")
    app.include_router(api_resources.router, prefix="/api")

    # Build tool metadata from the module-level TOOLS variable in api.tools
    tools_meta: List[Dict] = []
    for t in getattr(api_tools, "TOOLS", []):
        tools_meta.append(t if not hasattr(t, "dict") else t.dict())

    # Discovery endpoints (handlers will fetch content at runtime)
    @app.get("/mcp/tools")
    def list_tools():
        return tools_meta

    @app.get("/mcp/resources")
    def list_resources():
        # Try to fetch live content; fall back to placeholders if DB unavailable
        db = SessionLocal()
        try:
            try:
                course_descriptions = api_resources.get_course_descriptions(db=db)
            except Exception:
                course_descriptions = ""
            try:
                department_directory = api_resources.get_department_directory(db=db)
            except Exception:
                department_directory = ""
            return [
                {"name": "course_descriptions", "description": "Formatted list of all courses and descriptions.", "content": course_descriptions},
                {"name": "department_directory", "description": "List of departments and codes.", "content": department_directory}
            ]
        finally:
            db.close()

    @app.get("/mcp/prompts")
    def list_prompts():
        prompts_dir = Path(__file__).parent.parent / "prompts"
        template_path = prompts_dir / "course_comparison_template.txt"
        if template_path.exists():
            return [{"name": "course_comparison_template", "template": template_path.read_text(encoding="utf-8")}]
        return []


async def create_mcp_server(app: FastAPI):
    """Async helper retained for runtime use; dynamic resource fetching is
    already supported via the synchronous `register_mcp` above.
    """
    # Nothing required here at the moment; registration is synchronous.
    return


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/")
async def root():
    return {"message": "Welcome to the MCP Course Catalog Server!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)