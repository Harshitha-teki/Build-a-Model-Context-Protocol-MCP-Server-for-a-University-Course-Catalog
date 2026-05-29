from fastapi import FastAPI
from src.mcp_server import create_mcp_server

app = FastAPI()
from src.mcp_server import register_mcp

# Register routes so OpenAPI includes them at import time
register_mcp(app)

@app.on_event("startup")
async def startup_event():
    # Initialize the MCP server
    await create_mcp_server(app)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)