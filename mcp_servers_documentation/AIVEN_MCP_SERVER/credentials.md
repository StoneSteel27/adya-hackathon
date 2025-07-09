# Aiven MCP Server Credentials

## Overview
This document provides instructions on obtaining and structuring the credentials needed to connect the Aiven MCP Server in the Vanij Platform.

---

## Credential Format
Provide the exact JSON structure for the credentials. Use clear and descriptive key names.

```json
{
  "AIVEN_BASE_URL": "https://api.aiven.io",
  "AIVEN_TOKEN": "your-aiven-api-token"
}
```

---

## Obtaining Credentials
1.  **Log in** to your [Aiven Console](https://console.aiven.io/).
2.  Navigate to **User settings** by clicking your user icon in the top right corner.
3.  Go to the **Authentication** tab.
4.  Click **"Generate new token"**.
5.  Provide a description for the token and set an expiry date.
6.  Copy the generated **API Token**.
