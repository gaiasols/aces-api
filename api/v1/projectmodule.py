import logging
from typing import Any, List

from fastapi import APIRouter, Depends

from api.v1.deps import get_current_active_user, get_current_project_admin
from crud import projectmodule as crud
from crud.license import find_one as find_license
from models.base import Msg
from models.module import Module, ModuleInfo
from models.user import User
from utils.utils import raise_bad_request, raise_not_found


router = APIRouter()


@router.get("", response_model=List[Module])
async def read_modules(
    project: str,
    current_user: User = Depends(get_current_active_user)
):
    '''slug: license's slug or * (all)'''
    logging.info(">>> " + __name__ + ":get_project_modules")
    return await crud.find_many(project)


@router.post("", response_model=Module)
async def add_module(
    project: str,
    module: str,
    current_user: User = Depends(get_current_project_admin)
):
    '''
    Required role: project-admin
    '''
    return await crud.insert(project, module)


@router.get("/{id}", response_model=Module)
async def read_module(
    project: str,
    id: str,
    current_user: User = Depends(get_current_active_user)
):
    '''slug: license's slug or * (all)'''
    logging.info(">>> " + __name__ + ":get_project_modules")
    return await crud.find_one(project, id)


@router.put("/{id}", response_model=Module)
async def update_module(
    project: str,
    id: str,
    data: ModuleInfo,
    current_user: User = Depends(get_current_project_admin)
):
    '''slug: license's slug or * (all)'''
    logging.info(">>> " + __name__ + ":get_project_modules")
    return await crud.update_one(project, id, data)


@router.delete("/{id}", response_model=Msg)
async def delete_module(
    project: str,
    id: str,
    current_user: User = Depends(get_current_project_admin)
):
    '''slug: license's slug or * (all)'''
    logging.info(">>> " + __name__ + ":get_project_modules")
    return await crud.delete_one(project, id)
