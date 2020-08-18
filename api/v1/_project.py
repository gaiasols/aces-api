import logging
from typing import Any, List

from bson.objectid import ObjectId
from fastapi import APIRouter

from crud import project as crud
from crud.client import find_one as find_client
from crud.contract import find_one as find_contract
from models.base import Msg
from models.module import Module, ModuleInfo
from models.project import Project, ProjectCreate, ProjectUpdate
from utils.utils import raise_bad_request, raise_not_found


router = APIRouter()


@router.get("", response_model=List[Project])
async def read_projects(license: str, limit: int=20, skip: int=0):
    license = license.strip().lower()
    return await crud.find_many_by_license(license, limit, skip)


@router.post("", response_model=Project)
async def create_project(license: str, client: str, contract: str, data: ProjectCreate):
    logging.info(">>> " + __name__ + ":create_project")
    client = client.strip().lower()
    license = license.strip().lower()
    contract = contract.strip().lower()

    if not (ObjectId.is_valid(client) and ObjectId.is_valid(contract)):
        raise_bad_request("Not valid contract or client.")

    db_client = await find_client(license, id=client)
    if not db_client:
        raise_bad_request("Not valid license or client.")

    db_client = await find_contract(license, id=contract)
    if not db_client:
        raise_bad_request("Not valid license or client.")

    return await crud.insert(license, client, contract, data)


@router.get("/{id}", response_model=Project)
async def find_project(license: str, id: str):
    license = license.strip().lower()
    id = id.strip().lower()

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid project ID.")

    project = await crud.find_one(license, id)
    if not project:
        raise_not_found()

    return project


@router.post("/{id}/modules", response_model=List[Module])
async def set_project_modules(license: str, id: str, modules: List[str]):
    license = license.strip().lower()
    return await crud.add_modules(license, id, modules)


@router.put("/{id}/modules", response_model=Module)
async def update_module(license: str, id: str, module: str, data: ModuleInfo):
    license = license.strip().lower()
    module = module.strip().lower()
    id = id.strip().lower()
    return await crud.update_module(license, id, module, data)


@router.put("/{id}", response_model=Project)
async def update_project(license: str, id: str, data: ProjectUpdate):
    license = license.strip().lower()
    id = id.strip().lower()

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid project ID.")

    project = await crud.find_one(license, id)
    if not project:
        raise_not_found()

    return await crud.update(license, id, data)


@router.delete("/{id}", response_model=Msg)
async def delete_project(license: str, id: str):
    license = license.strip().lower()
    id = id.strip().lower()

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid license ID.")

    project = await crud.find_one(license, id)
    if not project:
        raise_not_found()

    return await crud.delete(license, id)
