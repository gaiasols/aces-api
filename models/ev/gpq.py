from typing import List

from models.base import BaseModel, DBModel, WithLicense, WithProject
from models.ev.evidence import EvidenceBase


class GPQRow(BaseModel):
    seq: int
    wbSeq: int             # nomer urut di workbook
    element: str = None     # simbol elemen
    statement: str = None   # Lorem ipsum...
    saved: int = None       # time when record was saved
    elapsed: int = None     # elapsed time since previous touch event


class GPQRowUpdate(BaseModel):
    seq: int
    wbSeq: int
    total: int
    element: str
    statement: str
    lastTouch: int



class GPQEvidenceCreate(EvidenceBase):
    sequence: str
    rows: List[GPQRow] = []


# class GPQEvidence(EvidenceBase, WithProject, WithLicense, DBModel):
class GPQEvidence(GPQEvidenceCreate, DBModel):
    pass
