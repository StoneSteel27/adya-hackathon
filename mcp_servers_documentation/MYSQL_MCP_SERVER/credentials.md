# MySQL MCP Server Credentials

To configure the MySQL MCP Server, you need to set the following environment variables. These variables provide the necessary credentials for the server to connect to your MySQL database.

## Environment Variables

-   `MYSQL_HOST`: The hostname or IP address of your MySQL server.
-   `MYSQL_PORT`: The port number for the MySQL server (defaults to `3306`).
-   `MYSQL_USER`: The username for the MySQL database.
-   `MYSQL_PASSWORD`: The password for the MySQL database.
-   `MYSQL_DATABASE`: The name of the database to connect to.

### Example

```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=test_db
```
