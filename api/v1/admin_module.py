import logging
from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter

from crud import module as crud
from models.base import Msg
from models.module import Module, ModuleCreate, ModuleUpdate
from utils.utils import raise_bad_request, raise_not_found


router = APIRouter()


@router.get("", response_model=List[Module])
async def read_modules():
    return await crud.find_many()


@router.post("", response_model=Module)
async def create_module(data: ModuleCreate):
    return await crud.insert(data)


@router.get("/{id}", response_model=Module)
async def find_module(id: str):
    id = id.strip().lower()

    # if not ObjectId.is_valid(id):
        # raise_bad_request("Not valid module ID.")

    module = await crud.find_one(id)
    if not module:
        raise_not_found()

    return module


@router.put("/{id}", response_model=Module)
async def update_module(id: str, data: ModuleUpdate):
    id = id.strip().lower()

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid module ID.")

    module = await crud.find_one(id)
    if not module:
        raise_not_found()

    return await crud.update(id, data)


@router.delete("/{id}", response_model=Msg)
async def update_module(id: str):
    id = id.strip().lower()

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid module ID.")

    module = await crud.find_one(id)
    if not module:
        raise_not_found()

    return await crud.delete(id)
