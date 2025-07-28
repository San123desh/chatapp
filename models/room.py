# models/room.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Room(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)  # e.g., 'room1', 'admin_room'
    description: Optional[str] = None
    
    # Foreign key
    created_by: int = Field(foreign_key="user.id")
    
    # Relationships
    created_by_user: Optional["User"] = Relationship(back_populates="rooms")
    messages: List["Message"] = Relationship(back_populates="room")