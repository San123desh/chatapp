from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlmodel import Session, select, delete
from models.message import Message
from models.user import User, Role
from models.room import Room
from dependencies.auth import get_current_user, require_role
from config.settings import settings
from sqlmodel import create_engine
import logging
import jwt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws", tags=["chat"])
engine = create_engine(settings.DATABASE_URL)
active_connections = {}

def get_db():
    with Session(engine) as session:
        yield session

@router.post("/rooms", dependencies=[Depends(require_role(Role.ADMIN))])
async def create_room(room_name: str, description: str = None, current_user: dict = Depends(get_current_user), session: Session = Depends(get_db)):
    existing_room = session.exec(select(Room).where(Room.name == room_name)).first()
    if existing_room:
        raise HTTPException(status_code=400, detail="Room already exists")
    
    user = session.exec(select(User).where(User.username == current_user["username"])).first()
    room = Room(name=room_name, description=description, created_by=user.id)
    session.add(room)
    session.commit()
    logger.info(f"Room {room_name} created by {current_user['username']}")
    return {"message": f"Room {room_name} created"}

@router.delete("/rooms/{room_name}", dependencies=[Depends(require_role(Role.ADMIN))])
async def delete_room(room_name: str, session: Session = Depends(get_db)):
    room = session.exec(select(Room).where(Room.name == room_name)).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Delete all messages in the room
    session.exec(delete(Message).where(Message.room_id == room.id))
    session.delete(room)
    session.commit()
    logger.info(f"Room {room_name} deleted by admin")
    return {"message": f"Room {room_name} deleted"}

@router.get("/messages/{room_name}")
async def get_messages(room_name: str, session: Session = Depends(get_db)):
    room = session.exec(select(Room).where(Room.name == room_name)).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Get recent messages with cursor-based pagination
    messages = session.exec(
        select(Message)
        .where(Message.room_id == room.id)
        .order_by(Message.timestamp.desc())
        .limit(50)  # Limit to 50 most recent messages
    ).all()
    
    return {"room_name": room_name, "messages": messages}

@router.websocket("/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str):
    await websocket.accept()
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008, reason="Token required")
        return
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role", Role.USER)
        if not username:
            await websocket.close(code=1008, reason="Invalid token")
            return
    except jwt.ExpiredSignatureError:
        await websocket.close(code=1008, reason="Token expired")
        return
    except jwt.JWTError:
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    with Session(engine) as session:
        room = session.exec(select(Room).where(Room.name == room_name)).first()
        if not room:
            await websocket.close(code=1008, reason="Room does not exist")
            return
        
        if room_name == "admin_room" and role != Role.ADMIN:
            logger.warning(f"Unauthorized access to admin_room by {username}")
            await websocket.close(code=1008, reason="Admin access required")
            return
        
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            await websocket.close(code=1008, reason="User not found")
            return
    
    if room_name not in active_connections:
        active_connections[room_name] = []
    active_connections[room_name].append(websocket)
    
    try:
        await broadcast_message(room_name, f"{username} joined the room")
        
        # Send recent messages to the user
        with Session(engine) as session:
            recent_messages = session.exec(
                select(Message)
                .where(Message.room_id == room.id)
                .order_by(Message.timestamp.desc())
                .limit(20)  # Send last 20 messages
            ).all()
            
            for msg in reversed(recent_messages):  # Send in chronological order
                await websocket.send_text(f"{msg.user.username}: {msg.content}")
        
        while True:
            data = await websocket.receive_text()
            message_content = data.strip()
            logger.info(f"Message from {username} in {room_name}: {message_content}")
            
            with Session(engine) as session:
                message = Message(room_id=room.id, user_id=user.id, content=message_content)
                session.add(message)
                session.commit()
            
            await broadcast_message(room_name, f"{username}: {message_content}")
    
    except WebSocketDisconnect:
        active_connections[room_name].remove(websocket)
        await broadcast_message(room_name, f"{username} left the room")
        if not active_connections[room_name]:
            del active_connections[room_name]
    
    except Exception as e:
        logger.error(f"Error in WebSocket: {e}")
        await websocket.close(code=1011)
        if websocket in active_connections.get(room_name, []):
            active_connections[room_name].remove(websocket)

async def broadcast_message(room_name: str, message: str):
    for connection in active_connections.get(room_name, []):
        await connection.send_text(message)