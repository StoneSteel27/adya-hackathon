from typing import Dict
from mcp.types import Tool

class ClusterTools:
    def __init__(self, search_client):
        self.search_client = search_client

    def get_tools(self) -> list[Tool]:
        return [
            Tool(name="get_cluster_health", description="Returns basic information about the health of the cluster.", inputSchema={"type": "object", "properties": {}}),
            Tool(name="get_cluster_stats", description="Returns high-level overview of cluster statistics.", inputSchema={"type": "object", "properties": {}}),
        ]

    def call_tool(self, name: str, arguments: dict) -> any:
        if name == "get_cluster_health":
            return self.search_client.get_cluster_health()
        elif name == "get_cluster_stats":
            return self.search_client.get_cluster_stats()
        else:
            return None