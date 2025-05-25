from datetime import datetime

from sqlmodel import Field, Session, SQLModel, create_engine, select

class DeviceBase(SQLModel):
    mac: str = Field(max_length=17)
    tx_power: int = Field(default=0)

class Device(DeviceBase, table=True):

    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    mac: str = Field(max_length=17, nullable=False)
    tx_power: int = Field(nullable=False)
    type: str = Field(nullable=False)
    status: int = Field(nullable=False)
    add_date: datetime = Field(nullable=False)

class DevicePublic(DeviceBase):

    id: int
    name: str
    mac: str
    tx_power: int
    type: str
    status: int
    add_date: datetime

class DeviceRead(DeviceBase):

    mac: str
    tx_power: int

class DeviceCreate(DeviceBase):

    name: str
    mac: str
    tx_power: int
    type: str
    status: int

class DeviceUpdate(DeviceBase):

    name: str
    mac: str
    tx_power: int
    type: str
    status: int

class UserBase(SQLModel):

    email: str
    username: str
    disabled: int = 0
    hashed_password: str

class User(SQLModel, table=True):

    id: int = Field(primary_key=True)
    email: str = Field(max_length=100)
    username: str = Field(max_length=100)
    disabled: int = Field(default=0)
    hashed_password: str = Field(max_length=100)

class UserPublic(UserBase):

    email: str
    username: str

class UserCreate(UserBase):

    email: str
    username: str
    hashed_password: str

class UserUpdate(UserBase):

    email: str
    username: str
    disabled: int
    hashed_password: str
