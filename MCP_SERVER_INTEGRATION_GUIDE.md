### **Report: Aiven MCP Server Integration and Structure**

This document outlines the directory, code, and module structure of the Aiven MCP server. It is intended to be a blueprint for developers looking to integrate new Python-based MCP servers into the existing framework. The key principle is to follow the established pattern, which promotes consistency and simplifies integration.

The Aiven MCP server's implementation was based on the existing `MYSQL_MCP_SERVER`, which should be considered the primary template.

#### **1. Directory Structure**

A consistent directory structure is crucial. Each new server should be self-contained within its own project folder.

The structure for the Aiven server is as follows:

```
mcp_servers/python/servers/
└── AIVEN_MCP_SERVER/                # 1. Uppercase name for the server's container folder.
    └── mcp_aiven/                   # 2. Lowercase project name, as defined in pyproject.toml.
        ├── .venv/                   #    (Ignored by Git) Virtual environment for dependencies.
        ├── src/                     # 3. Source code directory.
        │   └── mcp_aiven/           # 4. The Python package directory. Must match the project name.
        │       ├── __init__.py      # 5. Makes the directory a package and defines the entry point.
        │       └── server.py        # 6. Core application logic for the MCP server.
        ├── pyproject.toml           # 7. Project definition, dependencies, and scripts.
        ├── README.md                #    (Optional) Project-specific documentation.
        └── uv.lock                  #    Lockfile for reproducible dependencies.
```

**Key Takeaways for New Integrations:**

1.  Create a main folder in `mcp_servers/python/servers/` with an uppercase name (e.g., `NEW_SERVER/`).
2.  Inside it, create a lowercase project folder (e.g., `new_server/`).
3.  The source code must reside in `src/` and be contained within a directory that can act as a Python package (i.e., `src/new_server/`).

---

#### **2. Project Configuration (`pyproject.toml`)**

This file is the heart of the Python project. It defines the project's metadata, dependencies, and, most importantly, the command-line script that makes it runnable.

**Key Sections of `mcp_aiven/pyproject.toml`:**

```toml
[project]
name = "mcp-aiven"  # The name of the package on PyPI, if published.
version = "0.1.4"
description = "An MCP server for Aiven."
requires-python = ">=3.11"
dependencies = [
     "mcp[cli]>=1.3.0", # CRITICAL: The core MCP library.
     "python-dotenv>=1.0.1",
     "uvicorn>=0.34.0",
     "aiven-client>=4.5.1", # Server-specific dependency.
]

# This section makes the server runnable via `uv run`.
[project.scripts]
mcp-aiven = "mcp_aiven:main" # Maps `uv run mcp-aiven` to the `main` function in the `mcp_aiven` package.

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# This tells the build system what to include in the final package.
[tool.hatch.build.targets.wheel]
packages = ["src/mcp_aiven"] # Specifies that `src/mcp_aiven` is the package to be built.
```

**Key Takeaways for New Integrations:**

*   **Dependencies:** Add your server's specific Python libraries to the `[project.dependencies]` list. The `mcp[cli]` dependency is essential.
*   **Scripts:** The `[project.scripts]` section is vital. Define a script (e.g., `new-server = "new_server:main"`) that maps a command to the `main` function in your package's `__init__.py`.
*   **Packaging:** Update `[tool.hatch.build.targets.wheel]` to point to your source package directory (e.g., `packages = ["src/new_server"]`).

---

#### **3. Module and Code Structure**

The code is structured to separate the entry point from the core server logic, which is necessary to handle the asynchronous nature of the MCP server.

**A. The Entry Point (`src/mcp_aiven/__init__.py`)**

The `[project.scripts]` entry in `pyproject.toml` needs to call a synchronous function. However, the MCP server runs asynchronously. This `__init__.py` file acts as a bridge.

```python
from . import server  # Import the server.py module.
import asyncio

def main():
   """Main entry point for the package."""
   # Run the asynchronous main function from the server module.
   asyncio.run(server.main())

# Expose important items at package level
__all__ = ['main', 'server']
```

**Key Takeaways for New Integrations:**

*   This file should be replicated exactly for your new server. Simply change the package name if necessary, although relative imports (`. import server`) make it generic. Its purpose is to create a synchronous `main` function that the command line can execute.

**B. The Core Logic (`src/mcp_aiven/server.py`)**

This file contains the actual implementation of your MCP server.

```python
import asyncio
import logging
from aiven.client import client # Specific SDK for this server
from mcp.server import Server
from mcp.types import Tool, TextContent

# ... (Logging configuration) ...

# ... (Helper functions like get_aiven_client) ...

# 1. Initialize the MCP Server
app = Server("mcp-aiven") # Use the server's name

# 2. Implement the @app.list_tools() decorator
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Aiven tools."""
    logger.info("Listing tools...")
    return [
        Tool(
            name="list_projects",
            description="List all projects on your Aiven account.",
            inputSchema={"type": "object", "properties": {}}
        ),
        # ... other tools
    ]

# 3. Implement the @app.call_tool() decorator
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute Aiven tools."""
    # Credential handling
    __credentials__ = arguments.pop("__credentials__")
    aiven_client = get_aiven_client(__credentials__)
    
    # Tool dispatching logic
    if name == "list_projects":
        # ... call the SDK and process results
        return [TextContent(type="text", text=str(project_names))]
    # ... elif for other tools
    else:
        raise ValueError(f"Unknown tool: {name}")

# 4. The main async function to run the server
async def main():
    """Main entry point to run the MCP server."""
    from mcp.server.stdio import stdio_server

    logger.info("Starting Aiven MCP server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )
```

**Key Takeaways for New Integrations:**

1.  **Initialize `Server`:** Create an instance of `mcp.server.Server` with your server's unique name.
2.  **Implement `list_tools`:** This function advertises your server's capabilities. Define each tool with a unique `name`, a clear `description`, and a JSON `inputSchema` that defines the arguments it accepts.
3.  **Implement `call_tool`:** This is the workhorse. It receives the tool `name` and `arguments`.
    *   Securely extract credentials from the `arguments`.
    *   Use an `if/elif/else` block to determine which tool was called.
    *   Execute the corresponding logic using the third-party SDK or library.
    *   Return the result wrapped in a `list` of `mcp.types.TextContent` objects.
4.  **Create `async def main()`:** This function contains the boilerplate for running the server over `stdio`, which is how it communicates with the MCP client. This can be copied directly.

---

#### **4. Client-Side Integration**

After building the server, you must register it with the Python MCP client so it can be launched and used. This involves editing two files in `mcp_servers/python/clients/src/`.

**A. Registering the Server for Launch (`client_and_server_config.py`)**

This file tells the client application how to start your server as a subprocess. You need to add a new dictionary to the `ServersConfig` list.

```python
# In mcp_servers/python/clients/src/client_and_server_config.py

ServersConfig = [
	# ... other servers
	{
		"server_name": "AIVEN_MCP_SERVER", # The unique name for your server.
		"command":"uv", # The command to run. Usually "uv".
		"args": [ # The arguments for the command.
			"--directory",
			"../servers/AIVEN_MCP_SERVER/mcp_aiven", # Path to the server's project folder.
			"run",
			"mcp-aiven" # The script name from pyproject.toml.
		]
	}
]
```

**Key Takeaways for New Integrations:**

*   Add a new entry to `ServersConfig`.
*   `server_name` must be the unique identifier you've used elsewhere.
*   Update the `args` to point to your new server's directory and the script name you defined in its `pyproject.toml`.

**B. Handling Credentials (`client_and_server_execution.py`)**

This file's `call_and_execute_tool` function is responsible for passing credentials from the client to the MCP server during a tool call. You must add a `case` for your new server to the `match/case` block.

```python
# In mcp_servers/python/clients/src/client_and_server_execution.py

async def call_and_execute_tool(
    selected_server: str,
    credentials: Any,
    tool_name: str,
    args: Dict[str, Any]
) -> Any:
    # ...
    
    # switch/case for injecting creds (Python 3.10+)
    match selected_server:
        # ... other servers
        case "AIVEN_MCP_SERVER":
            args["__credentials__"]   = creds
            args["server_credentials"] = creds
        case _:
            pass
    # ...
```

**Key Takeaways for New Integrations:**

*   Add a `case "YOUR_SERVER_NAME":` to the `match` block.
*   Inside the case, add the lines `args["__credentials__"] = creds` and `args["server_credentials"] = creds`. This ensures that the credentials provided by the end-user are correctly injected into the arguments sent to your MCP server.

---

#### **5. Postman and Git Integration**

*   **Postman:** To facilitate testing, add a new request for your server to the `postman_api_collections/MCP.postman_collection.json` file. Copy an existing request (like the one for Aiven or MySQL) and modify the `selected_servers` and `selected_server_credentials` fields to match your new server's name and required credentials.
*   **.gitignore:** Ensure that any virtual environment directories (`.venv/`) or other generated artifacts are included in the root `.gitignore` file to keep the repository clean. The entry `**/.venv` handles this for all servers.