import logging
from typing import List

from fastapi import APIRouter

from crud import license as crud
from crud.utils import raise_not_found, raise_bad_request
from models.base import Msg
from models.license import License, LicenseCreate, LicenseUpdate


router = APIRouter()


@router.get("", response_model=List[License])
async def read_licenses(limit: int=20, skip: int=0):
    logging.info(">>> " + __name__ + ":get")
    return await crud.find_many(limit, skip)


@router.post("", response_model=License)
async def create_license(data: LicenseCreate):
    '''
    Membuat license dan sekaligus user admin (owner).
    `publishDate`: `(yyyy-mm-dd)`.
    '''
    logging.info(">>> " + __name__ + ":create")
    license = await crud.find_one(data.slug)
    if license:
        raise_bad_request('License with this slug is already exists in the system.')
    return await crud.insert_one(data)


@router.get("/{slug}", response_model=License)
async def find_license(slug: str):
    '''Required: `slug`'''
    logging.info(">>> " + __name__ + ":find")
    license = await crud.find_one(slug)
    if not license:
        raise_not_found("License not found.")
    return license


@router.put("/{slug}", response_model=License)
async def update_license(slug: str, data: LicenseUpdate):
    '''Required: `slug`'''
    logging.info(">>> " + __name__ + ":update")

    license = await crud.find_one(slug)
    if not license:
        raise_not_found("License not found.")

    return await crud.update_one(slug, data)


@router.delete("/{slug}", response_model=Msg)
async def delete_license(slug: str):
    '''Required: `slug`'''
    logging.info(">>> " + __name__ + ":delete")

    license = await crud.find_one(slug)
    if not license:
        raise_not_found("License not found.")

    return await crud.delete_one(slug)

