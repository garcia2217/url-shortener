import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

# NOTE: 1. Engine is the core interface to the database, managing connections and executing SQL.
# NOTE: 2. SessionLocal is a factory for creating new sessions (connections) to the database.

# oad the variables from the .env file
load_dotenv()

# Get the variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# In production, this would come from an .env file
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# The engine is the "starting point" for SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# A factory for creating database sessions
SessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base class for our models
class Base(DeclarativeBase):
    pass

# Dependency to get DB session in FastAPI routes
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session