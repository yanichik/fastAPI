from fastapi import FastAPI, Depends
import models
from database import engine
from routers import auth, todos, users
from company import companyapis, dependencies

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
# this includes all of auth's routes inside the main API
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(
    companyapis.router,
    prefix="/companyapis",
    tags=["companyapis"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={418: {"description": "Internal Use Only."}},
)
app.include_router(users.router)
