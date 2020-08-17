import logging
from typing import Any, List

from fastapi import APIRouter

from crud import client as crud
from crud.license import find_one as find_license
from models.base import Msg
from models.client import Client, ClientCreate, ClientUpdate
from utils.utils import raise_bad_request, raise_not_found


router = APIRouter()


@router.get("", response_model=List[Client])
async def read_clients(license: str, limit: int=20, skip: int=0):
    '''License: license's slug or * (all)'''
    logging.info(">>> " + __name__ + ":read_clients")
    return await crud.find_many(license, limit, skip)


@router.post("", response_model=Client)
async def create_client(license: str, data: ClientCreate):
    logging.info(">>> " + __name__ + ":create_client")
    license = license.strip().lower()
    found = await find_license(license)
    if not found:
        raise_bad_request("License is not valid.")
    return await crud.insert(license, data)


@router.get("/{id}", response_model=Client)
async def find_client(license: str, id: str):
    '''License: license's slug or * (all)'''
    logging.info(">>> " + __name__ + ":find_client")
    license = license.strip().lower()
    id = id.strip().lower()
    found = await find_license(license)
    if not found:
        raise_bad_request("License is not valid.")
    client = await crud.find_one(license, id)
    if client:
        return client
    raise_not_found("Not found.")


@router.put("/{id}", response_model=Client)
async def update_client(license: str, id: str, data: ClientUpdate):
    logging.info(">>> " + __name__ + ":update_client")
    license = license.strip().lower()
    id = id.strip().lower()
    client = await crud.find_one(license, id)
    if not client:
        raise_not_found("Client not found.")
    return await crud.update(license, id, data)


@router.delete("/{id}", response_model=Msg)
async def delete_client(license: str, id: str):
    logging.info(">>> " + __name__ + ":delete_client")
    license = license.strip().lower()
    id = id.strip().lower()
    client = await crud.find_one(license, id)
    if not client:
        raise_not_found("Client not found.")
    return await crud.delete(license, id)
