from urllib.request import Request
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: Optional[str] = Field(
        title="Description of Book", min_length=1, max_length=50
    )
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "04c0f3b6-072b-4df8-af23-40ba21604742",
                "title": "Some Sample Title",
                "author": "Sample Author",
                "description": "Sample description",
                "rating": 80,
            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: Optional[str] = Field(
        None, title="Description of Book", min_length=1, max_length=50
    )


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(
    request: Request, exception: NegativeNumberException
):
    print(0)
    return JSONResponse(
        status_code=418,
        content={
            "message": f"Hey, why do you want {exception.books_to_return} books? You need to read more!"
        },
    )


@app.post("/books/login")
async def book_login(
    book_id: UUID,
    username: Optional[str] = Header(None),
    password: Optional[str] = Header(None),
):
    if username == "FastAPIUser" and password == "test1234":
        for book in BOOKS:
            if book.id == book_id:
                return book
    return "Invalid User"


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header}


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return)
    if len(BOOKS) < 1:
        create_books_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        books_returned = []
        for i in range(books_to_return):
            books_returned.append(BOOKS[i])
        return books_returned
    return BOOKS


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    for ind, bk in enumerate(BOOKS):
        if bk.id == book_id:
            BOOKS[ind] = book
    raise_not_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    for ind, bk in enumerate(BOOKS):
        print(ind)
        print(BOOKS[ind])
        if bk.id == book_id:
            popped = BOOKS.pop(ind)
            return popped
    raise_not_found_exception()


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise_not_found_exception()


@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise_not_found_exception()


def create_books_no_api():
    book_1 = Book(
        id="14c0f3b6-072b-4df8-af23-40ba21604742",
        title="Title 1",
        author="Author 1",
        description="Descriptino 1",
        rating=50,
    )
    book_2 = Book(
        id="24c0f3b6-072b-4df8-af23-40ba21604742",
        title="Title 2",
        author="Author 2",
        description="Descriptino 2",
        rating=60,
    )
    book_3 = Book(
        id="34c0f3b6-072b-4df8-af23-40ba21604742",
        title="Title 3",
        author="Author 3",
        description="Descriptino 3",
        rating=70,
    )
    book_4 = Book(
        id="44c0f3b6-072b-4df8-af23-40ba21604742",
        title="Title 4",
        author="Author 4",
        description="Descriptino 4",
        rating=80,
    )
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
    # print(BOOKS)


def raise_not_found_exception():
    raise HTTPException(
        status_code=404,
        detail="Book Not Found.",
        headers={"X-Header-Error": "UUID not found."},
    )