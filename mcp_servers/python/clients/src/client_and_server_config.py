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
	},
	{
		"server_name": "PANDAS_MCP_SERVER",
		"command": "uv",
		"args": [
			"--directory",
			"../servers/PANDAS_MCP_SERVER/pandas-mcp-server",
			"run",
			"pandas-mcp-server"
		]
	},
	{
		"server_name": "DISCORD_MCP_SERVER",
		"command":"uv",
		"args": [
			"--directory",
			"../servers/DISCORD_MCP_SERVER/mcp_discord",
			"run",
			"mcp-discord"
		]
	}
]
