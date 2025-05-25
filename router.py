from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

import service
from auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_active_user, \
    verify_password, get_password_hash
from database import SessionDep, get_session
from models import User, UserPublic, DevicePublic, DeviceRead, DeviceUpdate, DeviceCreate
from schemas import Token, PasswordChange
from service import find_all_devices, load_test_message, find_by_device_id
from util import add_document_to_meilisearch

api_router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
)

auth_router = APIRouter()

v0_router = APIRouter()

@v0_router.get("/devices")
async def get_device(
    session: Annotated[SessionDep, Depends(get_session)]
):
    return [ {"id": d.id, "MAC": d.mac, "txPower": d.tx_power}
             for d in filter(lambda device: device.status, find_all_devices(session))
            ]

@api_router.get("/user/devices",response_model=list[DevicePublic])
async def get_device(
    current_user: Annotated[
        User,
        Depends(
            get_current_active_user
        )],
    session: Annotated[SessionDep, Depends(get_session)]
):
    return find_all_devices(session)

@api_router.get("/user/devices/{device_id}",response_model=DevicePublic)
async def get_device(
    device_id: int,
    current_user: Annotated[
        User,
        Depends(
            get_current_active_user
        )],
    session: Annotated[SessionDep, Depends(get_session)]
):
    return find_by_device_id(device_id, session)

@api_router.put("/user/devices/{device_id}",response_model=DevicePublic)
async def update_device(
    device_id: int,
    res: DeviceUpdate,
    current_user: Annotated[
        User,
        Depends(
            get_current_active_user
        )],
    session: Annotated[SessionDep, Depends(get_session)],
    background_tasks: BackgroundTasks
):
    result = service.update_device_by_id(device_id, res, session)
    background_tasks.add_task(add_document_to_meilisearch, result)
    return result

@api_router.post("/user/devices",response_model=DevicePublic)
async def create_device(
    res: DeviceCreate,
    current_user: Annotated[
        User,
        Depends(
            get_current_active_user
        )],
    session: Annotated[SessionDep, Depends(get_session)]
):
    return service.create_device(res, session)

@api_router.delete("/user/devices/{device_id}")
async def delete_device(
    device_id: int,
    current_user: Annotated[
        User,
        Depends(
            get_current_active_user
        )],
    session: Annotated[SessionDep, Depends(get_session)]
):
    return service.delete_device_by_id(device_id, session)

@api_router.get("/test")
async def test() -> dict:
    return load_test_message()

@api_router.get("/user/me", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[
        User,
        Depends(
            get_current_active_user
        )]
):
    return current_user

@api_router.put("/user/me", response_model=UserPublic)
async def update_user_me(
    current_user: Annotated[
        User,
        Depends(
            get_current_active_user
        )],
    session: Annotated[SessionDep, Depends(get_session)]
):
    return service.update_user_password(current_user, session)

@api_router.put("/user/me/change-password", response_model=UserPublic)
async def change_password(
    res: PasswordChange,
    current_user: Annotated[
        User,
        Depends(
            get_current_active_user
        )],
    session: Annotated[SessionDep, Depends(get_session)]
):
    if not verify_password(res.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )
    current_user.hashed_password = get_password_hash(res.new_password)
    return service.update_user(current_user, session)

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[
    OAuth2PasswordRequestForm,
    Depends()],
    session: Annotated[ SessionDep, Depends(get_session)]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
