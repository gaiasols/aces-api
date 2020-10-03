import logging
from typing import Any, List

from fastapi import APIRouter, Depends

from api.v1.deps import get_current_active_user, get_current_project_admin
# from crud import projectmodule as crud
from crud import projectmember as crud
from models.base import Msg
from models.projectmember import Member, MemberBase, MemberCreate, MemberInDB
from models.user import User
from utils.utils import raise_bad_request, raise_not_found


router = APIRouter()


@router.get("", response_model=List[Member])
async def read_members(
    project: str,
    current_user: User = Depends(get_current_active_user)
):
    logging.info(">>> " + __name__ + ":read_members")
    return await crud.find_many(project)


@router.post("", response_model=Member)
async def add_member(
    project: str,
    data: MemberCreate,
    current_user: User = Depends(get_current_project_admin)
):
    logging.info(">>> " + __name__ + ":add_member")
    member = await crud.find_by_email_or_username(project, data.email, data.username)
    logging.info(member)
    if member:
        raise_bad_request("Username or email is already registered in the system.")

    return await crud.insert(project, data)


@router.get("/{search}", response_model=Member)
async def find_member(
    project: str,
    search: str,
    current_user: User = Depends(get_current_active_user)
):
    '''slug: license's slug or * (all)'''
    logging.info(">>> " + __name__ + ":get_project_modules")
    return await crud.find_one(project, search)


@router.delete("/{search}", response_model=Msg)
async def delete_member(
    project: str,
    search: str,
    current_user: User = Depends(get_current_project_admin)
):
    logging.info(">>> " + __name__ + ":delete_member")
    return await crud.delete_one(project, search)
