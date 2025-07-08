ClientsConfig =[
    "MCP_CLIENT_AZURE_AI",
    "MCP_CLIENT_OPENAI",
	"MCP_CLIENT_GEMINI"
]
ServersConfig = [
	{
		"server_name": "MYSQL_MCP_SERVER",
		"command":"uv",
		"args": [
			"--directory",
			"../servers/MYSQL_MCP_SERVER/mysql-mcp-server",
			"run",
			"mysql-mcp-server"
		]
	},
	{
		"server_name": "AIVEN_MCP_SERVER",
		"command": "uv",
		"args": [
			"--directory",
			"../servers/AIVEN_MCP_SERVER/mcp_aiven",
			"run",
			"mcp-aiven"
		]
	},
	{
		"server_name": "ELASTICSEARCH_MCP_SERVER",
		"command": "uv",
		"args": [
			"--directory",
			"../servers/ELASTICSEARCH_MCP_SERVER/mcp_elasticsearch",
			"run",
			"mcp-elasticsearch"
		]
	}
]
