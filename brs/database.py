from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from constants import DB_HOST, DB_SCHEMA, DB_PASSWORD, DB_USERNAME

SQLALCHEMY_DATABASE_URL = str("postgresql://" + DB_USERNAME + ":" +
                              DB_PASSWORD + "@" + DB_HOST + "/" + DB_SCHEMA)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base class for models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
