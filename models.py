from sqlalchemy import Column, TEXT, INT, BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class address(Base):
    __tablename__ = "bluetooth"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    MAC = Column(TEXT, nullable=False)
