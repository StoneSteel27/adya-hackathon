import asyncio
import logging
import pandas as pd
from mcp.server import Server
from mcp.types import Tool, TextContent
from io import StringIO
from contextlib import redirect_stdout
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Server("pandas-mcp-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Pandas tools."""
    logger.info("Listing tools...")
    return [
        Tool(
            name="summarize_dataframe",
            description="Provides a high-level summary of the dataframe, including shape, columns, data types, and the first 5 rows.",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_dataframe_head",
            description="Returns the first n rows of the dataframe.",
            inputSchema={
                "type": "object",
                "properties": {
                    "n": {
                        "type": "integer",
                        "description": "The number of rows to return.",
                        "default": 5
                    }
                }
            }
        ),
        Tool(
            name="get_column_statistics",
            description="Calculates and returns descriptive statistics for a specified numerical column.",
            inputSchema={
                "type": "object",
                "properties": {
                    "column_name": {
                        "type": "string",
                        "description": "The name of the numerical column to analyze."
                    }
                },
                "required": ["column_name"]
            }
        ),
        Tool(
            name="get_value_counts",
            description="Counts the unique values in a specified column.",
            inputSchema={
                "type": "object",
                "properties": {
                    "column_name": {
                        "type": "string",
                        "description": "The name of the column to count values for."
                    }
                },
                "required": ["column_name"]
            }
        ),
        Tool(
            name="run_pandas_code",
            description="Executes Python code using a pre-loaded Pandas DataFrame. The DataFrame is available as 'df' and pandas is imported as 'pd'. Use this for complex queries or operations not covered by other tools. The code's print output or the string representation of a variable named 'result' will be returned. Important: Saving files or generating plots/images is not supported.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Python code to execute."
                    }
                },
                "required": ["code"]
            }
        )
    ]

def get_dataframe_from_credentials(credentials: dict) -> pd.DataFrame:
    """Loads a DataFrame from a CSV URL provided in the credentials."""
    csv_url = credentials.get("csv_url")
    if not csv_url:
        raise ValueError("A 'csv_url' must be provided in __credentials__.")
    try:
        return pd.read_csv(csv_url)
    except Exception as e:
        raise ValueError(f"Error loading DataFrame from URL: {e}")

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute Pandas tools."""
    logger.info(f"Calling tool: {name} with args: {arguments}")
    __credentials__ = arguments.pop("__credentials__", {})
    
    try:
        df = get_dataframe_from_credentials(__credentials__)
    except ValueError as e:
        return [TextContent(type="text", text=str(e))]

    result_text = ""

    if name == "summarize_dataframe":
        buffer = StringIO()
        buffer.write(f"Shape: {df.shape}\n\n")
        buffer.write("Columns:\n")
        buffer.write(f"{df.columns.tolist()}\n\n")
        buffer.write("Data Types:\n")
        df.info(buf=buffer)
        buffer.write("\nHead:\n")
        buffer.write(df.head().to_string())
        result_text = buffer.getvalue()

    elif name == "get_dataframe_head":
        n = arguments.get("n", 5)
        result_text = df.head(n).to_string()

    elif name == "get_column_statistics":
        column_name = arguments.get("column_name")
        if column_name not in df.columns:
            result_text = f"Error: Column '{column_name}' not found."
        elif pd.api.types.is_numeric_dtype(df[column_name]):
            result_text = df[column_name].describe().to_string()
        else:
            result_text = f"Error: Column '{column_name}' is not a numerical type."

    elif name == "get_value_counts":
        column_name = arguments.get("column_name")
        if column_name not in df.columns:
            result_text = f"Error: Column '{column_name}' not found."
        else:
            result_text = df[column_name].value_counts().to_string()

    elif name == "run_pandas_code":
        code_to_run = arguments.get("code")
        if not code_to_run:
            return [TextContent(type="text", text="No code provided to execute.")]

        safe_globals = {
            'pd': pd,
            'np': np,
            '__builtins__': {
                'print': print, 'len': len, 'str': str, 'int': int, 'float': float,
                'list': list, 'dict': dict, 'set': set, 'tuple': tuple, 'range': range,
                'True': True, 'False': False, 'None': None
            }
        }
        safe_locals = {'df': df}
        output_buffer = StringIO()

        try:
            with redirect_stdout(output_buffer):
                exec(code_to_run, safe_globals, safe_locals)
            
            printed_output = output_buffer.getvalue()
            result_val = safe_locals.get('result')
            
            final_output = ""
            if printed_output:
                final_output += f"Output:\n{printed_output}"
            if result_val is not None:
                final_output += f"\nResult:\n{str(result_val)}"

            result_text = final_output if final_output else "Code executed successfully with no output."
        except Exception as e:
            result_text = f"Error executing code: {e}"
    
    else:
        raise ValueError(f"Unknown tool: {name}")

    return [TextContent(type="text", text=result_text)]

async def main():
    """Main entry point to run the MCP server."""
    from mcp.server.stdio import stdio_server

    logger.info("Starting Pandas MCP server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )
