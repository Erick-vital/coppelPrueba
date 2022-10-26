from tkinter import W
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from client_rpc import RpcClient
import json, requests

app = FastAPI()

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # posiblemente lleva await
    r_client = RpcClient()
    user_data = {
        'username': form_data.username,
        'password': form_data.password,
    }
    print(user_data)
    print(type(user_data))
    token = r_client.call(json.dumps(user_data))
    return token.decode()

@app.get("/comic")
async def get_comics():
    r = requests.get('http://host-busqueda:8005/searchComics/?buscar=personajes')
    return r.text


@app.get("/")
async def root():
    return {"message": "Hello Mundooooo"}

