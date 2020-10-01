import logging
from typing import Any, List

from fastapi import APIRouter, Body, Depends

from api.v1.deps import get_current_active_user, get_current_project_admin
from crud import projectmodule as crud
from crud import project as project_crud
# from crud.license import find_one as find_license
from models.base import Msg
from models.module import Module, ModuleInfo
from models.project import ProjectModule, ProjectModuleUpdate
from models.user import User
from utils.utils import raise_bad_request, raise_not_found


router = APIRouter()


@router.get("", response_model=List[Any])
async def read_modules(
    project: str,
    current_user: User = Depends(get_current_active_user)
):
    logging.info(">>> " + __name__ + ":read_modules")
    return await crud.read_modules(project)


@router.get("/{id}", response_model=ProjectModule)
async def read_module(
    project: str,
    id: str,
    current_user: User = Depends(get_current_active_user)
):
    logging.info(">>> " + __name__ + ":read_module")
    return await crud.read_module(project, id)

# 5f6ef337d784025cf45ab926 5f6da077b244f3a86bc85ba1

@router.put("/{id}", response_model=ProjectModule)
async def update_module(
    project: str,
    id: str,
    data: ProjectModuleUpdate,
    current_user: User = Depends(get_current_project_admin)
):
    logging.info(">>> " + __name__ + ":update_module")
    if (not data.title) and (not data.description):
        raise_bad_request("Nothing to update")
    return await crud.update_one(project, id, data)


@router.put("/{id}/enable", response_model=ProjectModule)
async def enable_module(
    project: str,
    id: str,
    current_user: User = Depends(get_current_project_admin)
):
    logging.info(">>> " + __name__ + ":enable_module")
    return await crud.enable(project, id, True)


@router.put("/{id}/disable", response_model=ProjectModule)
async def enable_module(
    project: str,
    id: str,
    current_user: User = Depends(get_current_project_admin)
):
    logging.info(">>> " + __name__ + ":enable_module")
    return await crud.enable(project, id, False)


@router.post("/create-group", response_model=Any)
async def create_group(
    project: str,
    group: List[str] = Body(...)
) -> Any:
    return {}
