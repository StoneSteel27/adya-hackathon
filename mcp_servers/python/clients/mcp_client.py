import os
import json
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set the host for the dev-python server
dev_python_host = os.environ.get("DEV_PYTHON_HOST", "http://localhost:5001")

def load_config():
    """Loads configuration from config.json."""
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("config.json not found. Please ensure the file exists and is correctly formatted.")
        return None
    except json.JSONDecodeError:
        logging.error("Failed to decode config.json. Please check for syntax errors.")
        return None

def call_mcp_api(selected_server_credentials, client_details, selected_client, selected_servers):
    """
    Calls the MCP API with the given parameters.
    """
    url = f"{dev_python_host}/api/v1/mcp/process_message"
    headers = {"Content-Type": "application/json"}
    data = {
        "selected_server_credentials": selected_server_credentials,
        "client_details": client_details,
        "selected_client": selected_client,
        "selected_servers": selected_servers,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err} - {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"An unexpected error occurred: {req_err}")
    return None

def main():
    """
    Main function to run the MCP client.
    """
    config = load_config()
    if not config:
        return

    # Initialize chat history from config or as an empty list
    chat_history = config.get("client_details", {}).get("chat_history", [])

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # Append user message to chat history before making the API call
        chat_history.append({"role": "user", "content": user_input})
        config["client_details"]["input"] = user_input
        config["client_details"]["chat_history"] = chat_history
        config["client_details"]["prompt"] = "whenever sending sql queries to tools, send them as one single block of code"

        # Call the API
        response_data = call_mcp_api(
            config.get("selected_server_credentials", {}),
            config.get("client_details", {}),
            config.get("selected_client"),
            config.get("selected_servers"),
        )

        # Process the response
        if response_data:
            messages = response_data["Data"].get("messages", [])
            if messages:
                ai_message = messages[0]
                print(f"AI: {ai_message}")
                # Append AI response to chat history
                chat_history.append({"role": "model", "content": ai_message})
            else:
                logging.warning("No messages received from AI.")
        else:
            logging.error("Failed to get a valid response from the server.")
            # Remove the user's message from history if the call failed
            chat_history.pop()

if __name__ == "__main__":
    main()

