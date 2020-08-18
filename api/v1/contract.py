import logging
from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter

from crud import contract as crud
from crud.client import find_one as find_client
from crud.license import find_one as find_license
from models.base import Msg
from models.contract import Contract, ContractCreate, ContractUpdate
from utils.utils import raise_bad_request, raise_not_found


router = APIRouter()


@router.get("", response_model=List[Contract])
async def read_contracts(license: str, limit: int=20, skip: int=0):
    license = license.strip().lower()
    return await crud.find_many_by_license(license, limit, skip)


@router.post("", response_model=Contract)
async def create_contract(license: str, client: str, data: ContractCreate):
    license = license.strip().lower()
    client = client.strip().lower()

    if not ObjectId.is_valid(client):
        raise_bad_request("Not valid license or client.")

    db_client = await find_client(license, id=client)
    if not db_client:
        raise_bad_request("Not valid license or client.")

    return await crud.insert(license, client, data)


@router.get("/{id}", response_model=Contract)
async def find_contract(license: str, id: str):
    license = license.strip().lower()
    id = id.strip().lower()

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid license ID.")

    contract = await crud.find_one(license, id)
    if not contract:
        raise_not_found()

    return contract


@router.put("/{id}", response_model=Contract)
async def update_contract(license: str, id: str, data: ContractUpdate):
    license = license.strip().lower()
    id = id.strip().lower()

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid license ID.")

    contract = await crud.find_one(license, id)
    if not contract:
        raise_not_found()

    return await crud.update(license, id, data)


@router.delete("/{id}", response_model=Msg)
async def update_contract(license: str, id: str):
    license = license.strip().lower()
    id = id.strip().lower()

    # TODO: If there are related projects, CANCEL

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid license ID.")

    contract = await crud.find_one(license, id)
    if not contract:
        raise_not_found()

    return await crud.delete(license, id)
