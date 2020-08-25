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
from api.v1.deps import get_current_active_user, get_current_project_admin


router = APIRouter()

# async def test_license(current_user: User = Depends(get_current_active_user)):

@router.get("", response_model=List[Project])
async def read_projects(
    slug: str,
    limit: int=20,
    skip: int=0,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    slug = slug.strip().lower()
    return await crud.find_many_by_license(slug, limit, skip)

# license: str,
# creator: str,
# data: ProjectCreate,
# client: str,
# contract: str

@router.post("", response_model=Project)
async def create_project(
    slug: str,
    data: ProjectCreate,
    current_user: User = Depends(get_current_project_admin),
    client: str = None,
    contract: str = None,
) -> Any:
    logging.info(">>> " + __name__ + ":create_project")
    slug = slug.strip().lower()

    if client:
        client = client.strip().lower()
        if not ObjectId.is_valid(client):
            raise_bad_request("Not valid client id.")
        db_client = await find_client(slug, id=client)
        if not db_client:
            raise_bad_request("Client reference not found.")

    if contract:
        contract = contract.strip().lower()
        if not ObjectId.is_valid(contract):
            raise_bad_request("Not valid contract id.")
        db_client = await find_contract(slug, id=contract)
        if not db_client:
            raise_bad_request("Contract reference not found.")

    creator = current_user.username
    return await crud.insert(slug, creator, data, client, contract)


@router.get("/{id}", response_model=Project)
async def find_project(
    slug: str,
    id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    slug = slug.strip().lower()
    id = id.strip().lower()

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid project ID.")

    project = await crud.find_one(slug, id)
    if not project:
        raise_not_found()

    return project


# @router.post("/{id}/modules", response_model=List[Module])
async def set_project_modules(
    slug: str,
    id: str,
    modules: List[str],
    current_user: User = Depends(get_current_project_admin)
) -> Any:
    slug = slug.strip().lower()

    if not crud.is_valid_project_admin(current_user, id):
        raise HTTPException(status_code=400, detail="You'r not the admin of the project.")
    return await crud.add_modules(slug, id, modules)


# @router.put("/{id}/modules", response_model=Module)
async def update_module(
    slug: str,
    id: str,
    module: str,
    data: ModuleInfo,
    current_user: User = Depends(get_current_project_admin)
) -> Any:
    slug = slug.strip().lower()
    module = module.strip().lower()
    id = id.strip().lower()

    if not crud.is_valid_project_admin(current_user, id):
        raise HTTPException(status_code=400, detail="You'r not the admin of the project.")

    return await crud.update_module(slug, id, module, data)


@router.put("/{id}", response_model=Project)
async def update_project(
    slug: str,
    id: str,
    data: ProjectUpdate,
    current_user: User = Depends(get_current_project_admin)
) -> Any:
    slug = slug.strip().lower()
    id = id.strip().lower()

    if not crud.is_valid_project_admin(current_user, id):
        raise HTTPException(status_code=400, detail="You'r not the admin of the project.")

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid project ID.")

    project = await crud.find_one(slug, id)
    if not project:
        raise_not_found()

    return await crud.update(slug, id, data)


@router.delete("/{id}", response_model=Msg)
async def delete_project(
    slug: str,
    id: str,
    current_user: User = Depends(get_current_project_admin)
) -> Any:
    slug = slug.strip().lower()
    id = id.strip().lower()

    if not crud.is_valid_project_admin(current_user, id):
        raise HTTPException(status_code=400, detail="You'r not the admin of the project.")

    if not ObjectId.is_valid(id):
        raise_bad_request("Not valid license ID.")

    project = await crud.find_one(slug, id)
    if not project:
        raise_not_found()

    return await crud.delete(slug, id)
