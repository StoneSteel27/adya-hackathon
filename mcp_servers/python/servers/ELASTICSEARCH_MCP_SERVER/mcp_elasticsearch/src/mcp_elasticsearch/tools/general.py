from typing import Dict, Optional
from mcp.types import Tool

class GeneralTools:
    def __init__(self, search_client):
        self.search_client = search_client

    def get_tools(self) -> list[Tool]:
        return [
            Tool(
                name="general_api_request",
                description="Perform a general HTTP API request. Use this tool for any Elasticsearch/OpenSearch API that does not have a dedicated tool.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "method": {"type": "string"},
                        "path": {"type": "string"},
                        "params": {"type": "object"},
                        "body": {"type": "object"},
                    },
                },
            ),
        ]

    def call_tool(self, name: str, arguments: dict) -> any:
        if name == "general_api_request":
            return self.search_client.general_api_request(**arguments)
        else:
            return None