import logging
from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, Depends

from api.v1.deps import get_current_active_user
from crud import contract as crud
from crud.client import find_one as find_client
from models.base import Msg
from models.contract import Contract, ContractCreate, ContractUpdate
from models.user import User
from utils.utils import raise_bad_request, raise_not_found


router = APIRouter()


@router.get("", response_model=List[Contract])
async def read_contracts(slug: str, limit: int=20, skip: int=0, current_user: User = Depends(get_current_active_user)):
    slug = slug.strip().lower()
    return await crud.find_many_by_license(slug, limit, skip)


@router.post("", response_model=Contract)
async def create_contract(slug: str, client: str, data: ContractCreate, current_user: User = Depends(get_current_active_user)):
    slug = slug.strip().lower()
    client = client.strip().lower()

    if not ObjectId.is_valid(client):
        raise_bad_request("Not valid client id.")

    # Check client
    db_client = await find_client(slug, id=client)
    if not db_client:
        raise_bad_request("Client not found.")

    return await crud.insert(slug, client, data)


@router.get("/{id}", response_model=Contract)
async def find_contract(slug: str, id: str, current_user: User = Depends(get_current_active_user)):
    slug = slug.strip().lower()
    id = id.strip().lower()

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid license ID.")

    contract = await crud.find_one(slug, id)
    if not contract:
        raise_not_found()

    return contract


@router.put("/{id}", response_model=Contract)
async def update_contract(slug: str, id: str, data: ContractUpdate, current_user: User = Depends(get_current_active_user)):
    '''
    Pricing harus update whole array.
    '''
    slug = slug.strip().lower()
    id = id.strip().lower()

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid license ID.")

    contract = await crud.find_one(slug, id)
    if not contract:
        raise_not_found()

    return await crud.update(slug, id, data)


@router.delete("/{id}", response_model=Msg)
async def update_contract(slug: str, id: str, current_user: User = Depends(get_current_active_user)):
    slug = slug.strip().lower()
    id = id.strip().lower()

    # TODO: If there are related projects, CANCEL

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid license ID.")

    contract = await crud.find_one(slug, id)
    if not contract:
        raise_not_found()

    return await crud.delete(slug, id)
