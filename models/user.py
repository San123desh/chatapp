from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    role: Role = Field(default=Role.USER)
    
    # Relationships
    messages: List["Message"] = Relationship(back_populates="user")
    rooms: List["Room"] = Relationship(back_populates="created_by_user")


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: Role = Role.USER


class UserLogin(BaseModel):
    username: str
    password: str


