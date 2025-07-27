from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Message(SQLModel, table=True):
    # Primary key, auto-incremented
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Room identifier for the chat room (e.g., "room1", "room2")
    room_id: str = Field(index=True)
    
    # Foreign key linking to the User table
    user_id: int = Field(foreign_key="user.id")
    
    # Message content (text sent by the user)
    content: str
    
    # Timestamp of when the message was created
    timestamp: datetime = Field(default_factory=datetime.utcnow)