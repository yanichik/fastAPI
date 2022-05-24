from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class Todos(Base):
    # defining table name
    __tablename__ = "todos"

    # columns w/in table:
    # id (primary key for todo), title, description, priority, and todo completion status
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
