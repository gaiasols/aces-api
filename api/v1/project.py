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
async def read_projects(limit: int=20, skip: int=0, current_user: User = Depends(get_current_active_user)):
    return await crud.find_many_by_license(current_user.license, limit, skip)


@router.post("", response_model=Project)
async def create_project(
    client: str, contract: str, data: ProjectCreate,
    current_user: User = Depends(get_current_active_user)
):
    logging.info(">>> " + __name__ + ":create_project")
    client = client.strip().lower()
    # license = license.strip().lower()
    contract = contract.strip().lower()

    if not (ObjectId.is_valid(client) and ObjectId.is_valid(contract)):
        raise_bad_request("Not valid contract or client.")

    db_client = await find_client(current_user.license, id=client)
    if not db_client:
        raise_bad_request("Not valid license or client.")

    db_client = await find_contract(current_user.license, id=contract)
    if not db_client:
        raise_bad_request("Not valid license or client.")

    return await crud.insert(current_user.license, client, contract, data)


@router.get("/{id}", response_model=Project)
async def find_project(id: str, current_user: User = Depends(get_current_active_user)):
    id = id.strip().lower()

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid project ID.")

    project = await crud.find_one(current_user.license, id)
    if not project:
        raise_not_found()

    return project


@router.post("/{id}/modules", response_model=List[Module])
async def set_project_modules(id: str, modules: List[str], current_user: User = Depends(get_current_active_user)):
    # license = license.strip().lower()
    return await crud.add_modules(current_user.license, id, modules)


@router.put("/{id}/modules", response_model=Module)
async def update_module(id: str, module: str, data: ModuleInfo, current_user: User = Depends(get_current_active_user)):
    # license = license.strip().lower()
    module = module.strip().lower()
    id = id.strip().lower()
    return await crud.update_module(current_user.license, id, module, data)


@router.put("/{id}", response_model=Project)
async def update_project(id: str, data: ProjectUpdate, current_user: User = Depends(get_current_active_user)):
    # license = license.strip().lower()
    id = id.strip().lower()

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid project ID.")

    project = await crud.find_one(current_user.license, id)
    if not project:
        raise_not_found()

    return await crud.update(current_user.license, id, data)


@router.delete("/{id}", response_model=Msg)
async def delete_project(id: str, current_user: User = Depends(get_current_active_user)):
    # license = license.strip().lower()
    id = id.strip().lower()

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid license ID.")

    project = await crud.find_one(current_user.license, id)
    if not project:
        raise_not_found()

    return await crud.delete(current_user.license, id)
