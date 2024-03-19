from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import dotenv

# Load the environment variables
dotenv.load_dotenv()

# Retrieve database connection details from environment variables
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DBNAME = os.getenv('DBNAME')


# Form the database URL
DB_URL = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'

print(DB_URL)

class engineconn:

    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle=500)

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def create_connection(self):
        conn = self.engine.connect()
        return conn