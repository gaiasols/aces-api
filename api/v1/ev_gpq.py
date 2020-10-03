import logging
from random import shuffle
from typing import Any, List

from fastapi import APIRouter, Depends

from api.v1.deps import get_current_active_user, get_current_project_admin
from crud.persona import find_one as find_persona
from crud.utils import raise_not_found, raise_bad_request
from models.ev.gpq import EvidenceBase, GPQEvidence, GPQRow


router = APIRouter()


@router.post("/{username}")
async def create_evidence_doc(
    project: str,
    username: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    '''TEST'''
    logging.info(">>> " + __name__ + ":create_evidence_doc")
    project = project.strip().lower()
    username = username.strip().lower()
    persona = find_persona(project, username)
    if not persona:
        raise_not_found()

    model = EvidenceBase(
        "license" = current_user.license,
        "projectId" = project,
        "username" = username,
        "fullname" = persona.fullname
    )

    # Check item numbers from project
    # Assume it is 30
    numItems = 30
    rows: List[GPQRow] = []
    seqs = [i for i in range(1, numItems + 1)]
    shuffle(seqs)
    for i in range(numItems):
        rows.append(GPQRow(
            "seq" = i + 1,
            "wbSeq" = seqs[i]
        ))


