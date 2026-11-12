import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Load env variables (useful when running locally)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./signal_clone.db")

# Render and other providers may supply PostgreSQL URLs without a driver name.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

if os.getenv("APP_ENV", "development").lower() == "production" and not DATABASE_URL.startswith("postgresql"):
    raise RuntimeError("A persistent PostgreSQL DATABASE_URL must be configured in production")

# check_same_thread: False is needed only for SQLite to allow multiple threads to access it.
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
