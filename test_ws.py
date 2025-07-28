# test_ws.py
import asyncio
import websockets
import json

async def test_chat(token, room_name):
    # WebSocket URL for the chat endpoint with token as query parameter
    uri = f"ws://localhost:8000/ws/{room_name}?token={token}"
    
    try:
        # Connect to the WebSocket with minimal parameters for compatibility
        async with websockets.connect(uri, ping_interval=None, ping_timeout=None) as ws:
            print(f"Connected to {room_name}")
            
            # Send a test message
            await ws.send("Hello, room!")
            
            # Listen for incoming messages
            while True:
                message = await ws.recv()
                print(f"Received: {message}")
                
    except websockets.exceptions.ConnectionClosedError as e:
        # Handle connection closure (e.g., authentication failure)
        print(f"Connection closed: {e.code} - {e.reason}")
    except Exception as e:
        # Handle other errors (e.g., timeout, network issues)
        print(f"Error: {str(e)}")

# Use the fresh token from the generate_tokens.py script
user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsInJvbGUiOiJ1c2VyIiwiZXhwIjoxNzUzNjgzNDAyfQ.wH_eOk33lcQ1sQXP1ceIBkmzCjg7d1w9O2MaAzu5QDE"

# Run the test for a regular room
asyncio.run(test_chat(user_token, "general")) 


# Token for admin:
# "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc1MzY4MzQwNn0.HY9XfNY8Jf1oh3IqjCQdaZ45QVMOKyGRONMFGM_e_mQ