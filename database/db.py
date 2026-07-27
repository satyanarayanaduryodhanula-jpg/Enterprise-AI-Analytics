import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load variables from .env
load_dotenv()

# Read database connection from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing. Check your .env file.")

# Create PostgreSQL connection engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)