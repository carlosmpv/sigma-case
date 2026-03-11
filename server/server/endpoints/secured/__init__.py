from fastapi import APIRouter, Depends
from typing import Annotated

import jwt
from server.exceptions import invalid_credentials_exception
from fastapi import Depends, HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from server.myjwt import jwt_decode
from .products import router as products_router
from .map import router as map_router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate")

async def get_current_userid(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt_decode(token)
    except jwt.InvalidTokenError:
        raise invalid_credentials_exception

    userid = payload.get('sub')
    if userid is None:
        raise invalid_credentials_exception
    
    return userid


secured_router = APIRouter(
    prefix="/secured",
    dependencies=[
        Depends(get_current_userid)
    ],
)


secured_router.include_router(products_router)
secured_router.include_router(map_router)
