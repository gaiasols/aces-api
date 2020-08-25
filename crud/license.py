import logging
from pymongo import ReturnDocument

from core.config import (
    DOCTYPE_LICENSE as DOCUMENT_TYPE,
    DOCTYPE_USER,
    ERROR_MONGODB_UPDATE,
    ERROR_MONGODB_DELETE,
    NEW_LICENSE_PASSWORD,
)
from db.mongo import get_collection
from models.license import (
    BaseModel,
    License,
    LicenseCreate,
)
from models.user import UserCreate
from crud.user import insert_license_owner
from crud.utils import (
    delete_empty_keys,
    fields_in_create,
    fields_in_update,
    raise_bad_request,
    raise_not_found,
    raise_server_error,
)


def seek(slug: str):
    return {"slug": slug.strip().lower()}


async def find_many(limit: int, skip: int):
    logging.info(">>> " + __name__ + ":find_many")
    collection = get_collection(DOCUMENT_TYPE)
    rs: List[License] = []
    cursor = collection.find({}, limit=limit, skip=skip)
    async for row in cursor:
        rs.append(row)
    return rs


async def insert_one(data: LicenseCreate):
    logging.info(">>> " + __name__ + ":insert_one")
    collection = get_collection(DOCUMENT_TYPE)
    props = fields_in_create(data)
    try:
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            license = await collection.find_one({"_id": rs.inserted_id})
            # Create license owner
            owner = UserCreate(
                license = data.slug,
                name = data.contactName,
                username = data.contactUsername,
                email = data.contactEmail,
                password = NEW_LICENSE_PASSWORD
            )
            user = await insert_license_owner(owner)
            return license
    except Exception as e:
        logging.info(e)
        raise_server_error(str(e))


async def find_one(slug: str):
    logging.info(">>> " + __name__ + ":find_one")
    collection = get_collection(DOCUMENT_TYPE)
    filter = seek(slug)
    return await collection.find_one(filter)


async def update_one(slug: str, data: BaseModel):
    logging.info(">>> " + __name__ + ":update_one")
    props = delete_empty_keys(data)
    logging.info(props)
    if len(props) == 0:
        raise_bad_request("No data supplied")
    collection = get_collection(DOCUMENT_TYPE)
    filter = seek(slug)
    rs = await collection.find_one_and_update(
        filter,
        {"$set": fields_in_update(props)},
        return_document=ReturnDocument.AFTER
    )
    return rs if rs else raise_server_error(ERROR_MONGODB_UPDATE)


async def delete_one(slug: str):
    logging.info(">>> " + __name__ + ":delete_one")
    collection = get_collection(DOCUMENT_TYPE)
    filter = seek(slug)
    deleted = collection.find_one_and_delete(filter, {"_id": True})
    if deleted:
        return {"message": "Resource deleted."}
    raise_server_error(ERROR_MONGODB_DELETE)

