from typing import Dict, Optional, List
from mcp.types import Tool

class IndexTools:
    def __init__(self, search_client):
        self.search_client = search_client

    def get_tools(self) -> list[Tool]:
        return [
            Tool(name="list_indices", description="List all indices.", inputSchema={"type": "object", "properties": {}}),
            Tool(name="get_index", description="Get information about one or more indices.", inputSchema={"type": "object", "properties": {"index": {"type": "string"}}}),
            Tool(name="create_index", description="Create a new index.", inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "body": {"type": "object"}}}),
            Tool(name="delete_index", description="Delete an index.", inputSchema={"type": "object", "properties": {"index": {"type": "string"}}}),
        ]

    def call_tool(self, name: str, arguments: dict) -> any:
        if name == "list_indices":
            return self.search_client.list_indices()
        elif name == "get_index":
            return self.search_client.get_index(**arguments)
        elif name == "create_index":
            return self.search_client.create_index(**arguments)
        elif name == "delete_index":
            return self.search_client.delete_index(**arguments)
        else:
            return None
