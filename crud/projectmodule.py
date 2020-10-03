import logging
from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from pymongo import ReturnDocument

from core.config import (
    DOCTYPE_PROJECT,
    ERROR_MONGODB_DELETE,
    ERROR_MONGODB_UPDATE,
)
from db.mongo import get_collection
from models.project import ProjectModule, ProjectModuleUpdate
from crud import module as crudmodule
from crud.utils import (
    delete_empty_keys,
    fields_in_create,
    fields_in_update,
    raise_bad_request,
    raise_not_found,
    raise_server_error,
)


async def read_modules(project: str):
    collection = get_collection(DOCTYPE_PROJECT)
    rs = await collection.find_one(
        {"_id": ObjectId(project)},
        {"_id": False, "modules": True}
    )
    logging.info(rs)
    return rs["modules"]


async def read_module(project: str, id: str):
    collection = get_collection(DOCTYPE_PROJECT)
    rs = await collection.find_one(
        {"_id": ObjectId(project)},
        {"_id": False, "modules": {"$elemMatch": {"ref": id}}}
    )
    logging.info(rs)
    if rs and rs["modules"] and len(rs["modules"]) > 0:
        return rs["modules"][0]
    raise_not_found()


async def update_one(project: str, id: str, data: ProjectModuleUpdate):
    logging.info(">>> " + __name__ + ":update_one")

    props = {"updatedAt": datetime.utcnow()}
    if data.title:
        props["modules.$.title"] = data.title
    if data.description:
        props["modules.$.description"] = data.description

    collection = get_collection(DOCTYPE_PROJECT)
    rs = await collection.find_one_and_update(
        {"_id": ObjectId(project), "modules": {"$elemMatch": {"ref": id}}},
        {"$set": props},
        {"_id": False, "modules": {"$elemMatch": {"ref": id}}},
        return_document=ReturnDocument.AFTER
    )

    if rs == None:
        raise_not_found()

    if rs and rs["modules"] and len(rs["modules"]) > 0:
        return rs["modules"][0]

    raise_server_error()


async def enable(project: str, id: str, enable: bool):
    logging.info(">>> " + __name__ + ":enable")

    collection = get_collection(DOCTYPE_PROJECT)
    rs = await collection.find_one_and_update(
        {"_id": ObjectId(project), "modules": {"$elemMatch": {"ref": id}}},
        {"$set": {
            "modules.$.enabled": enable,
            "updatedAt": datetime.utcnow()
        }},
        {"_id": False, "modules": {"$elemMatch": {"ref": id}}},
        return_document=ReturnDocument.AFTER
    )

    if rs == None:
        raise_not_found()

    if rs and rs["modules"] and len(rs["modules"]) > 0:
        return rs["modules"][0]

    raise_server_error()
