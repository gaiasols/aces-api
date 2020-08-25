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
    contact: str = None

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
    # admin: str
    # Will be created first with creator as admin


class ProjectRefs(BaseModel):
    # license: str
    client: str = None
    contract: str = None


# Properties to persist in database
class ProjectInDB(ProjectBase, ProjectRefs, WithLicense):
    admin: str
    createdBy: str
    pass


class Project(ProjectInDB, DBModel):
    pass


# Properties to receive on update
class ProjectUpdate(ProjectBase, ProjectRefs):
    admin: str = None
    pass

