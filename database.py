from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import dotenv

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

engine = create_engine(DB_URL, connect_args={"connect_timeout": 10}, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
