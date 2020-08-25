from typing import List
from datetime import date, datetime
from pydantic import BaseModel, validator

from models.base import DBModel, WithClient, WithContract, WithLicense
from models.client import Contact
from models.module import Module
from utils.utils import is_date


# Shared properties
class ProjectBase(BaseModel):
    title: str = None
    description: str = None
    startDate: str = None
    endDate: str = None
    status: str = None
    contact: str = None     # Nama PIC klien
    managedBy: str = None   # Nama
    # modules: List[Module] = []

    @validator("startDate")
    @classmethod
    def validate_start_date(cls, v):
        if not v:
            return None
        v = v.strip()
        if not is_date(v):
            raise ValueError("Date format error")
        return v

    @validator("endDate")
    @classmethod
    def validate_end_date(cls, v):
        if not v:
            return None
        v = v.strip()
        if not is_date(v):
            raise ValueError("Date format error")
        return v


# Properties to receive on project creation
class ProjectCreate(ProjectBase):
    title: str
    managedBy: str



# Properties to receive on update
class ProjectUpdate(ProjectBase):
    pass


# Properties to receive as simple project info
class ProjectInfo(ProjectBase, WithLicense, WithContract, WithClient, DBModel):
    # modules: int = 0
    pass


# Properties to persist in database
class ProjectInDB(ProjectCreate, WithLicense, WithContract, WithClient):
    modules: List[Module] = []

# Properties to return
class Project(ProjectInDB, DBModel):
    pass
