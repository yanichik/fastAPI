from fastapi import FastAPI
from enum import Enum
BOOKS = {
    'book_1': {"title": 'title one', "author": 'author one'},
    'book_2': {"title": 'title one', "author": 'author one'},
    'book_3': {"title": 'title one', "author": 'author one'},
    'book_4': {"title": 'title one', "author": 'author one'},
    'book_5': {"title": 'title one', "author": 'author one'},
}
class DirectionName(str, Enum):
    north = 'North'
    north = 'South'
    north = 'East'
    north = 'West'

app = FastAPI()

@app.get("/")
async def read_all_books():
    return BOOKS

@app.get("/books/mybook")
async def read_book():
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