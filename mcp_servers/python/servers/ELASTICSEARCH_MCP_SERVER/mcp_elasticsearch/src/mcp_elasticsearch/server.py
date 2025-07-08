import asyncio
import logging
from mcp.server import Server
from mcp.types import Tool, TextContent

from .clients import create_search_client
from .tools.alias import AliasTools
from .tools.cluster import ClusterTools
from .tools.document import DocumentTools
from .tools.general import GeneralTools
from .tools.index import IndexTools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Server("mcp-elasticsearch")

TOOL_CLASSES = [
    IndexTools,
    DocumentTools,
    ClusterTools,
    AliasTools,
    GeneralTools,
]

def get_all_tools(search_client=None):
    """Get all tools from all tool classes."""
    all_tools = []
    for tool_class in TOOL_CLASSES:
        # Pass the client (or None) to the tool class constructor
        tool_instance = tool_class(search_client)
        all_tools.extend(tool_instance.get_tools())
    return all_tools

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Elasticsearch tools."""
    logger.info("Listing tools...")
    # Pass no client to get the tool list, as we don't have credentials here.
    return get_all_tools()

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute Elasticsearch tools."""
    logger.info(f"Calling tool: {name} with arguments: {arguments}")
    
    __credentials__ = arguments.pop("__credentials__", None)
    search_client = create_search_client(__credentials__=__credentials__)

    result = None
    for tool_class in TOOL_CLASSES:
        tool_instance = tool_class(search_client)
        result = tool_instance.call_tool(name, arguments)
        if result is not None:
            break
    
    if result is not None:
        return [TextContent(type="text", text=str(result))]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point to run the MCP server."""
    from mcp.server.stdio import stdio_server

    logger.info("Starting Elasticsearch MCP server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
