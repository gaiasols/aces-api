import logging
from typing import List

from bson.objectid import ObjectId
from pymongo import ReturnDocument

from core.config import (
    DOCTYPE_MODULE,
    DOCTYPE_PROJECT_MODULE,
    ERROR_MONGODB_DELETE,
    ERROR_MONGODB_UPDATE,
)
from db.mongo import get_collection
from models.module import Module, ModuleInfo, ProjectModule, ProjectModuleInput
from crud import module as crudmodule
from crud.utils import (
    delete_empty_keys,
    fields_in_create,
    fields_in_update,
    raise_bad_request,
    raise_not_found,
    raise_server_error,
)


async def find_many(project: str):
    collection = get_collection(DOCTYPE_PROJECT_MODULE)
    modules: List[Module] = []
    cursor = collection.find({ 'project': project })
    async for row in cursor:
        modules.append(row)
    return modules


async def find_one(project: str, id: str):
    collection = get_collection(DOCTYPE_PROJECT_MODULE)
    return await collection.find_one({"_id": ObjectId(id), "project": project})


async def update_one(project: str, id: str, data: ModuleInfo):
    try:
        props = delete_empty_keys(data)
        collection = get_collection(DOCTYPE_PROJECT_MODULE)
        module = await collection.find_one_and_update(
            {"_id": ObjectId(id), "project": project},
            {"$set": fields_in_update(props)},
            return_document=ReturnDocument.AFTER
        )
        if module:
            return module
    except Exception as e:
        raise_server_error(str(e))


async def delete_one(project: str, id: str):
    try:
        collection = get_collection(DOCTYPE_PROJECT_MODULE)
        module = await collection.find_one_and_delete(
            {"_id": ObjectId(id), "project": project},
            {"_id": True}
        )
        if module:
            return {"message": "Module has been deleted."}
    except Exception as e:
        raise_server_error(str(e))


async def insert(project: str, id: str):
    ref = await crudmodule.find_one(id)
    if not ref:
        raise_server_error("Could not find referenced module.")

    # Manual spread
    models = {
        # '_id': ObjectId(id),
        'ref': id,
        'project': project,
        'type': ref['type'],
        'version': ref['version'],
        'method': ref['method'],
        'name': ref['name'],
        'title': ref['title'],
        'description': ref['description'],
        'items': ref['items'],
        'url': ref['url'],
    }
    logging.info(models)
    props = fields_in_create(models)
    logging.info(props)
    try:
        # props = fields_in_create(data)
        collection = get_collection(DOCTYPE_PROJECT_MODULE)
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            return await collection.find_one({"_id": rs.inserted_id})
    except Exception as e:
        raise_server_error(str(e))
    return None
