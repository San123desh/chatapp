from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Foreign keys
    user_id: int = Field(foreign_key="user.id")
    room_id: int = Field(foreign_key="room.id")
    
    # Relationships
    user: Optional["User"] = Relationship(back_populates="messages")
    room: Optional["Room"] = Relationship(back_populates="messages")