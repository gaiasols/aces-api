import logging
from typing import Any, List

from fastapi import APIRouter, Depends

from crud import user as crud
from crud.license import find_one as find_license
from models.base import Msg
from models.user import User, UserCreate, UserUpdate
from utils.utils import raise_bad_request, raise_not_found
from api.v1.login import get_current_active_user


router = APIRouter()


@router.get("", response_model=List[User])
async def read_license_users(limit: int=20, skip: int=0, current_user: User=Depends(get_current_active_user)):
    logging.info(">>> " + __name__ + ":get")
    license = current_user.license
    return await crud.find_many(license, limit, skip)


@router.post("", response_model=User)
async def create_license_user(data: UserCreate, current_user: User=Depends(get_current_active_user)):
    logging.info(">>> " + __name__ + ":create")
    license = current_user.license
    data.license = license
    logging.info(data)
    user = await crud.find_by_email_or_username(data.email, data.username)
    if user:
        raise_bad_request("Username or email is already registered in the system.")
    return await crud.insert_one(data, license_owner=False)


@router.get("/{search}", response_model=User)
async def find_license_user(search: str, current_user: User=Depends(get_current_active_user)):
    logging.info(">>> " + __name__ + ":find")
    license = current_user.license
    user = await crud.find_license_user(license, search)
    if not user:
        raise_not_found("User not found.")
    return user


@router.put("/{search}", response_model=User)
async def update_license_user(search: str, data: UserUpdate, current_user: User=Depends(get_current_active_user)):
    logging.info(">>> " + __name__ + ":update")
    license = current_user.license
    user = await crud.find_license_user(license, search)
    if not user:
        raise_not_found("User not found.")
    return await crud.update_one(search, data)


@router.delete("/{search}", response_model=Msg)
async def delete_license_user(search: str, current_user: User=Depends(get_current_active_user)):
    logging.info(">>> " + __name__ + ":find")
    license = current_user.license
    user = await crud.find_license_user(license, search)
    if not user:
        raise_not_found("User not found.")
    if user['licenseOwner']:
        raise_bad_request("Could not delete license owner.")
    return await crud.delete(search)
