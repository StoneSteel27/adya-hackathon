# Discord MCP Server Credentials

## Overview
This document provides instructions on obtaining and structuring the credentials needed to connect the Discord MCP Server in the Vanij Platform.

---

## Credential Format
Provide the exact JSON structure for the credentials. Use clear and descriptive key names.

```json
{
  "api_key": "your-discord-bot-token",
  "guild_id": "your-discord-server-id"
}
```

---

## Obtaining Credentials
### Bot Token
1.  Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2.  Click **"New Application"**.
3.  Give your application a name and click **"Create"**.
4.  Go to the **"Bot"** tab and click **"Add Bot"**.
5.  Click **"Reset Token"** to generate a new token. Copy this token.

### Guild ID
1.  Open your Discord client.
2.  Go to **User Settings > Advanced**.
3.  Enable **Developer Mode**.
4.  Right-click on your server icon and click **"Copy Server ID"**.
