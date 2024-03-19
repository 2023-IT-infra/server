from typing import Union
from fastapi import FastAPI, Depends, Path, HTTPException
from pydantic import BaseModel
from database import engineconn
from models import address

app = FastAPI()

engine = engineconn()
session = engine.create_session()


class Item(BaseModel):
    MAC: str


@app.get("/")
async def first_get():
    return session.query(address).all()


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
