from typing import List
from datetime import date, datetime
from pydantic import BaseModel

from models.base import DBModel, WithClient, WithContract, WithLicense
from models.client import Contact
from models.module import Module


# Shared properties
class ProjectBase(BaseModel):
    title: str = None
    description: str = None
    startDate: str = None
    endDate: str = None
    status: str = None
    modules: List[] = []
    simulations: List = []

