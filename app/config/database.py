# database.py

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database configuration
Base = declarative_base()

# Get the database URL from the .env file
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create an engine that establishes a connection to the specified database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal is a factory for producing instances of the Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency that provides a SQLAlchemy session.

    This function yields a database session from the SessionLocal factory,
    ensuring that resources are properly managed. It's used in route handlers
    to interact with the database.

    Yields:
        Session: An instance of SQLAlchemy Session for database operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
