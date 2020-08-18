from pydantic import BaseModel, validator

from core.config import BEHAVIORAL_MODULE_TYPES, BEHAVIORAL_MODULE_METHODS
from models.base import DBModel


# Shared properties
class ModuleBase(BaseModel):
    type: str = None
    version: str = None
    method: str = None
    name: str = None    # Formal name
    title: str = None   # Marketing name
    description: str = None
    items: int = None
    url: str = None

    @validator("type")
    @classmethod
    def validate_type(cls, v):
        v = v.strip().lower()
        if not v in BEHAVIORAL_MODULE_TYPES:
            raise ValueError("Illegal module type.")
        return v
    @validator("method")
    @classmethod
    def validate_method(cls, v):
        v = v.strip().lower()
        if not v in BEHAVIORAL_MODULE_METHODS:
            raise ValueError("Illegal module type.")
        return v


# Properties to receive on creation
class ModuleCreate(ModuleBase):
    type: str
    version: str
    method: str
    name: str
    items: int


# Properties to receive on update (ACES only)
class ModuleUpdate(ModuleBase):
    pass


# Properties to receive on update by licensee
class ModuleInfo(BaseModel):
    title: str = None
    description: str = None


# Properties to return to client
class Module(ModuleBase, DBModel):
    pass
