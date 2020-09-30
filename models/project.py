from typing import List
from datetime import date, datetime
from pydantic import BaseModel, validator

from models.base import DBModel, WithClient, WithContract, WithLicense
from models.client import Contact
from models.module import Module
from utils.utils import is_date


class ProjectModule(BaseModel):
    ref: str
    type: str
    version: str
    method: str
    name: str
    title: str = None   # Marketing name
    description: str = None
    items: int
    url: str = None
    enabled: bool = False


class ProjectModuleUpdate(BaseModel):
    title: str = None
    description: str = None


# Shared properties
class ProjectInfo(BaseModel):
    title: str
    description: str = None
    startDate: str = None
    endDate: str = None
    status: str = None
    contact: str = None
    admin: str = None

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


class ProjectRefs(BaseModel):
    license: str
    clientId: str = None
    contractId: str = None



# Shared properties
class ProjectBase(ProjectInfo, ProjectRefs):
    createdBy: str = None
    modules: List[ProjectModule] = []
    settings: List[str] = []


# Properties to persist in database
class ProjectInDB(ProjectBase):
    admin: str
    createdBy: str
    pass


class Project(ProjectBase, DBModel):
    pass


# Properties to receive on project creation
class ProjectCreate(ProjectInfo):
    # title: str
    # description: str = None
    # startDate: str = None
    # endDate: str = None
    # status: str = None
    # contact: str = None
    # admin: str = None
    pass


# Properties to receive on update
class ProjectUpdate(ProjectInfo):
    title: str = None

