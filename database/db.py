import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine

# Find project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load project .env file
load_dotenv(BASE_DIR / ".env", override=True)

# Get DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is missing. Check the .env file."
    )

# Create database engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

print("Database configuration loaded successfully")