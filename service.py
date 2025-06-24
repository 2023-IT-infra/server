from datetime import datetime
from tkinter.tix import Select
from typing import Sequence, Type

from sqlmodel import Session, select

from models import Device, User, DevicePublic, DeviceCreate


def find_all_devices(session: Session) -> Sequence[Device]:
    return session.exec(select(Device)).all()

def load_test_message() -> dict[str, str]:
    return {"message": "Hello World"}

def find_user_by_email(email: str, session: Session) -> User | None:
    statement: Select= select(User).where(User.email == email)
    return session.exec(statement).first()

def find_by_device_id(device_id: int, session: Session) -> Device | None:
    return session.get(Device, device_id)

def update_device_by_id(device_id: int, device: DevicePublic, session: Session) -> Type[Device] | None:
    db_device = session.get(Device, device_id)
    if db_device is None:
        return None
    db_device.name = device.name
    db_device.mac = device.mac
    db_device.tx_power = device.tx_power
    db_device.type = device.type
    db_device.status = device.status
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device

def delete_device_by_id(device_id: int, session: Session) -> None:
    device = session.get(Device, device_id)
    session.delete(device)
    session.commit()
    return None

def create_device(device: DeviceCreate, session: Session) -> Device:
    db_device = Device(**device.dict())
    db_device.add_date = datetime.now()
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device

def update_user(user: User, session: Session) -> Type[User] | None:
    db_user = session.get(User, user.id)
    if db_user is None:
        return None
    db_user.email = user.email
    db_user.username = user.username
    db_user.disabled = user.disabled
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def update_user_password(user: User, session: Session) -> Type[User] | None:
    db_user = session.get(User, user.id)
    if db_user is None:
        return None
    db_user.hashed_password = user.hashed_password
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user