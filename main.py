# from fastapi import FastAPI
# from sqlmodel import create_engine, SQLModel
# from config.settings import settings
# from routes.auth import router as auth_router
# from routes.chat import router as chat_router

# # Initialize FastAPI app
# app = FastAPI()

# # Create database engine and initialize tables
# engine = create_engine(settings.DATABASE_URL)
# SQLModel.metadata.create_all(engine)

# # Include authentication and chat routers
# app.include_router(auth_router)
# app.include_router(chat_router)

# # Root endpoint for health check
# @app.get("/")
# async def root():
#     return {"message": "Chat App is running!"}



# main.py
from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel
from config.settings import settings

# Import all models to register them with SQLModel
import models

from routes import auth, chat

app = FastAPI()
app.include_router(auth.router)
app.include_router(chat.router)

engine = create_engine(settings.DATABASE_URL)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"message": "Chat App is running!"}