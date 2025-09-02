from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file
DATABASE_URL = "sqlite:///finance_tracker.db"

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Base class for models
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Shortcut so you can import "Session" directly
Session = SessionLocal

# Function to get a new session safely
def get_session():
    """Return a new SQLAlchemy session."""
    return SessionLocal()




