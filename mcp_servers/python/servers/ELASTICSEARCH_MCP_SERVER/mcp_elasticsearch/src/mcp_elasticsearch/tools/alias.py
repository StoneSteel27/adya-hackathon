from typing import Dict, List
from mcp.types import Tool

class AliasTools:
    def __init__(self, search_client):
        self.search_client = search_client

    def get_tools(self) -> list[Tool]:
        return [
            Tool(name="list_aliases", description="List all aliases.", inputSchema={"type": "object", "properties": {}}),
            Tool(name="get_alias", description="Get alias information for a specific index.", inputSchema={"type": "object", "properties": {"index": {"type": "string"}}}),
            Tool(name="put_alias", description="Create or update an alias for a specific index.", inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "name": {"type": "string"}, "body": {"type": "object"}}}),
            Tool(name="delete_alias", description="Delete an alias for a specific index.", inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "name": {"type": "string"}}}),
        ]

    def call_tool(self, name: str, arguments: dict) -> any:
        if name == "list_aliases":
            return self.search_client.list_aliases()
        elif name == "get_alias":
            return self.search_client.get_alias(**arguments)
        elif name == "put_alias":
            return self.search_client.put_alias(**arguments)
        elif name == "delete_alias":
            return self.search_client.delete_alias(**arguments)
        else:
            return None