import re
from datetime import datetime, timezone
from typing import Any, Optional
from pydantic import BaseConfig, BaseModel, EmailStr, Schema, validator
from bson.objectid import ObjectId


class Msg(BaseModel):
    message: str


class RWModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_alias = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        }


class DBModel(RWModel):
    oid: Optional[Any] = Schema(..., alias="_id")
    @validator("oid")
    @classmethod
    def validate_id(cls, v):
        return str(v)


class WithSlug(BaseModel):
    slug: str


class WithLicense(BaseModel):
    license: str
    @validator("license")
    @classmethod
    def validate_id(cls, v: str):
        return v.strip().lower()


class WithClient(BaseModel):
    client: str


class WithProject(BaseModel):
    project: str
