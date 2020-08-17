import logging
from typing import List

from bson.objectid import ObjectId
from pymongo import ReturnDocument

from core.config import DOCTYPE_CLIENT as DOCUMENT_TYPE
from core.config import ERROR_MONGODB_DELETE, ERROR_MONGODB_UPDATE
from crud.utils import (delete_empty_keys, fields_in_create, fields_in_update,
                        raise_bad_request, raise_server_error)
from db.mongo import get_collection
from models.client import Client, ClientCreate, ClientUpdate, ClientWithLicense


async def find_many(license: str, limit: int, skip: int):
    logging.info(">>> " + __name__ + ":find_many")
    collection = get_collection(DOCUMENT_TYPE)
    licenses: List[Client] = []
    cursor = collection.find({"license": license}, limit=limit, skip=skip)
    async for row in cursor:
        licenses.append(row)
    return licenses


async def insert(license: str, data: ClientCreate):
    logging.info(">>> " + __name__ + ":insert")
    collection = get_collection(DOCUMENT_TYPE)
    client = ClientWithLicense(**data.dict(), license=license)
    props = fields_in_create(client)
    try:
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            client = await collection.find_one({"_id": rs.inserted_id})
            return client
    except Exception as e:
        raise_server_error(str(e))


async def find_one(license: str, id: str):
    logging.info(">>> " + __name__ + ":find_one")
    collection = get_collection(DOCUMENT_TYPE)
    seek = {"license": license, "_id": ObjectId(id)}
    return await collection.find_one(seek)


async def update(license: str, id: str, data: ClientUpdate):
    logging.info(">>> " + __name__ + ":update")
    props = delete_empty_keys(data)
    if len(props) == 0:
        raise_bad_request("No data supplied.")
    collection = get_collection(DOCUMENT_TYPE)
    seek = {"license": license, "_id": ObjectId(id)}
    client = await collection.find_one_and_update(
        seek,
        {"$set": fields_in_update(props)},
        return_document=ReturnDocument.AFTER
    )
    if client:
        return client
    raise_server_error(ERROR_MONGODB_UPDATE)


async def delete(license: str, id: str):
    logging.info(">>> " + __name__ + ":delete")
    collection = get_collection(DOCUMENT_TYPE)
    seek = {"license": license, "_id": ObjectId(id)}
    client = await collection.find_one_and_delete(seek, {"_id": True})
    if client:
        return {"message": "Client deleted."}
    raise_server_error(ERROR_MONGODB_DELETE)
