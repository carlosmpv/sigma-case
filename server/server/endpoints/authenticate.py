from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from server.exceptions import invalid_credentials_exception
from server.myjwt import jwt_encode
from server.repository import get_user_repository, UserRepository
from server.repository.users import CreateUserPayload

router = APIRouter()

@router.post("/authenticate")
async def authenticate(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)]
):
    """
    Obtem o access token que deve ser utilizado nos cabeçalhos como `Authorization: Bearer <token>`
    """
    user = await user_repository.find_by_username_and_password(
        form_data.username,
        form_data.password
    )

    if user is None:
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
    """
    Realiza o cadastro do usuário com base em username e password
    """
    await user_repository.create_user(CreateUserPayload(
        username=new_user_request.username, 
        password=new_user_request.password,
    ))