from typing import List

from pydantic import BaseModel, EmailStr

from models.base import DBModel, WithLicense


class Contact(BaseModel):
    name: str
    phone: str = None
    email: EmailStr = None
    messenger: str = None


# Shared properties
class ClientBase(BaseModel):
    name: str = None
    address: str = None
    phones: List[str] = None
    fax: str = None
    website: str = None
    contacts: List[Contact] = None


# Properties to receive on creation
class ClientCreate(ClientBase):
    name: str


class ClientWithLicense(ClientBase, WithLicense):
    pass


# Properties to receive on update
class ClientUpdate(ClientBase):
    pass


class Client(ClientBase, WithLicense, DBModel):
    pass
