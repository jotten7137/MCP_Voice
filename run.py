# Simple entry point for running the MCP server
import uvicorn

if __name__ == "__main__":
    uvicorn.run("mcp_server.main:app", host="0.0.0.0", port=8000, reload=True)