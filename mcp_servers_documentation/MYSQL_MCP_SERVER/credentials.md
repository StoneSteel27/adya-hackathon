# MySQL MCP Server Credentials

## Overview
This document provides instructions on obtaining and structuring the credentials needed to connect the MySQL MCP Server in the Vanij Platform.

---

## Credential Format
Provide the exact JSON structure for the credentials. Use clear and descriptive key names.

```json
{
  "host": "your-mysql-host",
  "port": 3306,
  "user": "your-mysql-user",
  "password": "your-mysql-password",
  "database": "your-mysql-database"
}
```

---

## Obtaining Credentials
You need to provide the credentials for your MySQL database. It is recommended to create a dedicated user with limited permissions for the server.

