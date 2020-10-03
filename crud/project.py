import logging
from typing import List

from bson.objectid import ObjectId
from pymongo import ReturnDocument

from core.config import (
    DOCTYPE_PROJECT,
    ERROR_MONGODB_DELETE,
    ERROR_MONGODB_UPDATE,
)
from db.mongo import get_collection
from models.project import Project, ProjectCreate, ProjectInDB, ProjectUpdate
from models.module import Module, ModuleInfo
from models.user import User
from crud.module import find_modules, find_project_modules
from crud.utils import (
    delete_empty_keys,
    fields_in_create,
    fields_in_update,
    raise_bad_request,
    raise_not_found,
    raise_server_error,
)


async def find_many(limit: int, skip: int):
    collection = get_collection(DOCTYPE_PROJECT)
    projects: List[Project] = []
    cursor = collection.find({}, limit=limit, skip=skip)
    async for row in cursor:
        projects.append(row)
    return projects


async def find_many_by_license(license: str, limit: int, skip: int):
    collection = get_collection(DOCTYPE_PROJECT)
    projects: List[Project] = []
    cursor = collection.find({"license": license}, {"modules": False}, limit=limit, skip=skip)
    # cursor = collection.find({"license": license}, limit=limit, skip=skip)
    async for row in cursor:
        projects.append(row)
    return projects


async def find_one(license: str, id: str):
    collection = get_collection(DOCTYPE_PROJECT)
    return await collection.find_one({"license": license,  "_id": ObjectId(id)})


async def insert(
    license: str,
    creator: str,
    data: ProjectCreate,
    client: str = None,
    contract: str = None
):
    logging.info(">>> " + __name__ + ":insert")
    logging.info(data)

    # Project otomatis memiliki seluruh modul yang tersedia
    aces_modules = await find_project_modules()
    logging.info(aces_modules)
    try:
        project = ProjectInDB(
            **data.dict(),
            license=license,
            client=client,
            contract=contract,
            # admin=creator,
            createdBy=creator,
            modules=aces_modules,
        )
        logging.info("======")
        logging.info(project)
        props = fields_in_create(project)
        collection = get_collection(DOCTYPE_PROJECT)
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            return await collection.find_one({"_id": rs.inserted_id})
    except Exception as e:
        raise_server_error(str(e))


async def add_modules(license: str, id: str, module_ids: List[str]):
    # modules => module str ids
    modules = await find_modules(module_ids)

    try:
        collection = get_collection(DOCTYPE_PROJECT)
        rs = await collection.find_one_and_update(
            {"_id": ObjectId(id), "license": license},
            {"$set": {"modules": modules}},
            {"_id": False, "modules": True},
            return_document=ReturnDocument.AFTER
        )
        logging.info(rs)
        if rs and rs["modules"]:
            return rs["modules"]
    except Exception as e:
        raise_server_error(str(e))


async def update_module(license: str, id: str, module: str, data: ModuleInfo):
    try:
        collection = get_collection(DOCTYPE_PROJECT)
        update = await collection.find_one_and_update(
            {"_id": ObjectId(id), "modules": {"$elemMatch": {"oid": module}}},
            {"$set": {
                "modules.$.title": data.title,
                "modules.$.description": data.description
            }},
            {"_id": False, "modules": {"$elemMatch": {"oid": module}}},
            return_document=ReturnDocument.AFTER
        )
        if update and len(update["modules"]) > 0:
            return update["modules"][0]
    except Exception as e:
        raise_server_error(str(e))


async def update(license: str, id: str, data: ProjectUpdate):
    try:
        props = delete_empty_keys(data)
        collection = get_collection(DOCTYPE_PROJECT)
        project = await collection.find_one_and_update(
            {"_id": ObjectId(id), "license": license},
            {"$set": fields_in_update(props)},
            return_document=ReturnDocument.AFTER
        )
        if project:
            return project
    except Exception as e:
        raise_server_error(str(e))


async def delete(license: str, id: str):
    try:
        collection = get_collection(DOCTYPE_PROJECT)
        project = await collection.find_one_and_delete(
            {"_id": ObjectId(id), "license": license},
            {"_id": True}
        )
        if project:
            return {"message": "Project has been deleted."}
    except Exception as e:
        raise_server_error(str(e))


async def is_valid_project_admin(user: User, id: str) -> bool:
    collection = get_collection(DOCTYPE_PROJECT)
    project = await collection.find_one({"_id": ObjectId(id), "admin": user.username})
    return True if project else False


# ProjectModule


async def get_modules(id: str):
    collection = get_collection(DOCTYPE_PROJECT)
    rs = await collection.find_one(
        {"_id": ObjectId(id)},
        {"_id": False, "modules": True}
    )
    logging.info(rs)
    return rs["modules"]

