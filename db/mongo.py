import logging
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import (
    MONGODB_URI,
    MONGODB_NAME,
    ADMIN_DBNAME,
    MONGODB_MAX_POOL_SIZE,
    MONGODB_MIN_POOL_SIZE,
    DOCTYPE_ADMIN,
    DOCTYPE_CLIENT,
    DOCTYPE_LICENSE,
    DOCTYPE_USER,
    DOCTYPE_MODULE,
    DOCTYPE_PROJECT,
    DOCTYPE_PROJECT_MEMBER,
    DOCTYPE_PERSONA,
)

class MongoDB:
    client: AsyncIOMotorClient = None

db = MongoDB()


async def close():
    logging.info("Closing MongoDB Atlas connection")
    db.client.close()
    logging.info("Connection closed")


def get_connection():
    return db.client


def get_collection(name: str):
    conn = get_connection()
    return conn[MONGODB_NAME][name]


async def connect():
    logging.info("Connecting to MongoDB Atlas...")
    db.client = AsyncIOMotorClient(
        MONGODB_URI,
        maxPoolSize=MONGODB_MAX_POOL_SIZE,
        minPoolSize=MONGODB_MIN_POOL_SIZE
    )

    if db.client:
        logging.info("Connected to MongoDB Atlas")

    # await check_admin_indexes(db.client)
    # await check_module_indexes(db.client)
    await check_license_indexes(db.client)
    # await check_user_indexes(db.client)
    # await check_client_indexes(db.client)
    # await check_project_indexes(db.client)
    await check_project_member_indexes(db.client)
    # await check_persona_indexes(db.client)


# Admins
async def check_admin_indexes(db: AsyncIOMotorClient):
    logging.info(">>> " + __name__ + ":check_admin_indexes")
    logging.info(">>> Cheking admin indexes...")
    collection = db[ADMIN_DBNAME][DOCTYPE_ADMIN]
    info = await collection.index_information()
    index_name = "admin_username_index"
    if index_name in info:
        logging.info(">>> Found " + index_name)
    else:
        logging.info(">>> Index not found, creating one: " + index_name)
        await collection.create_index(
            [("username", 1)],
            unique=True,
            name=index_name
        )


# Modules
async def check_module_indexes(db: AsyncIOMotorClient):
    logging.info(">>> " + __name__ + ":check_module_indexes")
    logging.info(">>> Cheking module indexes...")
    collection = db[MONGODB_NAME][DOCTYPE_MODULE]
    info = await collection.index_information()
    index_name = "module_compound_index"
    if index_name in info:
        logging.info(">>> Found " + index_name)
    else:
        logging.info(">>> Index not found, creating one: " + index_name)
        await collection.create_index(
            [("type", 1), ("version", 1)],
            unique=True,
            name=index_name
        )


# Licenses
async def check_license_indexes(db: AsyncIOMotorClient):
    logging.info(">>> " + __name__ + ":check_license_indexes")
    logging.info(">>> Cheking licence indexes...")
    collection = db[MONGODB_NAME][DOCTYPE_LICENSE]
    info = await collection.index_information()
    index_name = "license_slug_index"
    if index_name in info:
        logging.info(">>> Found " + index_name)
    else:
        logging.info(">>> Index not found, creating one: " + index_name)
        await collection.create_index(
            [("slug", 1)],
            unique=True,
            name=index_name
        )


# Users: username and email are unique across ACES
async def check_user_indexes(db: AsyncIOMotorClient):
    logging.info(">>> " + __name__ + ":check_user_indexes")
    logging.info(">>> Cheking user indexes...")
    collection = db[MONGODB_NAME][DOCTYPE_USER]
    info = await collection.index_information()

    # One email my be used in different license
    index_name = "user_license_email_index"
    if index_name in info:
        logging.info(">>> Found " + index_name)
    else:
        logging.info(">>> Index not found, creating one: " + index_name)
        await collection.create_index(
            [("license", 1), ("email", 1)],
            unique=True,
            name=index_name
        )

    # No identical usernames with the same license
    index_name = "user_license_username_index"
    if index_name in info:
        logging.info(">>> Found " + index_name)
    else:
        logging.info(">>> Index not found, creating one: " + index_name)
        await collection.create_index(
            [("license", 1), ("username", 1)],
            unique=True,
            name=index_name
        )



# Users
async def __check_user_indexes(db: AsyncIOMotorClient):
    logging.info(">>> " + __name__ + ":check_user_indexes")
    logging.info(">>> Cheking user indexes...")
    collection = db[MONGODB_NAME][DOCTYPE_USER]
    info = await collection.index_information()

    # One email my be used in different license
    index_name = "user_license_email_index"
    if index_name in info:
        logging.info(">>> Found " + index_name)
    else:
        logging.info(">>> Index not found, creating one: " + index_name)
        await collection.create_index(
            [("license", 1), ("email", 1)],
            unique=True,
            name=index_name
        )

    # No identical usernames with the same license
    index_name = "user_license_username_index"
    if index_name in info:
        logging.info(">>> Found " + index_name)
    else:
        logging.info(">>> Index not found, creating one: " + index_name)
        await collection.create_index(
            [("license", 1), ("username", 1)],
            unique=True,
            name=index_name
        )


# Clients
async def check_client_indexes(db: AsyncIOMotorClient):
    logging.info(">>> " + __name__ + ":check_client_indexes")
    logging.info(">>> Cheking client indexes...")
    collection = db[MONGODB_NAME][DOCTYPE_CLIENT]
    info = await collection.index_information()

    index_name = "client_compound_index"
    if index_name in info:
        logging.info(">>> Found " + index_name)
    else:
        logging.info(">>> Index not found, creating one: " + index_name)
        await collection.create_index(
            [("license", 1), ("name", 1)],
            unique=True,
            name=index_name
        )


# Project
async def check_project_indexes(db: AsyncIOMotorClient):
    logging.info(">>> " + __name__ + ":check_project_indexes")
    logging.info(">>> Cheking project indexes...")
    collection = db[MONGODB_NAME][DOCTYPE_PROJECT]
    info = await collection.index_information()

    # This index exists but does not function
    index_name = "project_member_index"
    if index_name in info:
        logging.info(">>> Found " + index_name)
    else:
        logging.info(">>> Index not found, creating one: " + index_name)
        await collection.create_index(
            # [("slug", 1), ("members.username", 1)],
            [ ("slug", 1), ("members.username", 1) ],
            unique=True,
            name=index_name
        )


# Project member
async def check_project_member_indexes(db: AsyncIOMotorClient):
    logging.info(">>> " + __name__ + ":check_project_member_indexes")
    logging.info(">>> Cheking project_members indexes...")
    collection = db[MONGODB_NAME][DOCTYPE_PROJECT_MEMBER]
    info = await collection.index_information()

    index_name = "project_member_username_index"
    if index_name in info:
        logging.info(">>> Found " + index_name)
    else:
        logging.info(">>> Index not found, creating one: " + index_name)
        await collection.create_index(
            [ ("project", 1), ("username", 1) ],
            unique=True,
            name=index_name
        )

    index_name = "project_member_email_index"
    if index_name in info:
        logging.info(">>> Found " + index_name)
    else:
        logging.info(">>> Index not found, creating one: " + index_name)
        await collection.create_index(
            [ ("project", 1), ("email", 1) ],
            unique=True,
            name=index_name
        )


# Persona
async def check_persona_indexes(db: AsyncIOMotorClient):
    logging.info(">>> " + __name__ + ":check_persona_indexes")
    logging.info(">>> Cheking persona indexes...")
    collection = db[MONGODB_NAME][DOCTYPE_PERSONA]
    info = await collection.index_information()

    index_name = "persona_username_index"
    if index_name in info:
        logging.info(">>> Found " + index_name)
    else:
        logging.info(">>> Index not found, creating one: " + index_name)
        await collection.create_index(
            [ ("project", 1), ("username", 1) ],
            unique=True,
            name=index_name
        )

    index_name = "persona_email_index"
    if index_name in info:
        logging.info(">>> Found " + index_name)
    else:
        logging.info(">>> Index not found, creating one: " + index_name)
        await collection.create_index(
            [ ("project", 1), ("email", 1) ],
            unique=True,
            name=index_name
        )
