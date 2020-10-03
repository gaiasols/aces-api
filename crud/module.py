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
from models.module import Module, ModuleCreate, ModuleUpdate, ModuleInfo
from models.project import ProjectModule
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


async def find_project_modules():
    logging.info(">>> " + __name__ + ":find_project_modules")
    collection = get_collection(DOCTYPE_MODULE)
    modules: List[ProjectModule] = []
    cursor = collection.find({})
    async for row in cursor:
        # modules.append(row)
        idref = str(row["_id"])
        logging.info(row)
        project_module = ProjectModule(**row, ref=idref)
        logging.info(project_module)
        modules.append(project_module)
    return modules


async def find_modules(ids: List[str]) -> List[Module]:
    filter = []
    for id in ids:
        if ObjectId.is_valid(id):
            filter.append({"_id": ObjectId(id)})
    if len(filter) == 0:
        return []

    collection = get_collection(DOCTYPE_MODULE)
    modules: List[Module] = []
    cursor = collection.find({"$or": filter})
    async for row in cursor:
        module = Module(**row)
        modules.append(module.dict())
    return modules


def seek_by_term(term: str):
    if ObjectId.is_valid(term):
        return {"_id": ObjectId(term)}
    return {"slug": term}


async def find_one(id: str):
    collection = get_collection(DOCTYPE_MODULE)
    seek = seek_by_term(id)
    logging.info(seek)
    # return await collection.find_one({"_id": ObjectId(id)})
    return await collection.find_one(seek)


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
