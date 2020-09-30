import logging
from typing import List

from bson.objectid import ObjectId
from pymongo import ReturnDocument

from core.config import (
    DOCTYPE_CONTRACT,
    ERROR_MONGODB_DELETE,
    ERROR_MONGODB_UPDATE,
)
from db.mongo import get_collection
from models.contract import Contract, ContractCreate, ContractInDB, ContractUpdate
from crud.utils import (
    delete_empty_keys,
    fields_in_create,
    fields_in_update,
    raise_bad_request,
    raise_not_found,
    raise_server_error,
)


async def find_many(limit: int, skip: int):
    collection = get_collection(DOCTYPE_CONTRACT)
    contracts: List[Contract] = []
    cursor = collection.find({}, limit=limit, skip=skip)
    async for row in cursor:
        contracts.append(row)
    return contracts


async def find_many_by_license(slug: str, limit: int, skip: int):
    collection = get_collection(DOCTYPE_CONTRACT)
    contracts: List[Contract] = []
    cursor = collection.find({"license": slug}, limit=limit, skip=skip)
    async for row in cursor:
        contracts.append(row)
    return contracts


async def find_one(slug: str, id: str):
    collection = get_collection(DOCTYPE_CONTRACT)
    return await collection.find_one({"license": slug,  "_id": ObjectId(id)})


async def insert(slug: str, client: str, data: ContractCreate):
    try:
        contract = ContractInDB(**data.dict(), license=slug, clientId=client)
        props = fields_in_create(contract)
        collection = get_collection(DOCTYPE_CONTRACT)
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            return await collection.find_one({"_id": rs.inserted_id})
    except Exception as e:
        raise_server_error(str(e))


async def update(slug: str, id: str, data: ContractUpdate):
    try:
        props = delete_empty_keys(data)
        collection = get_collection(DOCTYPE_CONTRACT)
        contract = await collection.find_one_and_update(
            {"_id": ObjectId(id), "license": slug},
            {"$set": fields_in_update(props)},
            return_document=ReturnDocument.AFTER
        )
        if contract:
            return contract
    except Exception as e:
        raise_server_error(str(e))


async def delete(slug: str, id: str):
    try:
        collection = get_collection(DOCTYPE_CONTRACT)
        contract = await collection.find_one_and_delete(
            {"_id": ObjectId(id), "license": slug},
            {"_id": True}
        )
        if contract:
            return {"message": "Contract has been deleted."}
    except Exception as e:
        raise_server_error(str(e))
