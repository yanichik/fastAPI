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

@app.get("/")
async def read_all_books(skip_book: str):
    if skip_book:
        new_books = BOOKS.copy()
        new_books.pop(skip_book)
        return new_books
    return BOOKS

@app.get("/{book_name}")
async def read_book(book_name: str):
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