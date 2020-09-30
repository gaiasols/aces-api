from typing import List
from datetime import date, datetime
from pydantic import BaseModel

from models.base import DBModel, WithClient, WithLicense
from models.client import Contact


# Module pricing model
class PackagePricing(BaseModel):
    name: str = None
    priceLevel1: int = None
    priceLevel2: int = None
    priceLevel3: int = None


# Shared properties
class ContractBase(BaseModel):
    title: str = None
    startDate: str = None
    endDate: str = None
    terms: str = None
    status: str = None
    type: str = None
    contact: Contact = None
    admin: str = None
    pricing: List[PackagePricing] = []


class ContractRefs(BaseModel):
    license: str
    clientId: str


# Properties to receive on contract creation
class ContractCreate(ContractBase):
    title: str


# Properties to persist in database
class ContractInDB(ContractCreate, WithClient, WithLicense):
    pass


# Properties to receive on contract update
class ContractUpdate(ContractBase):
    pricing: List[PackagePricing] = None
    pass


# Properties to return
class Contract(ContractInDB, DBModel):
    pass
