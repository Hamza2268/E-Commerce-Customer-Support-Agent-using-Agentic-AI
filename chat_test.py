import requests
import uuid
import sys

BASE_URL = "http://127.0.0.1:8000"

def start_interactive_chat():
    # Generate a single unique session ID for this terminal instance
    session_id = str(uuid.uuid4())
    
    print("       E-Commerce Agent Terminal Interface        ")
    print(f"Session ID: {session_id}")
    print("Type 'quit', 'exit', or press CTRL+C to stop.")

    while True:
        try:
            user_message = input("\nYou: ").strip()
            
            # Handle exit commands
            if user_message.lower() in ['quit', 'exit']:
                print("Exiting chat session. Goodbye!")
                break
                
            # Skip empty messages
            if not user_message:
                continue

            # Package the JSON payload
            payload = {
                "message": user_message,
                "session_id": session_id
            }

            # POST to your local running server
            response = requests.post(f"{BASE_URL}/chat", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                agent_reply = data.get("reply", "No reply field returned.")
                print(f"Agent: {agent_reply}")
            else:
                print(f"Server Error ({response.status_code}): {response.text}")

        except KeyboardInterrupt:
            print("\nExiting chat session. Goodbye!")
            sys.exit(0)
        except requests.exceptions.ConnectionError:
            print("\nError: Could not connect to the server.")
            print("Make sure 'python main.py' is running in your other terminal window!")
            break

if __name__ == "__main__":
    start_interactive_chat()