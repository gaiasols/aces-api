import logging
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from core.config import (
    DOCTYPE_USER as DOCUMENT_TYPE,
    ERROR_MONGODB_DELETE,
    ERROR_MONGODB_UPDATE,
)
from core.security import get_password_hash, verify_password
from db.mongo import get_collection
from models.user import (
    BaseModel,
    User,
    UserCreate,
    UserSave,
    UserInDB,
    UserUpdate,
    UserUpdateSelf,
)
# from crud.license import is_license_valid
from crud.utils import (
    delete_empty_keys,
    fields_in_create,
    fields_in_update,
    raise_bad_request,
    raise_not_found,
    raise_server_error,
)


def seek_by_license(license: str):
    license = license.strip().lower()
    if license == "all" or license == "*":
        return {}
    return {"license": license}


def seek_by_term(term: str):
    term = term.strip().lower()
    if ObjectId.is_valid(term):
        return {"_id": ObjectId(term)}
    elif "@" in term and "." in term:
        return {"email": term}
    return {"username": term}


async def get_user(username: str):
    logging.info(">>> " + __name__ + ":get_user")
    user = await find_one(username)
    logging.info(user)
    if user:
        return UserInDB(**user)


async def authenticate_user(username: str, password: str):
    logging.info(">>> " + __name__ + ":authenticate_user")
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def find_many(license:str, limit: int, skip: int):
    logging.info(">>> " + __name__ + ":find_many")
    collection = get_collection(DOCUMENT_TYPE)
    seek = seek_by_license(license)
    rs: List[User] = []
    cursor = collection.find(seek, limit=limit, skip=skip)
    async for row in cursor:
        rs.append(row)
    return rs


async def insert_one(data: UserCreate, license_owner: bool):
    logging.info(">>> " + __name__ + ":insert_one")
    collection = get_collection(DOCUMENT_TYPE)
    hashed_password = get_password_hash(data.password)
    model = UserSave(**data.dict(), hashed_password=hashed_password)
    props = fields_in_create(model)
    try:
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            user = await collection.find_one({"_id": rs.inserted_id})
            return user
    except Exception as e:
        logging.info(e)
        raise_server_error(str(e))


async def insert_license_owner(data: UserCreate):
    logging.info(">>> " + __name__ + ":insert_license_owner")
    collection = get_collection(DOCUMENT_TYPE)
    hashed_password = get_password_hash(data.password)
    # model = UserInDB(**data.dict(), hashed_password=hashed_password)
    model = UserSave(**data.dict(), hashed_password=hashed_password)
    model.licenseOwner = True
    model.roles.append("license-admin")
    model.roles.append("project-admin")
    props = fields_in_create(model)
    try:
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            user = await collection.find_one({"_id": rs.inserted_id})
            return user
    except Exception as e:
        logging.info(e)
        raise_server_error(str(e))


async def find_one(term: str):
    logging.info(">>> " + __name__ + ":find_one")
    collection = get_collection(DOCUMENT_TYPE)
    seek = seek_by_term(term)
    return await collection.find_one(seek)


async def find_license_user(license: str, term: str):
    logging.info(">>> " + __name__ + ":find_one")
    collection = get_collection(DOCUMENT_TYPE)
    seek = seek_by_term(term)
    seek["license"] = license
    return await collection.find_one(seek)



async def find_license_owner(license: str):
    logging.info(">>> " + __name__ + ":find_one")
    collection = get_collection(DOCUMENT_TYPE)
    return await collection.find_one(
        {"license": license, "licenseOwner": True}
    )


async def find_by_email_or_username(email: str, username: str):
    logging.info(">>> " + __name__ + ":find_one")
    collection = get_collection(DOCUMENT_TYPE)
    return await collection.find_one({"$or": [
        {"email": email},
        {"username": username}
    ]})


async def get_by_email(email: str):
    logging.info(">>> " + __name__ + ":find_one")
    collection = get_collection(DOCUMENT_TYPE)
    return await collection.find_one({"email": email})


async def update_one(term: str, data: BaseModel):
    logging.info(">>> " + __name__ + ":update_one")

    props = delete_empty_keys(data)
    logging.info( props )
    if len(props) == 0:
        raise_bad_request("No data supplied.")

    collection = get_collection(DOCUMENT_TYPE)
    seek = seek_by_term(term)
    rs = await collection.find_one_and_update(
        seek,
        {"$set": fields_in_update(props)},
        return_document=ReturnDocument.AFTER
    )

    return rs if rs else raise_server_error(ERROR_MONGODB_UPDATE)


async def delete(term: str):
    logging.info(">>> " + __name__ + ":delete")

    collection = get_collection(DOCUMENT_TYPE)
    seek = seek_by_term(term)

    found = await collection.find_one_and_delete(
        seek,
        {"_id": True}
    )
    logging.info(found)
    message = {"message": "User deleted"}
    return message if found else raise_server_error(ERROR_MONGODB_DELETE)
