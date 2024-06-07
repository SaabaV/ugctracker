from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
from pydantic import BaseModel
from django.conf import settings
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
# Секретный ключ, который используется для подписи JWT токенов
TOKEN_SECRET_KEY = env('TOKEN_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return {"user_id": user_id}
    except JWTError:
        raise credentials_exception


class TokenData(BaseModel):
    username: Union[str, None] = None


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
