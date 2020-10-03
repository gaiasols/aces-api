import logging
from typing import Any, List

from fastapi import APIRouter, Body, Depends

from api.v1.deps import get_current_active_user, get_current_project_admin
# from crud import projectmodule as crud
from crud import persona as crud
from models.base import Msg
from models.user import User
from models.persona import Persona, PersonaCreate, PersonaUpdate
from utils.utils import raise_bad_request, raise_not_found


router = APIRouter()


@router.get("", response_model=List[Persona])
async def read_personas(
    project: str,
    current_user: User = Depends(get_current_active_user)
):
    logging.info(">>> " + __name__ + ":read_personas")
    return await crud.find_many(project)


@router.post("", response_model=Persona)
async def add_persona(
    project: str,
    data: PersonaCreate,
    current_user: User = Depends(get_current_project_admin)
):
    logging.info(">>> " + __name__ + ":add_persona")
    persona = await crud.find_by_email_or_username(project, data.email, data.username)
    logging.info(persona)
    if persona:
        raise_bad_request("Username or email is already registered in the system.")

    return await crud.insert(current_user.license, project, data)


@router.get("/{search}", response_model=Persona)
async def find_persona(
    project: str,
    search: str,
    current_user: User = Depends(get_current_active_user)
):
    logging.info(">>> " + __name__ + ":find_persona")
    persona = await crud.find_one(project, search)
    if not persona:
        raise_not_found("Persona not found.")
    return persona

@router.put("/{search}", response_model=Persona)
async def update_persona(
    project: str,
    search: str,
    data: PersonaUpdate,
    current_user: User = Depends(get_current_project_admin)
):
    logging.info(">>> " + __name__ + ":update_persona")
    return await crud.update_one(project, search, data)


@router.put("/{search}/set-tests", response_model=Persona)
async def set_tests(
    project: str,
    search: str,
    tests: List[str],
    current_user: User = Depends(get_current_project_admin)
):
    logging.info(">>> " + __name__ + ":set_tests")

    persona = await crud.find_one(project, search)
    if not persona:
        raise_not_found("Could not find persona.")

    if len(tests) == 0:
        raise_bad_request("Tests cannot be empty")
    return await crud.set_tests(project, search, tests)


@router.put("/{search}/set-simulations", response_model=Persona)
async def set_simulations(
    project: str,
    search: str,
    sims: List[str],
    current_user: User = Depends(get_current_project_admin)
):
    logging.info(">>> " + __name__ + ":set_simulations")

    if len(sims) == 0:
        raise_bad_request("Sims cannot be empty")
    return await crud.set_simulations(project, search, sims)


# @router.delete("/{search}", response_model=Msg)
async def delete_persona(
    project: str,
    search: str,
    current_user: User = Depends(get_current_project_admin)
):
    logging.info(">>> " + __name__ + ":delete_persona")
    return await crud.delete_one(project, search)


@router.post("/create-test-group", response_model=Any)
async def create_test_group(
    project: str,
    tests: List[str] = Body(...),
    personas: List[str] = Body(...)
) -> Any:
    return None
