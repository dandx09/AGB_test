import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    global engine
    Base.metadata.create_all(engine)


def get_db():
    with SessionLocal() as session:
        yield session