from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from pwdlib import PasswordHash
from pydantic import BaseModel
from server.exceptions import invalid_credentials_exception
from server.myjwt import jwt_encode
from server.repository import get_user_repository, UserRepository

password_hash = PasswordHash.recommended()
router = APIRouter()

@router.post("/authenticate")
async def authenticate(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)]
):

    username = form_data.username
    user = await user_repository.find_by_username(username)
    if user is None:
        raise invalid_credentials_exception
    
    if not password_hash.verify(form_data.password, user.passhash):
        raise invalid_credentials_exception
    
    return jwt_encode(str(user.uuid))

class NewUserRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    new_user_request: NewUserRequest,
):
    username = new_user_request.username
    passhash = password_hash.hash(new_user_request.password)
    await user_repository.create_user(username, passhash)