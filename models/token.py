from typing import Any, Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    user: Any


class TokenData(BaseModel):
    username: Optional[str] = None
    license: Optional[str] = None
