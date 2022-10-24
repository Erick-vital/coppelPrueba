from datetime import datetime, timedelta
from http.client import HTTPException
from urllib import response
from fastapi import APIRouter, status, Depends, HTTPException
from models.usermodel import UserRequest
from passlib.context import CryptContext
#from config.example import mycol
import json 
from bson.json_util import dumps
from jose import JWTError, jwt
from typing import Union
from models.token import Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = 'a35ae5dd7358614df9bc97c6290780cf9c30164b012373ee53c4b0fee249c7fb'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

from pymongo import MongoClient, errors

DOMAIN = 'localhost'
PORT = 27017

try:
    client = MongoClient(
        host = [DOMAIN + ':' + str(PORT)],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
        username = 'root',
        password = 'admin'
    )
    # print the version of MongoDB server if connection successful
    print ("server version:", client.server_info()["version"])

    mydb = client['mydatabase']
    mycol = mydb["customers"]
    # mydict = { "name": "John", "address": "Highway 37" }

    # x = mycol.insert_one(mydict)

    # get the database_names from the MongoClient()
    database_names = client.list_database_names()
except errors.ServerSelectionTimeoutError as err:
    # set the client and DB name list to 'None' and `[]` if exception
    client = None
    database_names = []

    # catch pymongo.errors.ServerSelectionTimeoutError
    print ("pymongo ERROR:", err)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Verifica que el hash sea correcto
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Crea hash de la contrasena
def get_password_hash(password):
    return pwd_context.hash(password)

# Obtiene el hash insertado en la db
def get_user_from_db(username: str):
    usuario_cursor = mycol.find({"name": username})
    list_cursor = list(usuario_cursor)
    json_data = dumps(list_cursor)
    return {'username': json.loads(json_data)[0]['name'], 'hash':json.loads(json_data)[0]['password']}

# autentica al usuario mediante el hash
def authenticate_user(username: str, password: str):
    hash = get_user_from_db(username)['hash']
    user = get_user_from_db(username)['username']
    if not hash:
        return False
    if not verify_password(password, hash):
        return False
    return user
    

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

# Obtiene el token y lo valida usando la private key
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


@router.post('/user/', status_code=status.HTTP_201_CREATED)
async def post_user(usuario: UserRequest):
    hash = get_password_hash(usuario.password)
    print(hash)
    #print(verify_password(usuario.password, hash))
    x = mycol.insert_one({
        "name" : usuario.nombre,
        "password": hash,
        "age": usuario.edad
    })
    print(x.inserted_id)
    return {"usuario creado" : str(x.inserted_id)}

@router.post('/user/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/users', status_code=status.HTTP_200_OK)
async def get_usuarios(token: str = Depends(get_token_data)):
    usuario_cursor = mycol.find({"name": token['sub']})
    list_cursor = list(usuario_cursor)
    json_data = json.loads(dumps(list_cursor))
    user_data = {
        'id': json_data[0]['_id']['$oid'],
        'name': json_data[0]['name'],
        'age': json_data[0]['age'],
        'token': token['token']
    }
    return user_data