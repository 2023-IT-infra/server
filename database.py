from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
import os
import dotenv
from sqlmodel import Session, SQLModel

# Load the environment variables
dotenv.load_dotenv()

# Retrieve database connection details from environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DBNAME = os.getenv('DBNAME')

# Form the database URL
DB_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{HOST}:{PORT}/{DBNAME}'

engine = create_engine(
    DB_URL,
    connect_args={"connect_timeout": 10},
    pool_size=20,          # 기본 풀 크기
    max_overflow=40,       # 최대 오버플로우 수
    pool_timeout=30,       # 풀에서 커넥션을 가져오기 위해 대기하는 최대 시간(초)
    pool_recycle=1800,     # 연결을 재활용하기 전에 대기할 시간(초)
    pool_pre_ping=True     # 연결이 살아있는지 확인하기 위해 사전 핑을 활성화
)

SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
