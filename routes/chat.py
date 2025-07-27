from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlmodel import Session, select
from models.message import Message
from models.user import User, Role
from dependencies.auth import get_current_user
from config.settings import settings
from sqlmodel import create_engine
from utils.security import create_access_token
import json
import jwt

router = APIRouter(prefix="/ws", tags=["chat"])
engine = create_engine(settings.DATABASE_URL)

# Store active WebSocket connections per room
active_connections = {}

@router.websocket("/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    # Accept the WebSocket connection
    await websocket.accept()
    
    # Get token from query parameters
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008, reason="Token required")
        return
    
    # Verify the token
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if not username:
            await websocket.close(code=1008, reason="Invalid token")
            return
    except jwt.ExpiredSignatureError:
        await websocket.close(code=1008, reason="Token expired")
        return
    except jwt.JWTError:
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    # Initialize room connections if not exists
    if room_id not in active_connections:
        active_connections[room_id] = []
    
    # Add the current WebSocket to the room's connections
    active_connections[room_id].append(websocket)
    
    try:
        # Look up the user in the database to get their ID
        with Session(engine) as session:
            user = session.exec(select(User).where(User.username == username)).first()
            if not user:
                await websocket.close(code=1008)  # Policy violation: user not found
                return
        
        # Notify room of user joining
        await broadcast_message(room_id, f"{username} joined the room")
        
        while True:
            # Receive message from the client
            data = await websocket.receive_text()
            message_content = data.strip()
            
            # Save the message to the database
            with Session(engine) as session:
                message = Message(room_id=room_id, user_id=user.id, content=message_content)
                session.add(message)
                session.commit()
            
            # Broadcast the message to all clients in the room
            await broadcast_message(room_id, f"{username}: {message_content}")
    
    except WebSocketDisconnect:
        # Remove the WebSocket from the room's connections
        active_connections[room_id].remove(websocket)
        
        # Notify room of user leaving
        await broadcast_message(room_id, f"{username} left the room")
        
        # Clean up empty rooms
        if not active_connections[room_id]:
            del active_connections[room_id]
    
    except Exception as e:
        # Handle unexpected errors
        await websocket.close(code=1011)  # Internal error
        if websocket in active_connections.get(room_id, []):
            active_connections[room_id].remove(websocket)

async def broadcast_message(room_id: str, message: str):
    # Send message to all active WebSocket connections in the room
    for connection in active_connections.get(room_id, []):
        await connection.send_text(message)


# Commented out this endpoint as it's not needed for basic WebSocket chat
# @router.get("/messages/{room_id}")
# async def get_messages(room_id: str, session: Session = Depends(get_db)):
#     messages = session.exec(select(Message).where(Message.room_id == room_id)).all()
#     return messages