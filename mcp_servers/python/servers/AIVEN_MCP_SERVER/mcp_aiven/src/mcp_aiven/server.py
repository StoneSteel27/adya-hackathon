"""
Aiven MCP server.

This server provides tools to interact with the Aiven platform, allowing you to manage
your Aiven projects and services. The server uses the Aiven API to perform actions
on your behalf. You need to provide your Aiven API token to use the server.

Supported tools:
- list_projects: List all projects on your Aiven account.
- list_services: List all services in a specific Aiven project.
- get_service_details: Get the details of a service in a specific Aiven project.

Usage examples:
- To list all projects, use the `list_projects` tool.
- To list services in a project, use `list_services` with `project_name`.
- To get service details, use `get_service_details` with `project_name` and `service_name`.
"""
import asyncio
import logging
from aiven.client import client
from mcp.server import Server
from mcp.types import Tool, TextContent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("aiven_mcp_server")

def get_aiven_client(credentials: dict):
    """Get Aiven client from credentials."""
    if not credentials:
        raise ValueError("Missing credentials")
    
    base_url = credentials.get("AIVEN_BASE_URL")
    token = credentials.get("AIVEN_TOKEN")

    if not base_url or not token:
        raise ValueError("AIVEN_BASE_URL and AIVEN_TOKEN are required in credentials")

    aiven_client = client.AivenClient(base_url=base_url)
    aiven_client.set_auth_token(token)
    return aiven_client

# Initialize server
app = Server("mcp-aiven")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Aiven tools."""
    logger.info("Listing tools...")
    return [
        Tool(
            name="list_projects",
            description="List all projects on your Aiven account.",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="list_services",
            description="List all services in a specific Aiven project.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string", "description": "The name of the Aiven project."}
                },
                "required": ["project_name"]
            }
        ),
        Tool(
            name="get_service_details",
            description="Get the detail of your service in a specific Aiven project.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string", "description": "The name of the Aiven project."},
                    "service_name": {"type": "string", "description": "The name of the service."}
                },
                "required": ["project_name", "service_name"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute Aiven tools."""
    if "__credentials__" not in arguments:
        raise ValueError("Missing credentials in tool call arguments")
    
    __credentials__ = arguments.pop("__credentials__")
    aiven_client = get_aiven_client(__credentials__)
    logger.info(f"Calling tool: {name} with arguments: {arguments}")

    try:
        if name == "list_projects":
            results = aiven_client.get_projects()
            project_names = [result['project_name'] for result in results]
            return [TextContent(type="text", text=str(project_names))]
        
        elif name == "list_services":
            project_name = arguments.get("project_name")
            if not project_name:
                raise ValueError("project_name is required")
            results = aiven_client.get_services(project=project_name)
            service_names = [s["service_name"] for s in results]
            return [TextContent(type="text", text=str(service_names))]

        elif name == "get_service_details":
            project_name = arguments.get("project_name")
            service_name = arguments.get("service_name")
            if not project_name or not service_name:
                raise ValueError("project_name and service_name are required")
            result = aiven_client.get_service(project=project_name, service=service_name)
            return [TextContent(type="text", text=str(result))]
        
        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Error executing tool '{name}': {e}")
        return [TextContent(type="text", text=f"Error executing tool: {str(e)}")]

async def main():
    """Main entry point to run the MCP server."""
    from mcp.server.stdio import stdio_server

    logger.info("Starting Aiven MCP server...")

    async with stdio_server() as (read_stream, write_stream):
        try:
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
        except Exception as e:
            logger.error(f"Server error: {str(e)}", exc_info=True)
            raise

