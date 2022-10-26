from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os

# SECRET_KEY = 'a35ae5dd7358614df9bc97c6290780cf9c30164b012373ee53c4b0fee249c7fb'
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_token_data(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # decodifica el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        payload['token'] = token
        print(payload)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return payload