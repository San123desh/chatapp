# test_ws.py
import asyncio
import websockets
import json

async def test_chat(token, room_id):
    # WebSocket URL for the chat endpoint with token as query parameter
    uri = f"ws://localhost:8000/ws/{room_id}?token={token}"
    
    try:
        # Connect to the WebSocket with minimal parameters for compatibility
        async with websockets.connect(uri, ping_interval=None, ping_timeout=None) as ws:
            print(f"Connected to {room_id}")
            
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


user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyYW5kb20iLCJyb2xlIjoidXNlciIsImV4cCI6MTc1MzU5ODIxNX0.I_REhMMcetGK4Tu_N-XWPESzkyQmt7XraZZEU-Wih-Q"

# Run the test for a regular room
asyncio.run(test_chat(user_token, "room1")) 







