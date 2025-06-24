from datetime import datetime
from sqlalchemy.sql import Select
from typing import Sequence, Type

from util import (
    add_document_to_meilisearch,
    update_document_in_meilisearch,
    delete_document_from_meilisearch,
    get_meilisearch,
)

from sqlmodel import Session, select

from models import Device, User, DevicePublic, DeviceCreate


def find_all_devices(session: Session) -> Sequence[Device]:
    return session.exec(select(Device)).all()

def load_test_message() -> dict[str, str]:
    return {"message": "Hello World"}

async def search_devices(term: str, session: Session) -> Sequence[Device]:
    """Search devices from Meilisearch by term and return matching DB records."""
    results = await get_meilisearch(term)
    ids = [r.get("id") for r in results if "id" in r]
    if not ids:
        return []
    statement: Select = select(Device).where(Device.id.in_(ids))
    devices = session.exec(statement).all()
    # Preserve the order of the search hits
    device_map = {d.id: d for d in devices}
    return [device_map[i] for i in ids if i in device_map]

def find_user_by_email(email: str, session: Session) -> User | None:
    statement: Select = select(User).where(User.email == email)
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

    update_document_in_meilisearch(db_device.dict())

    return db_device

def delete_device_by_id(device_id: int, session: Session) -> None:
    device = session.get(Device, device_id)
    session.delete(device)
    session.commit()

    delete_document_from_meilisearch(device_id)
    return None

def create_device(device: DeviceCreate, session: Session) -> Device:
    db_device = Device(**device.dict())
    db_device.add_date = datetime.now()
    session.add(db_device)
    session.commit()
    session.refresh(db_device)

    add_document_to_meilisearch(db_device.dict())

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
