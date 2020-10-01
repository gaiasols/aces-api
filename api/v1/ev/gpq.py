import logging
from typing import Any, List

from fastapi import APIRouter, Depends

from api.v1.deps import get_current_active_user, get_current_project_admin
from crud.ev import gpq as crud
from crud.persona import find_one as find_persona
from crud.utils import raise_not_found, raise_bad_request, raise_server_error
from models.ev.gpq import EvidenceBase, GPQEvidence, GPQRow, GPQRowUpdate
from models.user import User


router = APIRouter()

# 5f6ef337d784025cf45ab926 5f724e7219f6ec85e8f3a9f2
@router.get("/{personaId}", response_model=GPQEvidence)
async def read_evidence_doc(
    project: str,
    personaId: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    logging.info(">>> " + __name__ + ":read_evidence_doc")
    doc = await crud.find_one(project, personaId)
    if not doc:
        raise_not_found()
    return doc


@router.post("/{personaId}", response_model=GPQEvidence)
async def create_evidence_doc(
    project: str,
    personaId: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    '''TEST'''
    logging.info(">>> " + __name__ + ":create_evidence_doc")
    projectId = project.strip().lower()
    personaId = personaId.strip().lower()

    # Check if persona exists
    persona = await find_persona(projectId, personaId)
    if not persona:
        raise_not_found("Could not find persona.")

    # Check if doc has been created before
    doc = await crud.find_one(projectId, personaId)
    if doc:
        raise_server_error("Doc already exists in the sytem.")

    fullname = persona["fullname"]
    doc = await crud.create_doc(current_user.license, projectId, personaId, fullname)
    return doc


# 5f6ef337d784025cf45ab926 5f70ec59010bd033f07fd3a6 5f7384534a4ca28e3b04d199
@router.put("/{personaId}/init", response_model=Any)
async def init(
    project: str,
    personaId: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    '''CAUTION: For test only. It should only be called by Persona.'''
    logging.info(">>> " + __name__ + ":init")
    return await crud.init(project, personaId)


@router.put("/{personaId}/start", response_model=Any)
async def start(
    project: str,
    personaId: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    '''CAUTION: For test only. It should only be called by Persona.'''
    logging.info(">>> " + __name__ + ":start")
    return await crud.start(project, personaId)


@router.post("/{personaId}/post", response_model=Any)
async def post(
    project: str,
    personaId: str,
    data: GPQRowUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    '''CAUTION: For test only. It should only be called by Persona.'''
    logging.info(">>> " + __name__ + ":post")
    return await crud.update_row(project, personaId, data)

'''
{
  "seq": 1,
  "wbSeq": 3,
  "total": 30,
  "element": "GG",
  "statement": "Gudang Garam",
  "lastTouch": 1601398997371
}
{
  "touched": 1601399787274
}

5f7384534a4ca28e3b04d199
'''