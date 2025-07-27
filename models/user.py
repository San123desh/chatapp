from sqlmodel import SQLModel, Field
from typing import Optional
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


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: Role = Role.USER


class UserLogin(BaseModel):
    username: str
    password: str


