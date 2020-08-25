import logging
from typing import Any, List

from fastapi import APIRouter, Depends

from api.v1.deps import get_current_active_user, get_current_license_owner
from crud import license as crud
from crud.module import find_many as get_modules
from models.license import License, LicenseUpdateSelf
from models.module import Module
from models.user import User
from utils.utils import raise_bad_request, raise_not_found

router = APIRouter()


@router.get("", response_model=License)
async def read_info(slug: str, current_user: User=Depends(get_current_active_user)):
    logging.info(">>> " + __name__ + ":read_info")
    slug = slug.strip().lower()
    license = await crud.find_one(slug)
    if not license:
        raise_not_found("License not found.")
    return license


@router.put("", response_model=License)
async def update_info(slug: str, data: LicenseUpdateSelf, current_user: User=Depends(get_current_license_owner)):
    logging.info(">>> " + __name__ + ":update_info")
    slug = slug.strip().lower()
    # license = await crud.find_one(current_user.license)
    # if not license:
    #     raise_not_found("License not found.")
    return await crud.update_one(slug, data)


@router.get("/modules", response_model=List[Module])
async def get_aces_modules(slug: str, current_user: User=Depends(get_current_active_user)) -> Any:
    return await get_modules()
