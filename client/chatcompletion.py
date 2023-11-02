import requests
import json
from datetime import datetime

SERVER_ENDPOINT = "http://127.0.0.1:5000/api/chat"

# Initialize a session object to store the conversation history
session = requests.Session()
conversation = []  # Local storage for the conversation
user_name = "User123"  # Hardcoded user name for this example

def chat():
    print("-" * 40)  # Print the separator before the conversation starts
    try:
        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nExiting the conversation. Goodbye!")
                break

            # Append the user's input to the local conversation history
            conversation.append({"role": "user", "content": user_input})

            try:
                # Send the user's input to the server, including the hardcoded user name
                response = session.post(SERVER_ENDPOINT, json={"input": user_input, "user_name": user_name}, timeout=10)
                response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
                
                chatbot_response = response.json()["response"]
                # Append the assistant's response to the local conversation history
                conversation.append({"role": "assistant", "content": chatbot_response})
                
                print("-" * 40)  # Separator after user input
                print("Streamy:", chatbot_response)
                print("-" * 40)  # Separator after Streamy's response

            except requests.exceptions.HTTPError as http_err:
                # Handle HTTP errors
                print(f"HTTP error occurred: {http_err}")
            except requests.exceptions.ConnectionError:
                # Handle errors like the server being down
                print("Error: Could not connect to the server. Please check if the server is running.")
            except requests.exceptions.Timeout:
                # Handle the server taking too long to respond
                print("Timeout error: The server is taking too long to respond. Please try again later.")
            except requests.exceptions.RequestException as e:
                # Handle any other requests exceptions
                print(f"An error occurred: {e}")

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nConversation interrupted by user.")

    finally:
        # Save the conversation when the chat ends or is interrupted
        save_conversation()

def save_conversation():
    # Save conversation to local file
    filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_conversation_{user_name}.json"
    with open(filename, "w") as json_file:
        json.dump(conversation, json_file, indent=4)
        print(f"Conversation saved locally to {filename}")

    try:
        # Request the server to save the conversation, including the hardcoded user name
        response = session.post("http://127.0.0.1:5000/api/chat/end", json={"conversation": conversation, "user_name": user_name}, timeout=10)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        print("Conversation saved on the server side.")
    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        # Handle errors like the server being down
        print("Error: Could not connect to the server. Please check if the server is running.")
    except requests.exceptions.Timeout:
        # Handle the server taking too long to respond
        print("Timeout error: The server is taking too long to respond. Please try again later.")
    except requests.exceptions.RequestException as e:
        # Handle any other requests exceptions
        print(f"Failed to save conversation on the server side.\nError: {e}")

if __name__ == "__main__":
    chat()
