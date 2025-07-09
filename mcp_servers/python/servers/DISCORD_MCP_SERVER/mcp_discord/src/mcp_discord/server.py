import asyncio
import logging
import discord
from mcp.server import Server
from mcp.types import Tool, TextContent
from . import utils

# Logging configuration
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add a file handler to save logs to a file
file_handler = logging.FileHandler('discord_mcp_server.log')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# Optional: Add a stream handler to also print logs to the console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

# Initialize the MCP Server with a unique name
app = Server("mcp-discord")

# Helper function to get the Discord client
def get_discord_client(token: str) -> discord.Client:
    intents = discord.Intents.default()
    intents.members = True
    intents.guilds = True
    intents.messages = True
    intents.message_content = True
    client = discord.Client(intents=intents)
    return client

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Discord tools."""
    logger.info("Listing tools...")
    return [
        Tool(
            name="create_text_channel",
            description="Create a new text channel in the server.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the new text channel."
                    },
                    "category_name": {
                        "type": "string",
                        "description": "Optional: The name of the category to create the channel in."
                    },
                    "visible_to_roles": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional: List of role names that can see this channel. If empty, defaults to @everyone."
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="create_category",
            description="Create a new category.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the new category."
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="move_channel",
            description="Move a channel to a different category.",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel_name": {
                        "type": "string",
                        "description": "The name of the channel to move."
                    },
                    "new_category_name": {
                        "type": "string",
                        "description": "The name of the destination category."
                    }
                },
                "required": ["channel_name", "new_category_name"]
            }
        ),
        Tool(
            name="delete_channel",
            description="Delete a channel or category.",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel_name": {
                        "type": "string",
                        "description": "The name of the channel or category to delete."
                    }
                },
                "required": ["channel_name"]
            }
        ),
        Tool(
            name="create_role",
            description="Create a new role.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the new role."
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="give_role_to_member",
            description="Assign a role to a member.",
            inputSchema={
                "type": "object",
                "properties": {
                    "member_name": {
                        "type": "string",
                        "description": "The name or nickname of the member."
                    },
                    "role_name": {
                        "type": "string",
                        "description": "The name of the role to assign."
                    }
                },
                "required": ["member_name", "role_name"]
            }
        ),
        Tool(
            name="remove_role_from_member",
            description="Remove a role from a member.",
            inputSchema={
                "type": "object",
                "properties": {
                    "member_name": {
                        "type": "string",
                        "description": "The name or nickname of the member."
                    },
                    "role_name": {
                        "type": "string",
                        "description": "The name of the role to remove."
                    }
                },
                "required": ["member_name", "role_name"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute Discord tools."""
    logger.info(f"Executing tool: {name} with arguments: {arguments}")
    client = None  # Initialize client to None
    try:
        if "__credentials__" not in arguments:
            raise ValueError("Missing credentials")

        credentials = arguments.pop("__credentials__")
        api_key = credentials.get("api_key")
        guild_id_str = credentials.get("guild_id")

        if not api_key or not guild_id_str:
            raise ValueError("API key and guild ID are required in credentials.")

        try:
            guild_id = int(guild_id_str)
        except (ValueError, TypeError):
            raise ValueError("Guild ID must be a valid integer.")

        client = get_discord_client(api_key)
        await client.login(api_key)

        guild = await client.fetch_guild(guild_id)
        if not guild:
            raise ValueError(f"Could not find a guild with ID: {guild_id}. Ensure the bot is in the server and the ID is correct.")

        # Fetch all channels, roles, and members directly from the guild
        all_channels = await guild.fetch_channels()
        all_roles = await guild.fetch_roles()
        all_members = [member async for member in guild.fetch_members(limit=None)]
        
        # Manually filter channels by type
        text_channels = [c for c in all_channels if isinstance(c, discord.TextChannel)]
        voice_channels = [c for c in all_channels if isinstance(c, discord.VoiceChannel)]
        categories = [c for c in all_channels if isinstance(c, discord.CategoryChannel)]

        # Get the bot's own member object to ensure it doesn't lock itself out
        bot_member = guild.me

        logger.info(f"Fetched {len(all_channels)} channels, {len(all_roles)} roles, and {len(all_members)} members from guild '{guild.name}'.")

        if name == "create_text_channel":
            channel_name = arguments["name"]
            category_name = arguments.get("category_name")
            visible_to_roles = arguments.get("visible_to_roles", [])

            category = None
            if category_name:
                category = utils.get_category_by_name(category_name, categories)
                if not category:
                    raise ValueError(f"Category '{category_name}' not found.")

            new_channel = await guild.create_text_channel(name=channel_name, category=category)
            if not new_channel:
                raise RuntimeError(f"Failed to create text channel '{channel_name}'. This may be due to a permission issue.")
            result_text = f"Successfully created text channel '{new_channel.name}' with ID {new_channel.id}."

        elif name == "create_category":
            category_name = arguments["name"]
            new_category = await guild.create_category(name=category_name)
            if not new_category:
                raise RuntimeError(f"Failed to create category '{category_name}'. This may be due to a permission issue.")
            result_text = f"Successfully created category '{new_category.name}' with ID {new_category.id}."

        elif name == "move_channel":
            channel_name = arguments["channel_name"]
            new_category_name = arguments["new_category_name"]
            
            searchable_channels = text_channels + voice_channels
            channel = utils.get_channel_by_name(channel_name, searchable_channels)
            if not channel:
                raise ValueError(f"Channel '{channel_name}' not found.")

            new_category = utils.get_category_by_name(new_category_name, categories)
            if not new_category:
                raise ValueError(f"Category '{new_category_name}' not found.")

            await channel.edit(category=new_category)
            result_text = f"Successfully moved channel '{channel.name}' to category '{new_category.name}'."

        elif name == "delete_channel":
            channel_name = arguments["channel_name"]
            searchable_channels = text_channels + voice_channels + categories
            
            channel_names_to_log = [c.name for c in searchable_channels]
            logger.info(f"Searching for channel '{channel_name}' within the following channels: {channel_names_to_log}")

            channel = utils.get_channel_by_name(channel_name, searchable_channels)
            if not channel:
                raise ValueError(f"Channel or category '{channel_name}' not found.")
            
            await channel.delete()
            result_text = f"Successfully deleted '{channel.name}'."

        elif name == "create_role":
            role_name = arguments["name"]
            new_role = await guild.create_role(name=role_name)
            if not new_role:
                raise RuntimeError(f"Failed to create role '{role_name}'. This may be due to a permission issue.")
            result_text = f"Successfully created role '{new_role.name}' with ID {new_role.id}."

        elif name == "give_role_to_member":
            member_name = arguments["member_name"]
            role_name = arguments["role_name"]

            member = utils.get_member_by_name(member_name, all_members)
            if not member:
                raise ValueError(f"Member '{member_name}' not found.")

            role = utils.get_role_by_name(role_name, all_roles)
            if not role:
                raise ValueError(f"Role '{role_name}' not found.")

            await member.add_roles(role)
            result_text = f"Successfully gave role '{role.name}' to member '{member.display_name}'."

        elif name == "remove_role_from_member":
            member_name = arguments["member_name"]
            role_name = arguments["role_name"]

            member = utils.get_member_by_name(member_name, all_members)
            if not member:
                raise ValueError(f"Member '{member_name}' not found.")

            role = utils.get_role_by_name(role_name, all_roles)
            if not role:
                raise ValueError(f"Role '{role_name}' not found.")

            await member.remove_roles(role)
            result_text = f"Successfully removed role '{role.name}' from member '{member.display_name}'."

        else:
            raise ValueError(f"Unknown tool: {name}")

    except discord.Forbidden:
        result_text = f"Error: The bot does not have the required permissions to perform the action '{name}'."
    except ValueError as ve:
        result_text = f"Error: {ve}"
    except Exception as e:
        result_text = f"An unexpected error occurred: {e}"
    finally:
        if client and not client.is_closed():
            await client.close()

    return [TextContent(type="text", text=result_text)]

async def main():
    """Main entry point to run the MCP server."""
    from mcp.server.stdio import stdio_server

    logger.info("Starting Discord MCP server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )
