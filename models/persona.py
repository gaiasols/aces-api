from typing import Any, List

from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr, Schema, validator

from core.config import USERNAME_ERROR_MESSAGE, USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH
from models.base import DBModel, WithLicense, WithProject


'''
Persona
    tests: gpq, sjt, mate

'''

#
class Battery(BaseModel):
    '''
    Simple module info
    '''
    type: str
    items: int
    touched: int  # last-item


class PersonaBase(BaseModel):
    username: str
    email: EmailStr = None  # Anticipate non-email participants
    @validator('username')
    def check_username(cls, v):
        v = v.strip().lower()
        if not (USERNAME_MIN_LENGTH <= len(v) <= USERNAME_MAX_LENGTH and v.isalnum()):
            raise ValueError(USERNAME_ERROR_MESSAGE)
        return v
    @validator('email')
    def check_email(cls, v):
        if v:
            return v.strip().lower()
        return None


class PersonaInfo(BaseModel):
    fullname: str
    gender: str = None
    birth: str = None
    phone: str = None
    disabled: bool = False
    #
    nip: str = None
    position: str = None
    currentLevel: str = None
    targetLevel: str = None


class WithTest(BaseModel):
    tests: List[str] = []       # gpq-1.0, mate-1.1, etc
    testsPerformed: int = 0
    # testStatus: str = "idle"    # idle, test-name, finished/cancelled
    currentTest: str = None     # gpq or None
    # nextTest: str = None        # Defaulted to first test
    #
    simulations: List[str] = []
    simsPerformed: int = 0
    # simStatus: str = "idle"
    currentSim: str = None
    # nextSim: str = None


class PersonaUpdate(PersonaInfo):
    pass


# class PersonaCreate(WithTest, PersonaInfo, PersonaBase):
#     password: str


class PersonaCreate(BaseModel):
    fullname: str
    username: str
    email: EmailStr = None
    # password: str



class Persona(WithTest, PersonaInfo, PersonaBase, WithProject, WithLicense, DBModel):
    pass


class PersonaInDB(WithTest, PersonaInfo, PersonaBase, WithProject, WithLicense):
    hashed_password: str
