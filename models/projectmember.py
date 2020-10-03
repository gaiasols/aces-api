from typing import Any

from pydantic import BaseModel, EmailStr, validator

from core.config import (
    USERNAME_ERROR_MESSAGE,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH
)
from models.base import DBModel, WithProject


class MemberBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    role: str = "guest"

    @validator('username')
    def check_username(cls, v):
        v = v.strip().lower()
        if not (USERNAME_MIN_LENGTH <= len(v) <= USERNAME_MAX_LENGTH and v.isalnum()):
            raise ValueError(USERNAME_ERROR_MESSAGE)
        return v

    @validator('email')
    def check_email(cls, v):
        return v.strip().lower()


class MemberCreate(MemberBase):
    # password: str
    pass


class Member(MemberBase, WithProject, DBModel):
    pass


class MemberInDB(MemberBase, WithProject):
    hashed_password: str

