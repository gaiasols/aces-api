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
    create_fpwd,
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
        return {"_id": ObjectId(search), "projectId": project}
    elif "@" in search and "." in search:
        return {"email": search, "projectId": project}
    return {"username": search, "projectId": project}


async def find_by_email_or_username(project: str, email: str, username: str):
    logging.info(">>> " + __name__ + ":find_by_email_or_username")
    collection = get_collection(DOCTYPE_PROJECT_MEMBER)
    return await collection.find_one(
        {
            "projectId": project,
            "$or": [
                {"email": email},
                {"username": username}
            ]
        }
    )


async def find_many(project: str):
    collection = get_collection(DOCTYPE_PROJECT_MEMBER)
    members: List[Member] = []
    cursor = collection.find({ 'projectId': project })
    async for row in cursor:
        members.append(row)
    return members


async def find_one(project: str, search: str):
    collection = get_collection(DOCTYPE_PROJECT_MEMBER)
    seek = seek_by_search(project, search)
    member = await collection.find_one(seek)
    if member:
        return member
    raise_not_found()


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
    fpwd = create_fpwd(data.username)
    hashed_password = get_password_hash(fpwd)
    model = MemberInDB(
        **data.dict(),
        projectId=project,
        hashed_password=hashed_password
    )
    props = fields_in_create(model)
    props["xfpwd"] = fpwd[::-1]
    try:
        collection = get_collection(DOCTYPE_PROJECT_MEMBER)
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            member = await collection.find_one({"_id": rs.inserted_id})
            return member
    except Exception as e:
        logging.info(e)
        raise_server_error(str(e))
