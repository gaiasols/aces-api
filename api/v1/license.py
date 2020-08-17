import logging
from typing import Any, List

from fastapi import APIRouter

from crud import license as crud
from models.license import License, LicenseUpdateSelf
from utils.utils import raise_bad_request, raise_not_found

router = APIRouter()


@router.get("/{slug}", response_model=License)
async def read_license_info(slug: str):
    logging.info(">>> " + __name__ + ":find")
    license = await crud.find_one(slug)
    if not license:
        raise_not_found("License not found.")
    return license



@router.put("/{slug}", response_model=License)
async def update_license_info(slug: str, data: LicenseUpdateSelf):
    logging.info(">>> " + __name__ + ":update")
    license = await crud.find_one(slug)
    if not license:
        raise_not_found("License not found.")
    return await crud.update_one(slug, data)
