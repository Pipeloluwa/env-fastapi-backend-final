from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER : str = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")
POSTGRES_PORT : str = os.getenv("POSTGRES_PORT")
POSTGRES_DB : str = os.getenv("POSTGRES_DB")

POSTGRES_URL : str = os.getenv("POSTGRES_URL")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine= create_engine(DATABASE_URL, pool_pre_ping= True, pool_recycle= 300) #Pre ping filters out dead connections that were hitting my system and causinh havoc when hosted
SessionLocal= sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base= declarative_base()

def get_database():
    
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
