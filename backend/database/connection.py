import os
from sqlalchemy import create_engine

# Use SQLite by default. 
# Changing this URL to a postgresql:// string will automatically migrate the system to Postgres.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./diagnostics.db")

engine = create_engine(
    DATABASE_URL, 
    # check_same_thread=False is needed for SQLite when used with FastAPI
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
