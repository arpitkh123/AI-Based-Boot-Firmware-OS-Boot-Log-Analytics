from sqlalchemy.orm import sessionmaker
from database.connection import engine

# Create the SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency for FastAPI routes to inject database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
