# MCP Server Documentation Guide

This guide provides a template for creating standardized documentation for any new MCP (Multi-Cloud Platform) Server. Consistent documentation ensures that users can easily understand, configure, and use new servers.

For each new MCP server, you must create a dedicated folder within the `mcp_servers_documentation` directory. The folder should be named after your server (e.g., `NEW_SERVER_MCP`). Inside this folder, create the following three markdown files.

---

## 1. `server_features.md`

This file provides a comprehensive overview of the server. It should detail what the server does, its main features, and its technical capabilities.

**➡️ Create a file named `server_features.md` with the following content:**

```markdown
# [SERVER_NAME] MCP Server Overview

## What is the [SERVER_NAME] MCP Server?
A brief, one-paragraph description of the server's purpose and what it connects to. Explain the value it provides within the Vanij Platform.

---

## Key Features
- ✅ List the primary, user-facing features.
- ✅ Use checkmarks for clarity.
- ✅ Example: "Create and manage user accounts."
- ✅ Example: "Fetch and analyze sales data."

---

## Capabilities
Use a markdown table to list the technical capabilities or API endpoints the server exposes.

| Capability           | Description                                       |
|----------------------|---------------------------------------------------|
| Data Retrieval       | Describe what data can be retrieved.              |
| Content Management   | Detail content creation or modification abilities.|
| User Administration  | Explain user management functions.                |

---

## Supported Versions
- Specify any version requirements for the target service (e.g., "Service API v2.5+").
- Mention any other prerequisites (e.g., "Requires an Enterprise-level account").

---

## Security Notes
- Describe the authentication method used (e.g., API Keys, OAuth 2.0).
- Mention any important security considerations or required permissions.
- Note if communications must be over HTTPS.

---

## Integration Use Cases
- List potential applications for this server.
- Example: "Automating customer support ticket creation."
- Example: "Syncing product inventory with an e-commerce platform."
```

---

## 2. `credentials.md`

This file explains how to obtain the necessary credentials and shows the exact JSON format required by the server.

**➡️ Create a file named `credentials.md` with the following content:**

```markdown
# [SERVER_NAME] MCP Server Credentials

## Overview
This document provides instructions on obtaining and structuring the credentials needed to connect the [SERVER_NAME] MCP Server in the Vanij Platform.

---

## Credential Format
Provide the exact JSON structure for the credentials. Use clear and descriptive key names.

```json
{
  "[SERVER_NAME]": {
    "apiKey": "your-api-key",
    "apiSecret": "your-api-secret",
    "instanceUrl": "https://your-instance.example.com"
  }
}
```

---

## Obtaining Credentials
Provide a step-by-step guide on how to get the required credentials from the target service's user interface or admin panel.

1.  **Log in** to your [Service Name] account.
2.  Navigate to **Settings > API > Credentials**.
3.  Click **"Generate New Key"**.
4.  Copy the **API Key** and **API Secret**.
```

---

## 3. `demo_videos.md`

This file provides links to video demonstrations and includes example payloads for easy testing.

**➡️ Create a file named `demo_videos.md` with the following content:**

```markdown
# [SERVER_NAME] MCP Server – Demos and Payload Examples

## 🎥 Demo Video
- **MCP server setup explanation + API Execution + Features Testing**: [Watch Here](https://your-demo-video-link.com)

---

## 🎥 Credentials Gathering Video
- **Gathering Credentials & Setup (Full end-to-end video)**: [Watch Here](https://your-credentials-video-link.com)

---

## 🔐 Credential JSON Payload
This is the example payload for the credentials that will be used in the Client API payload.

```json
{
  "[SERVER_NAME]": {
    "apiKey": "your-api-key",
    "apiSecret": "your-api-secret",
    "instanceUrl": "https://your-instance.example.com"
  }
}
```
```