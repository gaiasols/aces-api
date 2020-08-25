import logging
from datetime import datetime, timedelta
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

from api.v1.deps import get_current_user, get_current_active_user, get_current_license_owner
from core.config import (ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, DOCTYPE_USER,
                         SECRET_KEY)
from core.security import (create_access_token, get_password_hash,
                           verify_password)
from crud.user import get_by_email, authenticate_user
from db.mongo import get_collection
from models.base import Msg
from models.token import Token, TokenData
from models.user import User, UserInDB
from utils import emailutils


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")


router = APIRouter()


@router.post("/access-token", response_model=Token)
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
        "roles": user.roles,
        "token": access_token,
    }
    return {"access_token": access_token, "token_type": "bearer", "user": user_data}


@router.get("/users/me", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/test")
async def send_new_account_email(email_to: str, username: str, password: str):
    logging.info("send_new_account_email")
    emailutils.send_new_account_email(email_to, username, password)

# def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:

@router.post("/password-recovery/{email}", response_model=Msg)
async def recover_password(email: str) -> Any:
    """
    Password Recovery
    """
    user = await get_by_email(email=email)
    logging.info(user)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = emailutils.generate_password_reset_token(email=email)
    emailutils.send_reset_password_email(
        email_to=user["email"], email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}
