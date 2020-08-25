import logging
from typing import List

from bson.objectid import ObjectId
from pymongo import ReturnDocument

from core.config import (
    DOCTYPE_PROJECT_MEMBER,
    ERROR_MONGODB_DELETE,
    ERROR_MONGODB_UPDATE,
)
from core.security import get_password_hash
from db.mongo import get_collection
from models.projectmember import Member, MemberBase, MemberCreate, MemberInDB
from crud.utils import (
    delete_empty_keys,
    fields_in_create,
    fields_in_update,
    raise_bad_request,
    raise_not_found,
    raise_server_error,
)


def seek_by_search(project: str, search: str):
    search = search.strip().lower()
    if ObjectId.is_valid(search):
        return {"_id": ObjectId(search), "project": project}
    elif "@" in search and "." in search:
        return {"email": search, "project": project}
    return {"username": search, "project": project}


async def find_many(project: str):
    collection = get_collection(DOCTYPE_PROJECT_MEMBER)
    members: List[Member] = []
    cursor = collection.find({ 'project': project })
    async for row in cursor:
        members.append(row)
    return members


async def find_one(project: str, search: str):
    collection = get_collection(DOCTYPE_PROJECT_MEMBER)
    seek = seek_by_search(project, search)
    return await collection.find_one(seek)


async def delete_one(project: str, search: str):
    try:
        collection = get_collection(DOCTYPE_PROJECT_MEMBER)
        seek = seek_by_search(project, search)
        member = await collection.find_one_and_delete(
            seek,
            {"_id": True}
        )
        if member:
            return {"message": "Member has been deleted."}
    except Exception as e:
        raise_server_error(str(e))


async def insert(project: str, data: MemberCreate):
    hashed_password = get_password_hash(data.password)
    model = MemberInDB(
        **data.dict(),
        project=project,
        hashed_password=hashed_password
    )
    props = fields_in_create(model)
    try:
        collection = get_collection(DOCTYPE_PROJECT_MEMBER)
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            member = await collection.find_one({"_id": rs.inserted_id})
            return member
    except Exception as e:
        logging.info(e)
        raise_server_error(str(e))
