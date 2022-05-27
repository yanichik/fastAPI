from enum import auto
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# for sqlite3 only
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# for postgresql
SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:test1234@localhost/TodoApplicationDatabase"
)

engine = create_engine(
    # for sqlite3
    # SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False}
    # for postgresql
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
