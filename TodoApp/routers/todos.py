import sys
from urllib.request import Request

sys.path.append("..")
from typing import Optional
from fastapi import Depends, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from database import Base
import models
from database import engine, SessionLocal
from pydantic import BaseModel, Field
from .auth import get_user_exception, get_current_user
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/todos", tags=["todos"], responses={404: {"description": "Todo not found."}}
)

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")
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


@router.get("/test")
async def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@router.get("/user")
async def read_all_by_user(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    if user is None:
        raise get_user_exception()
    return db.query(models.Todos).filter(models.Todos.owner_id == user["id"]).all()


@router.get("/{todo_id}")
async def read_todo(
    todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    if user is None:
        raise get_user_exception()
    todo_model = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .filter(models.Todos.owner_id == user["id"])
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise http_exception()


@router.post("/")
async def create_todo(
    todo: Todo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    # how does user token get passed in via auth in postman?
    if user is None:
        raise get_user_exception()
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")
    # db.add places an object in the Session. Its state\
    # will be persisted to the database on the next\
    # flush operation. Repeated calls to add() will \
    # be ignored. The opposite of add() is expunge().
    db.add(todo_model)
    # to flush the object:
    db.commit()
    return successful_response(201)


@router.put("/{todo_id}")
async def update_todo(
    todo_id: int,
    todo: Todo,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user is None:
        raise get_user_exception()
    todo_model = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .filter(models.Users.id == user["id"])
        .first()
    )
    if todo_model is None:
        raise http_exception()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    db.add(todo_model)
    db.commit()
    return successful_response(200)


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    if user is None:
        raise get_user_exception()
    todo_model = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .filter(models.Users.id == user["id"])
        .first()
    )
    if todo_model is None:
        raise http_exception()
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
    return successful_response(200)


def http_exception():
    return HTTPException(status_code=404, detail="Todo item not found.")


def successful_response(status_code: int):
    return {"status": status_code, "transaction": "Successful."}
