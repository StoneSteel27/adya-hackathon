```markdown
# Pandas MCP Server Overview

## What is the Pandas MCP Server?
The Pandas MCP Server allows you to perform data analysis on a CSV file using the Pandas library. You can load a CSV file from a URL and then use various tools to inspect and analyze the data.

---

## Key Features
- ✅ Load a CSV file from a URL.
- ✅ Get a summary of the dataframe, including shape, columns, and data types.
- ✅ Get the first n rows of the dataframe.
- ✅ Get descriptive statistics for a numerical column.
- ✅ Count unique values in a column.
- ✅ Execute custom Python code with the Pandas DataFrame.

---

## Capabilities
| Capability           | Description                                       |
|----------------------|---------------------------------------------------|
| Data Loading         | Load a CSV file from a URL into a Pandas DataFrame. |
| Data Inspection      | Summarize the dataframe, get the head, and get value counts. |
| Data Analysis        | Get descriptive statistics for numerical columns. |
| Code Execution       | Execute custom Python code with the DataFrame.    |

---

## Supported Versions
- This server works with Pandas version 2.x.

---

## Security Notes
- The server executes Python code, so it should be used with caution. The code is executed in a sandboxed environment with limited libraries available.
- The `run_pandas_code` tool does not support saving files or generating plots/images.

---

## Integration Use Cases
- Performing quick data analysis on a CSV file without writing a full script.
- Integrating data analysis into a larger workflow.
- Building custom data analysis tools.
```
