from fastapi import FastAPI
from mcp import MCPServer
from api.tools import tools
from api.resources import resources
from db.session import get_db
from schemas.pydantic_models import MCPTool, MCPResource

app = FastAPI()

# Initialize the MCP server
mcp_server = MCPServer()

# Register tools
for tool in tools:
    mcp_server.add_tool(tool)

# Register resources
for resource in resources:
    mcp_server.add_resource(resource)

@app.on_event("startup")
async def startup_event():
    # Connect to the database
    await get_db()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Welcome to the MCP Course Catalog Server!"}

# Run the MCP server
if __name__ == "__main__":
    mcp_server.run(app, host="0.0.0.0", port=8080)