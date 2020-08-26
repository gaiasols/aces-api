import logging
from typing import Any, List

from fastapi import APIRouter, Depends

from api.v1.login import get_current_active_user
from crud import license as crud
from crud.project import find_one as find_project, find_many_by_license
from models.license import License, LicenseUpdateSelf
from models.user import User
from models.project import Project
from utils.utils import raise_bad_request, raise_not_found

router = APIRouter()


@router.get("", response_model=License)
async def read_info(current_user: User=Depends(get_current_active_user)):
    logging.info(">>> " + __name__ + ":read_info")
    license = await crud.find_one(current_user.license)
    if not license:
        raise_not_found("License not found.")
    return license


@router.put("", response_model=License)
async def update_info(data: LicenseUpdateSelf, current_user: User=Depends(get_current_active_user)):
    logging.info(">>> " + __name__ + ":update_info")
    # license = await crud.find_one(current_user.license)
    # if not license:
    #     raise_not_found("License not found.")
    return await crud.update_one(current_user.license, data)


@router.get("/{slug}/projects", response_model=List[Project])
async def get_license_project(slug: str, limit: int = 20, skip: int = 0):
    return await find_many_by_license(slug, limit, skip)


@router.get("/{slug}/projects/{id}", response_model=Project)
async def get_license_project(slug: str, id: str):
    return await find_project(license=slug, id=id)

