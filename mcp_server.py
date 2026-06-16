import logging
from fastmcp import FastMCP
from tools import register_tools, get_tasks_service

# Set up basic local logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tasks-local-server")

# 1. Initialize a standard, local FastMCP server (no middleware)
mcp = FastMCP("Google Tasks Local Server")

# 2. Attach the tools from your tools.py file
register_tools(mcp)

if __name__ == "__main__":
    logger.info("Initializing Google Auth before starting server...")
    get_tasks_service()
    logger.info("Starting local Google Tasks MCP Server via stdio...")
    # Run the server locally
    mcp.run(transport="stdio")