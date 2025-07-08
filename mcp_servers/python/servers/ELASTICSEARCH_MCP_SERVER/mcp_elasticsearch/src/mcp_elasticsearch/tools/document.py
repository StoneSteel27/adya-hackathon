from typing import Dict, Optional
from mcp.types import Tool

class DocumentTools:
    def __init__(self, search_client):
        self.search_client = search_client

    def get_tools(self) -> list[Tool]:
        return [
            Tool(name="search_documents", description="Search for documents.", inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "body": {"type": "object"}}}),
            Tool(name="index_document", description="Creates or updates a document in the index.", inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "document": {"type": "object"}, "id": {"type": "string"}}}),
            Tool(name="get_document", description="Get a document by ID.", inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "id": {"type": "string"}}}),
            Tool(name="delete_document", description="Delete a document by ID.", inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "id": {"type": "string"}}}),
            Tool(name="delete_by_query", description="Deletes documents matching the provided query.", inputSchema={"type": "object", "properties": {"index": {"type": "string"}, "body": {"type": "object"}}}),
        ]

    def call_tool(self, name: str, arguments: dict) -> any:
        if name == "search_documents":
            return self.search_client.search_documents(**arguments)
        elif name == "index_document":
            return self.search_client.index_document(**arguments)
        elif name == "get_document":
            return self.search_client.get_document(**arguments)
        elif name == "delete_document":
            return self.search_client.delete_document(**arguments)
        elif name == "delete_by_query":
            return self.search_client.delete_by_query(**arguments)
        else:
            return None