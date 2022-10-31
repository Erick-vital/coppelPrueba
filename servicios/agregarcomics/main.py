from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from dependencias.dependencias import get_token_data
from client_rpc import RpcClient
import json, requests
from bson.json_util import dumps
from config.db import mycol

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
    return {"access_token": token.decode(), "token_type": "bearer"}

@app.post("/addToLayaway")
async def post_comics(nombre = None, token: str = Depends(get_token_data)):

    if not nombre:
        r = requests.get('http://host-busqueda:8005/searchComics/?buscar=comics')
    else:
        r = requests.get(f'http://host-busqueda:8005/searchComics/?buscar=comics&nombre={nombre}')
    usuario = token['sub']

    x = mycol.find({'name': usuario})
    data_json = json.loads(dumps(x))
    mycol.update_one({"name": usuario}, {"$set": {'comics': json.loads(r.text)['data']}})
    return {'data': json.loads(r.text), 'user_id': data_json[0]['_id']['$oid']}


@app.get("/user_data")
async def get_comics(token: str = Depends(get_token_data)):
    usuario = token['sub']
    x = mycol.find({'name': usuario})
    data_json = json.loads(dumps(x))

    return {"message": data_json}

@app.get("/")
async def root():
    return {"message": "Hello Mundooooo"}

