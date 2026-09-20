import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv() # load the variables from the .env file

DATABASE_URL = os.getenv("DATABASE_URL") # get the values belonging to the key DATABASE_URL from the .env file

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in the environment variables")

class Base(DeclarativeBase):
    pass

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db   # give this session to fastapi endpoints that needs it
    finally:
        db.close()

