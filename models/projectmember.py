from typing import Any

from pydantic import BaseModel, EmailStr, validator
from models.base import DBModel, WithProject


class MemberBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    role: str = "guest"


class MemberCreate(MemberBase):
    password: str


class Member(MemberBase, WithProject, DBModel):
    pass


class MemberInDB(MemberBase, WithProject):
    hashed_password: str

