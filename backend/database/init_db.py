from database.base import Base
from database.connection import engine

# Import all models here so that Base.metadata.create_all can find them
from database.models import *

def init_db():
    """Initializes the database by creating all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
