from datetime import datetime
from pydantic import BaseModel, EmailStr, validator

from core.config import (
    LICENSE_TYPES,
    LICENSE_CODE_MIN_LENGTH,
    LICENSE_CODE_MAX_LENGTH,
    LICENSE_CODE_ERROR_MESSAGE,
)
from models.base import DBModel, WithSlug
from utils.utils import is_date


# Shared properties
class LicenseBase(BaseModel):
    type: str = None
    licenseName: str = None
    contactName: str = None
    contactUsername: str = None
    contactEmail: EmailStr = None
    publishedBy: str = None
    publishDate: str = None
    refreshDate: datetime = None
    expiryDate: datetime = None
    disabled: bool = None

    @validator("type")
    @classmethod
    def validate_type(cls, v):
        v = v.strip()
        if not v.lower() in LICENSE_TYPES:
            raise ValueError("Illegal license type")
        return v.lower()

    @validator("publishDate")
    @classmethod
    def validate_publishDate(cls, v):
        v = v.strip()
        if not is_date(v):
            raise ValueError("Date format error")
        return v


# Properties to receive on create
class LicenseCreate(LicenseBase, WithSlug):
    type: str
    licenseName: str
    contactName: str
    contactUsername: str
    contactEmail: EmailStr
    publishedBy: str
    publishDate: str
    disabled: bool = False

    @validator("slug")
    @classmethod
    def validate_slug(cls, v):
        v = v.strip()
        if not (LICENSE_CODE_MIN_LENGTH <= len(v) <= LICENSE_CODE_MAX_LENGTH and v.isalnum()):
            raise ValueError(LICENSE_CODE_ERROR_MESSAGE)
        return v.lower()


# Properties to receive on update (by admin)
class LicenseUpdate(LicenseBase):
    disabled: bool = None


# Properties to receive on update (by license)
class LicenseUpdateSelf(BaseModel):
    licenseName: str = None
    contactName: str = None
    contactEmail: EmailStr = None


class License(LicenseBase, WithSlug, DBModel):
    pass
