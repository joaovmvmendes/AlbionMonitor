# File: imports/base/db_connections.py
"""
Reusable database connection module using SQLAlchemy.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Build the database URL
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST", "postgres")
port = os.getenv("POSTGRES_PORT", "5432")
dbname = os.getenv("POSTGRES_DB")
DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

# Create engine and session factory
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine)

def get_db_session():
    """
    Returns a new SQLAlchemy session.
    """
    return SessionLocal()