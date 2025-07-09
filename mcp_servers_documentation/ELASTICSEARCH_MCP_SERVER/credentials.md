# Elasticsearch MCP Server Credentials

## Overview
This document provides instructions on obtaining and structuring the credentials needed to connect the Elasticsearch MCP Server in the Vanij Platform.

---

## Credential Format
Provide the exact JSON structure for the credentials. Use clear and descriptive key names.

```json
{
  "ES_URL": "your-elasticsearch-url",
  "ES_API_KEY": "your-elasticsearch-api-key",
  "ELASTICSEARCH_VERIFY_CERTS": true
}
```

---

## Obtaining Credentials
1.  **Log in** to your Kibana instance.
2.  Go to **Stack Management > API Keys**.
3.  Click **"Create API key"**.
4.  Give your API key a name and assign it the appropriate roles.
5.  Copy the generated **API Key**.
6.  The **Elasticsearch URL** is the URL of your Elasticsearch cluster.
7.  `ELASTICSEARCH_VERIFY_CERTS` is an optional boolean to specify whether to verify SSL certificates. It defaults to `true`.
