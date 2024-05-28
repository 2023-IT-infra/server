from typing import Union
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import address
from middleware import DBSessionMiddleware

app = FastAPI()
app.add_middleware(DBSessionMiddleware)


# 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "MAC Address Server"}

@app.get("/devices")
async def get_device(db: Session = Depends(get_db)):
    devices = db.query(address).all()
    return devices