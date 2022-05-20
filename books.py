from typing import Optional
from fastapi import FastAPI
from enum import Enum
BOOKS = {
    'book_1': {"title": 'title one', "author": 'author one'},
    'book_2': {"title": 'title two', "author": 'author two'},
    'book_3': {"title": 'title three', "author": 'author three'},
    'book_4': {"title": 'title four', "author": 'author four'},
    'book_5': {"title": 'title five', "author": 'author five'},
}
class DirectionName(str, Enum):
    north = 'North'
    South = 'South'
    East = 'East'
    West = 'West'

app = FastAPI()

@app.get("/all_books/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        new_books.pop(skip_book)
        return new_books
    return BOOKS

@app.post("/")
async def create_book(book_title, book_author):
    last_book_id = int(list(BOOKS.keys())[-1].split('_')[-1])
    BOOKS[f'book_{last_book_id + 1}'] = {'title': book_title, 'author': book_author}
    # return BOOKS[f'book_{last_book_id + 1}']

# path parameter
@app.get("/{book_name}")
async def get_author_from_book_name(book_name: str):
    return BOOKS[book_name]['author']

# path & query parameter
# @app.get("/{book_name}")
# async def get_book_author(book_name: str, book_title: str):
#     if BOOKS[book_name]['title'] == book_title:
#         return BOOKS[book_name]['author']
#     return "Not Found"

@app.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    BOOKS[book_name] = {'title': book_title, 'author': book_author}

# delete w/ path params
# @app.delete("/{book_name}")
# async def remove_book(book_name: str):
#     del BOOKS[book_name]

# delete w/ query params
@app.delete("/")
async def remove_book(book_name: str):
    del BOOKS[book_name]

# using path params
# @app.get("/{book_name}")
# async def read_book(book_name: str):
#     return BOOKS[book_name]

# using query params
@app.get("/book/")
async def read_book(book_name: Optional[str] = 'book_1'):
    return BOOKS[book_name]

@app.get("/books/mybook")
async def read_my_book():
    return {"book_title": "My Favorite Book"}

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return {"book_id": book_id}

@app.get("/directions/{direction_name}")
async def get_direction(direction_name:DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction": direction_name, "Subject": "up"}
    if direction_name == DirectionName.south:
        return {"Direction": direction_name, "Subject": "down"}
    if direction_name == DirectionName.east:
        return {"Direction": direction_name, "Subject": "right"}
    return {"Direction": direction_name, "Subject": "left"}