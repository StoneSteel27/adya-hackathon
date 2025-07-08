# Elasticsearch MCP Server

This directory contains the MCP server for Elasticsearch.

## Running the Server

To run the server, use the following command from the `mcp_servers/python/clients` directory:

```bash
uv run python run.py
```

Then, select `ELASTICSEARCH_MCP_SERVER` from the list of available servers.

## Credentials

The server requires credentials to be sent with each request. It supports API Key authentication.

To use API key authentication, provide the following credentials in the `selected_server_credentials` field of your request:

```json
{
    "ELASTICSEARCH_MCP_SERVER": {
        "ES_URL": "your_elasticsearch_url",
        "ES_API_KEY": "your_api_key"
    }
}
```
