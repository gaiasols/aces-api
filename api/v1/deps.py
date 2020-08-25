from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from core.config import ALGORITHM, SECRET_KEY, API_V1_STR
from crud.user import get_user
from crud.project import is_valid_project_admin
from models.token import TokenData
from models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_V1_STR}/access-token")


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
        raise HTTPException(status_code=400, detail="Inactive user.")
    return current_user


async def get_current_license_owner(current_user: User = Depends(get_current_user)):
    if not current_user.licenseOwner:
        raise HTTPException(status_code=400, detail="Not enough permission.")
    return current_user


async def get_current_license_admin(current_user: User = Depends(get_current_user)):
    if not 'license-admin' in current_user.roles:
        raise HTTPException(status_code=400, detail="Not enough permission.")
    return current_user


async def get_current_project_creator(current_user: User = Depends(get_current_user)):
    if not 'project-creator' in current_user.roles:
        raise HTTPException(status_code=400, detail="Not enough permission.")
    return current_user


async def get_current_project_admin(current_user: User = Depends(get_current_user)):
    if not 'project-admin' in current_user.roles:
        raise HTTPException(status_code=400, detail="Not enough permission.")
    return current_user


# async def get_valid_project_admin(id: str, current_user: User = Depends(get_current_user)):
#     # if not 'project-admin' in current_user.roles:
#     if not is_valid_project_admin(current_user, id):
#         raise HTTPException(status_code=400, detail="Not enough permission.")
#     return current_user

