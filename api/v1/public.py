import logging
from typing import Any, List

from bson.objectid import ObjectId
from fastapi import APIRouter, Depends

from crud import project as crud
from crud.client import find_one as find_client
from crud.contract import find_one as find_contract
from crud.license import find_one as find_license
from models.base import Msg
from models.module import Module, ModuleInfo
from models.project import Project, ProjectCreate, ProjectUpdate
from models.user import User
from utils.utils import raise_bad_request, raise_not_found
from api.v1.login import get_current_active_user


router = APIRouter()

# async def test_license(current_user: User = Depends(get_current_active_user)):

@router.get("", response_model=List[Project])
async def read_projects(license: str, limit: int=20, skip: int=0):
    return await crud.find_many_by_license(license, limit, skip)


@router.get("/{id}", response_model=Project)
async def find_project(license: str, id: str):
    id = id.strip().lower()

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid project ID.")

    project = await crud.find_one(license, id)
    if not project:
        raise_not_found()

    return project
