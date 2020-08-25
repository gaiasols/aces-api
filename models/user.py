from typing import List
from pydantic import BaseModel, EmailStr, validator
from core.config import (
    PASSWORD_ERROR_MESSAGE,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    USERNAME_ERROR_MESSAGE,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
)
from models.base import DBModel, WithLicense


# Shared properties
class UserBase(BaseModel):
    name: str = None
    username: str = None    # lowercase, isalnum
    email: EmailStr = None
    licenseOwner: bool = False
    verified: bool = False
    disabled: bool = False
    gender: str = None
    phone: str = None
    roles: List[str] = []
    @validator('username')
    def check_username(cls, v):
        v = v.strip().lower()
        if not (USERNAME_MIN_LENGTH <= len(v) <= USERNAME_MAX_LENGTH and v.isalnum()):
            raise ValueError(USERNAME_ERROR_MESSAGE)
        return v
    @validator('email')
    def check_email(cls, v):
        return v.strip().lower()


# Properties to receive when license admin create user
class UserInfo(BaseModel):
    name: str
    username: str
    email: EmailStr
    gender: str = None
    phone: str = None
    password: str
    @validator('username')
    def check_username(cls, v):
        v = v.strip().lower()
        if not (USERNAME_MIN_LENGTH <= len(v) <= USERNAME_MAX_LENGTH and v.isalnum()):
            raise ValueError(USERNAME_ERROR_MESSAGE)
        return v

    @validator('password')
    def check_password(cls, v):
        v = v.strip()
        if not (PASSWORD_MIN_LENGTH <= len(v) <= PASSWORD_MAX_LENGTH):
            raise ValueError(PASSWORD_ERROR_MESSAGE)
        return v


# Properties to receive on create
class UserCreate(UserInfo, WithLicense):
    pass
    # name: str
    # username: str
    # email: EmailStr
    # gender: str = None
    # phone: str = None
    # password: str
    # @validator('username')
    # def check_username(cls, v):
    #     v = v.strip().lower()
    #     if not (USERNAME_MIN_LENGTH <= len(v) <= USERNAME_MAX_LENGTH and v.isalnum()):
    #         raise ValueError(USERNAME_ERROR_MESSAGE)
    #     return v

    # @validator('password')
    # def check_password(cls, v):
    #     v = v.strip()
    #     if not (PASSWORD_MIN_LENGTH <= len(v) <= PASSWORD_MAX_LENGTH):
    #         raise ValueError(PASSWORD_ERROR_MESSAGE)
    #     return v


# Properties to persist in database
class UserSave(UserBase, WithLicense):
    hashed_password: str


# Properties to receive on user update by self
class UserUpdateSelf(BaseModel):
    name: str = None
    gender: str = None
    phone: str = None


# Properties to receive on user update by license
class UserUpdate(BaseModel):
    licenseOwner: bool = None
    disabled: bool = None
    roles: List[str] = None


class User(UserBase, WithLicense, DBModel):
    pass


# class UserInDB(UserBase, WithLicense):
class UserInDB(User):
    hashed_password: str


class UserToSave(UserBase, WithLicense):
    hashed_password: str
