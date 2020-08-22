import logging
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends, APIRouter, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

from core.config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, DOCTYPE_USER, SECRET_KEY
from core.security import create_access_token, get_password_hash, verify_password
from crud.user import find_one as find_user
from db.mongo import get_collection
from models.token import Token, TokenData
from models.user import User, UserInDB

# ALGORITHM = "HS256"
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")


router = APIRouter()


async def get_user(username: str):
    user = await find_user(username)
    if user:
        return UserInDB(**user)


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    user_data = {
        "id": user.oid,
        "license": user.license,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "licenseOwner": user.licenseOwner,
        "verified": user.verified,
        "disabled": user.disabled,
        "userRoles": user.userRoles,
        "token": access_token,
    }
    return {"access_token": access_token, "token_type": "bearer", "user": user_data}


@router.get("/users/me", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


from models.license import License
from crud.license import find_one as find_license
@router.get("/test-license", response_model=License)
async def test_license(current_user: User = Depends(get_current_active_user)):
    license = await find_license(current_user.license)
    return license
