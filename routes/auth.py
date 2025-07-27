from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User, Role, UserCreate, UserLogin
from utils.security import hash_password, verify_password, create_access_token
from config.settings import settings
from sqlmodel import create_engine

router = APIRouter(prefix="/auth", tags=["auth"])
engine = create_engine(settings.DATABASE_URL)

@router.post("/signup")
async def signup(user: UserCreate):
    with Session(engine) as session:
        existing_user = session.exec(select(User).where((User.username == user.username) | (User.email == user.email))).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already exists")
        user_obj = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
            role=user.role
        )
        session.add(user_obj)
        session.commit()
        return {"message": "User created successfully"}

@router.post("/login")
async def login(user: UserLogin):
    with Session(engine) as session:
        user_obj = session.exec(select(User).where(User.username == user.username)).first()
        if not user_obj or not verify_password(user.password, user_obj.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"sub": user_obj.username, "role": user_obj.role})
        return {"access_token": token, "token_type": "bearer"}