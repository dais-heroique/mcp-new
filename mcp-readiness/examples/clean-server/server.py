import logging
from mcp.server.fastmcp import FastMCP
from mcp.server.streamable_http import StreamableHTTPTransport
logger = logging.getLogger("demo")
mcp = FastMCP("clean-demo")
@mcp.tool()
def search_catalog(query: str) -> str:
    """Read-only search over a catalog."""
    logger.info("tool_call name=search_catalog")
    return f"results for {query}"
transport = StreamableHTTPTransport("/mcp", stateless=True)
