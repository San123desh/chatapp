from sqlmodel import create_engine, SQLModel
from config.settings import settings

engine = create_engine(settings.DATABASE_URL)
SQLModel.metadata.create_all(engine)
print("Database tables created!")

