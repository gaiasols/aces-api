import logging
from typing import Any, List

from fastapi import APIRouter, Depends

from api.v1.login import get_current_active_user
from crud import client as crud
from crud.license import find_one as find_license
from models.base import Msg
from models.client import Client, ClientCreate, ClientUpdate
from models.user import User
from utils.utils import raise_bad_request, raise_not_found


router = APIRouter()


@router.get("", response_model=List[Client])
async def read_clients(slug: str, limit: int=20, skip: int=0, current_user: User = Depends(get_current_active_user)):
    '''slug: license's slug or * (all)'''
    logging.info(">>> " + __name__ + ":read_clients")
    return await crud.find_many(slug, limit, skip)


@router.post("", response_model=Client)
async def create_client(slug: str, data: ClientCreate, current_user: User = Depends(get_current_active_user)):
    logging.info(">>> " + __name__ + ":create_client")
    slug = slug.strip().lower()
    found = await find_license(slug)
    if not found:
        raise_bad_request("License is not valid.")
    return await crud.insert(slug, data)


@router.get("/{id}", response_model=Client)
async def find_client(slug: str, id: str, current_user: User = Depends(get_current_active_user)):
    '''slug: license's slug or * (all)'''
    logging.info(">>> " + __name__ + ":find_client")
    slug = slug.strip().lower()
    id = id.strip().lower()
    found = await find_license(slug)
    if not found:
        raise_bad_request("License is not valid.")
    client = await crud.find_one(slug, id)
    if client:
        return client
    raise_not_found("Not found.")


@router.put("/{id}", response_model=Client)
async def update_client(slug: str, id: str, data: ClientUpdate, current_user: User = Depends(get_current_active_user)):
    logging.info(">>> " + __name__ + ":update_client")
    slug = slug.strip().lower()
    id = id.strip().lower()
    client = await crud.find_one(slug, id)
    if not client:
        raise_not_found("Client not found.")
    return await crud.update(slug, id, data)


@router.delete("/{id}", response_model=Msg)
async def delete_client(slug: str, id: str, current_user: User = Depends(get_current_active_user)):
    logging.info(">>> " + __name__ + ":delete_client")
    slug = slug.strip().lower()
    id = id.strip().lower()
    client = await crud.find_one(slug, id)
    if not client:
        raise_not_found("Client not found.")
    return await crud.delete(slug, id)
