import sys

sys.path.append("..")
import models
from TodoApp.database import SessionLocal, engine
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .auth import get_current_user, get_user_exception, get_password_hash
from pydantic import BaseModel

router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "User not found."}}
)
models.Base.metadata.create_all(bind=engine)


class CurrentUser(BaseModel):
    username: str
    password: str


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/all")
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@router.get("/user/{username}")
async def get_user_by_username_path(username: str, db: Session = Depends(get_db)):
    user_model = (
        db.query(models.Users).filter(username == models.Users.username).first()
    )
    if user_model is not None:
        return user_model
    return "Invalid User"


@router.get("/user/")
async def get_user_by_username_query(username: str, db: Session = Depends(get_db)):
    user_model = (
        db.query(models.Users).filter(username == models.Users.username).first()
    )
    if user_model is not None:
        return user_model
    return "Invalid User"


@router.put("/")
async def update_user_password(
    new_password: str,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user is None:
        raise get_user_exception()
    user_model = (
        db.query(models.Users).filter(user["username"] == models.Users.username).first()
    )
    if user_model is None:
        raise http_exception()
    new_hashed_password = get_password_hash(new_password)
    user_model.hashed_password = new_hashed_password
    db.add(user_model)
    db.commit()
    return successful_response(200)


@router.delete("/user")
async def delete_user(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user is None:
        raise get_user_exception()
    user_model = (
        db.query(models.Users).filter(user.get("id") == models.Users.id).first()
    )
    if user_model is None:
        return "User not found"
    current_user_todos = (
        db.query(models.Todos).filter(user["id"] == models.Todos.owner_id).all()
    )
    if current_user_todos is not None:
        # for todo in current_user_todos:
        db.query(models.Todos).filter(models.Todos.owner_id == user_model.id).delete()
        # db.commit()
    db.query(models.Users).filter(user.get("id") == models.Users.id).delete()
    db.commit()
    return successful_response(200)


# Exceptions & Responses
def http_exception():
    return HTTPException(status_code=404, detail="User not found.")


def successful_response(status_code: int):
    return {"status": status_code, "transaction": "Successful."}
