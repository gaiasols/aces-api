import logging
from typing import List

from bson.objectid import ObjectId
from pymongo import ReturnDocument

from core.config import (
    DOCTYPE_MODULE,
    ERROR_MONGODB_DELETE,
    ERROR_MONGODB_UPDATE,
)
from db.mongo import get_collection
from models.module import Module, ModuleCreate, ModuleUpdate, ModuleSimpleUpdate
from crud.utils import (
    delete_empty_keys,
    fields_in_create,
    fields_in_update,
    raise_bad_request,
    raise_not_found,
    raise_server_error,
)


async def find_many():
    collection = get_collection(DOCTYPE_MODULE)
    modules: List[Module] = []
    cursor = collection.find({})
    async for row in cursor:
        modules.append(row)
    return modules


async def find_one(id: str):
    collection = get_collection(DOCTYPE_MODULE)
    return await collection.find_one({"_id": ObjectId(id)})


async def insert(data: ModuleCreate):
    try:
        props = fields_in_create(data)
        collection = get_collection(DOCTYPE_MODULE)
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            return await collection.find_one({"_id": rs.inserted_id})
    except Exception as e:
        raise_server_error(str(e))


async def update(id: str, data: ModuleUpdate):
    try:
        props = delete_empty_keys(data)
        collection = get_collection(DOCTYPE_MODULE)
        module = await collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": fields_in_update(props)},
            return_document=ReturnDocument.AFTER
        )
        if module:
            return module
    except Exception as e:
        raise_server_error(str(e))


async def delete(id: str):
    try:
        collection = get_collection(DOCTYPE_MODULE)
        module = await collection.find_one_and_delete(
            {"_id": ObjectId(id)},
            {"_id": True}
        )
        if module:
            return {"message": "Module has been deleted."}
    except Exception as e:
        raise_server_error(str(e))
