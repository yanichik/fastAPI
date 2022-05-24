from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base
import models
from database import engine, SessionLocal
from pydantic import BaseModel, Field

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# create session of our DB, and we close DB regardless of if we get the session or not
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="Priority must be between 1-5")
    complete: bool

    class Config:
        schema_extra = {
            "example": {
                "title": "Some Todo",
                "description": "Todo descripton",
                "priority": 3,
                "complete": False,
            }
        }


@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise http_exception()


@app.post("/")
async def create_todo(todo: Todo, db: Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    # db.add places an object in the Session. Its state\
    # will be persisted to the database on the next\
    # flush operation. Repeated calls to add() will \
    # be ignored. The opposite of add() is expunge().
    db.add(todo_model)
    # to flush the object:
    db.commit()
    return {"status": 201, "transaction": "Successful"}


def http_exception():
    return HTTPException(status_code=404, detail="Todo item not found.")
