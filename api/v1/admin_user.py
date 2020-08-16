import logging
from typing import Any, List

from fastapi import APIRouter

from crud import user as crud
from crud.license import find_one as find_license
from utils.utils import raise_not_found, raise_bad_request
from models.user import User, UserCreate, UserUpdate


router = APIRouter()


@router.get("", response_model=List[User])
async def read_users(license: str = "all", limit: int=20, skip: int=0):
    '''
    License: `all` or license's `slug`.
    '''
    logging.info(">>> " + __name__ + ":get")
    return await crud.find_many(license, limit, skip)


@router.post("", response_model=User)
async def create_license_owner(data: UserCreate):
    '''
    Required: `license, name, username, email, password`
    '''
    logging.info(">>> " + __name__ + ":create")
    license = await find_license(data.license)
    if not license:
        raise_bad_request("Could not find license with the specified slug")

    user = await crud.find_license_owner(data.license)
    if user:
        raise_bad_request("License owner user already exists in the system.")

    user = await crud.find_one_by_email_or_username(data.email, data.username)
    if user:
        raise_bad_request('Email or username is already registered in the system.')

    return await crud.insert_license_owner(data)


@router.get("/{search}", response_model=User)
async def find_user(search: str):
    '''
    Search: `id`, `username`, or `email`.
    '''
    logging.info(">>> " + __name__ + ":find")
    user = await crud.find_one(term=search)
    if not user:
        raise_not_found("User not found.")
    return user


@router.put("/{search}", response_model=User)
async def update_user(search: str, data: UserUpdate):
    '''
    Required: `search`, `body`<br>
    Search: `id`, `username`, or `email`.
    '''
    logging.info(">>> " + __name__ + ":update")
    user = await crud.find_one(search)
    if not user:
        raise_not_found("User not found.")
    return await crud.update_one(search, data)


@router.delete("/{search}", summary="Delete user", response_model=Any)
async def delete(search: str):
    '''
    Search: `id`, `username`, or `email`.
    '''
    logging.info(">>> " + __name__ + ":find")
    user = await crud.find_one(search)
    if not user:
        raise_not_found("User not found.")
    if user['licenseOwner']:
        raise_bad_request("Could not delete license owner.")
    return await crud.delete(search)
