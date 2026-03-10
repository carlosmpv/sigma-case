
from base64 import b64encode
import os
from secrets import token_bytes


import jwt
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone

_token_expire_time = timedelta(hours=int(os.getenv('TOKEN_EXPIRE_TIME', 24)))
_secret_key = os.getenv('SECRET_KEY', b64encode(token_bytes(32)).decode('utf-8'))
_jwt_algorithm = os.getenv('JWT_ALGORITHM', 'HS256')

class JWTPayload(BaseModel):
    sub: str
    exp: datetime = datetime.now(timezone.utc) + _token_expire_time

class OAuth2Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

def jwt_decode(access_token: str):
    return jwt.decode(access_token, _secret_key, _jwt_algorithm)

def jwt_encode(sub: str) -> OAuth2Token:
    payload = JWTPayload(sub=sub)
    access_token = jwt.encode(payload.model_dump(), _secret_key, algorithm=_jwt_algorithm)
    return OAuth2Token(access_token=access_token)