# The Crucible's Adya Hackathon Repository

This project contains a collection of MCP servers that can be used to interact with various services.

## Python Servers

- [Aiven MCP Server](./mcp_servers/python/servers/AIVEN_MCP_SERVER) - [Documentation](./mcp_servers_documentation/AIVEN_MCP_SERVER)
- [Discord MCP Server](./mcp_servers/python/servers/DISCORD_MCP_SERVER) - [Documentation](./mcp_servers_documentation/DISCORD_MCP_SERVER)
- [Elasticsearch MCP Server](./mcp_servers/python/servers/ELASTICSEARCH_MCP_SERVER) - [Documentation](./mcp_servers_documentation/ELASTICSEARCH_MCP_SERVER)
- [MySQL MCP Server](./mcp_servers/python/servers/MYSQL_MCP_SERVER) - [Documentation](./mcp_servers_documentation/MYSQL_MCP_SERVER)
- [Pandas MCP Server](./mcp_servers/python/servers/PANDAS_MCP_SERVER) - [Documentation](./mcp_servers_documentation/PANDAS_MCP_SERVER)

## Client Setup

To run the Python client, navigate to the `mcp_servers/python/clients` directory and follow these steps:

1.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

2.  **Activate the virtual environment:**
    -   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    -   **Unix/macOS:**
        ```bash
        source .venv/bin/activate
        ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the client:**
    ```bash
    python run.py
    ```

### Memebers in Team "The Crucible"
- Kanishq V (Leader)
- Lohith Varun R
- Harish G
- Sharan B
