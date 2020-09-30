import logging
import random
from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from pymongo import ReturnDocument

from core.config import (
    DOCTYPE_PERSONA,
    USERNAME_ERROR_MESSAGE,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
    ERROR_MONGODB_DELETE,
    ERROR_MONGODB_UPDATE,
)
from core.security import get_password_hash
from db.mongo import get_collection
from models.persona import Persona, PersonaCreate, PersonaUpdate, PersonaInDB
from crud.utils import (
    delete_empty_keys,
    fields_in_create,
    fields_in_update,
    raise_bad_request,
    raise_not_found,
    raise_server_error,
)


def create_fpwd(username: str):
    # First 3 chars
    seed1 = username[:3]
    # Last 4 chars
    seed2 = str(ObjectId())[20:]
    # Randomise
    seed2 = ''.join(random.sample(seed2, len(seed2)))
    return seed1 + seed2


def seek_by_search(project: str, search: str):
    search = search.strip().lower()
    if ObjectId.is_valid(search):
        return {"_id": ObjectId(search), "projectId": project}
    elif "@" in search and "." in search:
        return {"email": search, "projectId": project}
    return {"username": search, "projectId": project}


async def find_by_email_or_username(project: str, email: str, username: str):
    logging.info(">>> " + __name__ + ":find_by_email_or_username")
    collection = get_collection(DOCTYPE_PERSONA)
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
    collection = get_collection(DOCTYPE_PERSONA)
    personas: List[Persona] = []
    cursor = collection.find({ 'projectId': project })
    async for row in cursor:
        personas.append(row)
    return personas


async def find_one(project: str, search: str):
    collection = get_collection(DOCTYPE_PERSONA)
    seek = seek_by_search(project, search)
    # persona = await collection.find_one(seek)
    # if persona:
    #     return persona
    # raise_not_found()
    return await collection.find_one(seek)


async def o_insert(license:str, project: str, data: PersonaCreate):
    hashed_password = get_password_hash(data.password)
    model = PersonaInDB(
        **data.dict(),
        license=license,
        projectId=project,
        hashed_password=hashed_password
    )
    props = fields_in_create(model)
    try:
        collection = get_collection(DOCTYPE_PERSONA)
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            member = await collection.find_one({"_id": rs.inserted_id})
            return member
    except Exception as e:
        logging.info(e)
        raise_server_error(str(e))


async def insert(license:str, project: str, data: PersonaCreate):
    # Create temporary password
    fpwd = create_fpwd(data.username)
    hashed_password = get_password_hash(fpwd)

    model = PersonaInDB(
        **data.dict(),
        license=license,
        projectId=project,
        hashed_password=hashed_password
    )
    props = fields_in_create(model)
    # Persist inverted fpwd in xfpwd
    props["xfpwd"] = fpwd[::-1]
    logging.info(fpwd)
    logging.info(props["xfpwd"])

    try:
        collection = get_collection(DOCTYPE_PERSONA)
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            member = await collection.find_one({"_id": rs.inserted_id})
            return member
    except Exception as e:
        logging.info(e)
        raise_server_error(str(e))


async def update_one(project: str, search: str, data: PersonaUpdate):
    logging.info(">>> " + __name__ + ":update_one")
    try:
        props = delete_empty_keys(data)
        collection = get_collection(DOCTYPE_PERSONA)
        seek = seek_by_search(project, search)
        persona = await collection.find_one_and_update(
            seek,
            {"$set": fields_in_update(props)},
            return_document=ReturnDocument.AFTER
        )
        if persona:
            return persona
    except Exception as e:
        raise_server_error(str(e))


async def set_tests(project: str, search: str, tests: List[str]):
    logging.info(">>> " + __name__ + ":set_tests")
    try:
        collection = get_collection(DOCTYPE_PERSONA)
        seek = seek_by_search(project, search)
        persona = await collection.find_one_and_update(
            seek,
            {"$set": {
                "tests": tests,
                "nextTest": tests[0],
                "updatedAt": datetime.utcnow()
            }},
            return_document=ReturnDocument.AFTER
        )
        if persona:
            return persona
    except Exception as e:
        raise_server_error(str(e))


async def set_simulations(project: str, search: str, sims: List[str]):
    logging.info(">>> " + __name__ + ":set_simulations")
    try:
        collection = get_collection(DOCTYPE_PERSONA)
        seek = seek_by_search(project, search)
        persona = await collection.find_one_and_update(
            seek,
            {"$set": {
                "simulations": sims,
                "nextSim": sims[0],
                "updatedAt": datetime.utcnow()
            }},
            return_document=ReturnDocument.AFTER
        )
        if persona:
            return persona
    except Exception as e:
        raise_server_error(str(e))
