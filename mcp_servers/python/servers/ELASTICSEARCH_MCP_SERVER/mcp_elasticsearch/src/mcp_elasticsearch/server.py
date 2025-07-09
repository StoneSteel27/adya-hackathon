import asyncio
import logging
import warnings
from elasticsearch import Elasticsearch
from mcp.server import Server
from mcp.types import Tool, TextContent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_es_client(__credentials__: dict) -> Elasticsearch:
    """Create an Elasticsearch client from credentials."""
    if not __credentials__:
        raise ValueError("Missing credentials")

    es_url = __credentials__.get("ES_URL")
    api_key = __credentials__.get("ES_API_KEY")

    if not es_url or not api_key:
        raise ValueError("ES_URL and ES_API_KEY are required in credentials")

    verify_certs = str(__credentials__.get("ELASTICSEARCH_VERIFY_CERTS", "true")).lower() == "true"

    if not verify_certs:
        warnings.filterwarnings("ignore", message=".*verify_certs=False is insecure.*")
        warnings.filterwarnings("ignore", message=".*Unverified HTTPS request is being made to host.*")
        try:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        except ImportError:
            pass

    return Elasticsearch(
        hosts=[es_url],
        api_key=api_key,
        verify_certs=verify_certs
    )

app = Server("mcp-elasticsearch")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Elasticsearch tools with extensive descriptions and examples."""
    logger.info("Listing tools...")
    return [
        # Index Tools
        Tool(
            name="list_indices",
            description="Lists all indices in the cluster, providing details like health, status, name, and size.",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_index",
            description="Retrieves detailed information about one or more indices, including mappings and settings. Example: get_index(index='my-index')",
            inputSchema={"type": "object", "properties": {"index": {"type": "string"}}, "required": ["index"]}
        ),
        Tool(
            name="create_index",
            description="Creates a new index with optional settings and mappings. Example: create_index(index='my-new-index', body={'settings': {'number_of_shards': 1}})",
            inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "body": {"type": "object"}}, "required": ["index"]}
        ),
        Tool(
            name="delete_index",
            description="Deletes an existing index. This action is irreversible. Example: delete_index(index='my-old-index')",
            inputSchema={"type": "object", "properties": {"index": {"type": "string"}}, "required": ["index"]}
        ),
        # Document Tools
        Tool(
            name="search_documents",
            description="Searches for documents within an index. Can accept a simple query string or a full Elasticsearch Query DSL. Simple example: search_documents(index='my-index', body={'query': 'hello world'}). Advanced example: search_documents(index='my-index', body={'query': {'match': {'field_name': 'hello'}}})",
            inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "body": {"type": "object"}}, "required": ["index"]}
        ),
        Tool(
            name="index_document",
            description="Creates or updates a document in an index. If an 'id' is provided, it will update the existing document. Example: index_document(index='my-index', id='1', document={'title': 'New Title', 'content': 'Some content.'})",
            inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "document": {"type": "object"}, "id": {"type": "string"}}, "required": ["index", "document"]}
        ),
        Tool(
            name="get_document",
            description="Retrieves a specific document by its ID from an index. Example: get_document(index='my-index', id='1')",
            inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "id": {"type": "string"}}, "required": ["index", "id"]}
        ),
        Tool(
            name="delete_document",
            description="Deletes a specific document by its ID from an index. Example: delete_document(index='my-index', id='1')",
            inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "id": {"type": "string"}}, "required": ["index", "id"]}
        ),
        Tool(
            name="delete_by_query",
            description="Deletes all documents from an index that match a specific query. Example: delete_by_query(index='my-index', body={'query': {'match': {'user.id': 'kimchy'}}})",
            inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "body": {"type": "object"}}, "required": ["index", "body"]}
        ),
        # Cluster Tools
        Tool(
            name="get_cluster_health",
            description="Returns the health status of the cluster (green, yellow, or red) and other key statistics like the number of nodes and shards.",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_cluster_stats",
            description="Returns a comprehensive overview of cluster statistics, including node counts, index metrics, and memory usage.",
            inputSchema={"type": "object", "properties": {}}
        ),
        # Alias Tools
        Tool(
            name="list_aliases",
            description="Lists all aliases, which are secondary names for indices that can be used for searching and filtering.",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_alias",
            description="Retrieves information about a specific alias for a given index. Example: get_alias(index='my-index', name='my-alias')",
            inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "name": {"type": "string"}}, "required": ["index"]}
        ),
        Tool(
            name="put_alias",
            description="Creates or updates an alias for an index. Can be used to switch an alias to a new index. Example: put_alias(index='my-index-v2', name='my-app-alias')",
            inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "name": {"type": "string"}, "body": {"type": "object"}}, "required": ["index", "name"]}
        ),
        Tool(
            name="delete_alias",
            description="Deletes an alias from a specific index. Example: delete_alias(index='my-index-v1', name='my-app-alias')",
            inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "name": {"type": "string"}}, "required": ["index", "name"]}
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute Elasticsearch tools."""
    logger.info(f"Calling tool: {name} with arguments: {arguments}")
    
    __credentials__ = arguments.pop("__credentials__", None)
    arguments.pop("server_credentials", None)  # Remove the extra credentials argument
    es_client = get_es_client(__credentials__=__credentials__)

    result = None
    try:
        # Index Tools
        if name == "list_indices":
            result = es_client.cat.indices(**arguments)
        elif name == "get_index":
            result = es_client.indices.get(**arguments)
        elif name == "create_index":
            result = es_client.indices.create(**arguments)
        elif name == "delete_index":
            result = es_client.indices.delete(**arguments)
        # Document Tools
        elif name == "search_documents":
            if "body" in arguments and "query" in arguments["body"] and isinstance(arguments["body"]["query"], str):
                query_str = arguments["body"].pop("query")
                if not arguments["body"]:
                    arguments["body"] = {
                        "query": {
                            "multi_match": {
                                "query": query_str
                            }
                        }
                    }
            result = es_client.search(**arguments)
        elif name == "index_document":
            result = es_client.index(**arguments)
        elif name == "get_document":
            result = es_client.get(**arguments)
        elif name == "delete_document":
            result = es_client.delete(**arguments)
        elif name == "delete_by_query":
            result = es_client.delete_by_query(**arguments)
        # Cluster Tools
        elif name == "get_cluster_health":
            result = es_client.cluster.health(**arguments)
        elif name == "get_cluster_stats":
            result = es_client.cluster.stats(**arguments)
        # Alias Tools
        elif name == "list_aliases":
            result = es_client.cat.aliases(**arguments)
        elif name == "get_alias":
            result = es_client.indices.get_alias(**arguments)
        elif name == "put_alias":
            result = es_client.indices.put_alias(**arguments)
        elif name == "delete_alias":
            result = es_client.indices.delete_alias(**arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]

    return [TextContent(type="text", text=str(result))]

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