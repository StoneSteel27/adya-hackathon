import asyncio
import logging
from mysql.connector import connect, Error
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent
from pydantic import AnyUrl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mysql_mcp_server")

def get_db_config(credentials: dict):
    """Get database configuration from credentials."""
    port = credentials.get("port")
    if not port or not str(port).strip():
        port = 3306
    else:
        try:
            port = int(port)
        except (ValueError, TypeError):
            raise ValueError("Invalid port number provided. Port must be a valid integer.")

    config = {
        "host": credentials.get("host", "localhost"),
        "port": port,
        "user": credentials.get("user"),
        "password": credentials.get("password"),
        "database": credentials.get("database"),
        "charset": credentials.get("charset", "utf8mb4"),
        "collation": credentials.get("collation", "utf8mb4_unicode_ci"),
        "autocommit": True,
        "sql_mode": credentials.get("sql_mode", "TRADITIONAL")
    }

    config = {k: v for k, v in config.items() if v is not None}

    if not all([config.get("user"), config.get("password"), config.get("database")]):
        logger.error("Missing required database configuration in credentials.")
        raise ValueError("Missing required database configuration in credentials")

    return config

# Initialize server
app = Server("mysql_mcp_server")

@app.list_resources()
async def list_resources(__credentials__: dict) -> list[Resource]:
    """List MySQL tables as resources."""
    config = get_db_config(__credentials__)
    try:
        logger.info(f"Connecting to MySQL with charset: {config.get('charset')}, collation: {config.get('collation')}")
        with connect(**config) as conn:
            logger.info(f"Successfully connected to MySQL server version: {conn.get_server_info()}")
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                logger.info(f"Found tables: {tables}")

                resources = []
                for table in tables:
                    resources.append(
                        Resource(
                            uri=f"mysql://{table[0]}/data",
                            name=f"Table: {table[0]}",
                            mimeType="text/plain",
                            description=f"Data in table: {table[0]}"
                        )
                    )
                return resources
    except Error as e:
        logger.error(f"Failed to list resources: {str(e)}")
        logger.error(f"Error code: {e.errno}, SQL state: {e.sqlstate}")
        return []

@app.read_resource()
async def read_resource(uri: AnyUrl, __credentials__: dict) -> str:
    """Read table contents."""
    config = get_db_config(__credentials__)
    uri_str = str(uri)
    logger.info(f"Reading resource: {uri_str}")

    if not uri_str.startswith("mysql://"):
        raise ValueError(f"Invalid URI scheme: {uri_str}")

    parts = uri_str[8:].split('/')
    table = parts[0]

    try:
        logger.info(f"Connecting to MySQL with charset: {config.get('charset')}, collation: {config.get('collation')}")
        with connect(**config) as conn:
            logger.info(f"Successfully connected to MySQL server version: {conn.get_server_info()}")
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table} LIMIT 100")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                result = [",".join(map(str, row)) for row in rows]
                return "\n".join([",".join(columns)] + result)

    except Error as e:
        logger.error(f"Database error reading resource {uri}: {str(e)}")
        logger.error(f"Error code: {e.errno}, SQL state: {e.sqlstate}")
        raise RuntimeError(f"Database error: {str(e)}")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MySQL tools."""
    logger.info("Listing tools...")
    return [
        Tool(
            name="execute_sql",
            description="Execute an SQL query on the MySQL server",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SQL query to execute"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute SQL commands."""
    if "__credentials__" not in arguments:
        raise ValueError("Missing credentials in tool call arguments")
    
    __credentials__ = arguments.pop("__credentials__")
    config = get_db_config(__credentials__)
    logger.info(f"Calling tool: {name} with arguments: {arguments}")

    if name != "execute_sql":
        raise ValueError(f"Unknown tool: {name}")

    query = arguments.get("query")
    if not query:
        raise ValueError("Query is required")

    try:
        logger.info(f"Connecting to MySQL with charset: {config.get('charset')}, collation: {config.get('collation')}")
        with connect(**config) as conn:
            logger.info(f"Successfully connected to MySQL server version: {conn.get_server_info()}")
            with conn.cursor() as cursor:
                cursor.execute(query)

                if query.strip().upper().startswith("SHOW TABLES"):
                    tables = cursor.fetchall()
                    result = ["Tables_in_" + config["database"]]
                    result.extend([table[0] for table in tables])
                    return [TextContent(type="text", text="\n".join(result))]

                elif cursor.description is not None:
                    columns = [desc[0] for desc in cursor.description]
                    try:
                        rows = cursor.fetchall()
                        result = [",".join(map(str, row)) for row in rows]
                        return [TextContent(type="text", text="\n".join([",".join(columns)] + result))]
                    except Error as e:
                        logger.warning(f"Error fetching results: {str(e)}")
                        return [TextContent(type="text", text=f"Query executed but error fetching results: {str(e)}")]

                else:
                    conn.commit()
                    return [TextContent(type="text", text=f"Query executed successfully. Rows affected: {cursor.rowcount}")]

    except Error as e:
        logger.error(f"Error executing SQL '{query}': {e}")
        logger.error(f"Error code: {e.errno}, SQL state: {e.sqlstate}")
        return [TextContent(type="text", text=f"Error executing query: {str(e)}")]

async def main():
    """Main entry point to run the MCP server."""
    from mcp.server.stdio import stdio_server

    logger.info("Starting MySQL MCP server...")

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

if __name__ == "__main__":
    asyncio.run(main())
