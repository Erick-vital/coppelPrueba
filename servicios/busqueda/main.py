from fastapi import FastAPI
import hashlib
from datetime import datetime
import requests, json

app = FastAPI()
PUBLIC_KEY = 'e1429dae3a1dd7faece307505aa8c362'
PRIVATE_KEY = '32f411e8645f6f852cbfbea0dc0bd15ec5a34492'

def create_hash(public_key, private_key, time_stamp):
    string = time_stamp

@app.get("/searchComics/")
async def search_comics(buscar = 'personajes', nombre = None):
    ts = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
    cadena = ts + PRIVATE_KEY + PUBLIC_KEY
    hash = hashlib.md5(cadena.encode()).hexdigest()

    if buscar == 'personajes' and not nombre:
        url = f'https://gateway.marvel.com:443/v1/public/characters?ts={ts}&apikey={PUBLIC_KEY}&hash={hash}'
    elif buscar == 'personajes' and nombre:
        url = f'https://gateway.marvel.com:443/v1/public/characters?name={nombre}&ts={ts}&apikey={PUBLIC_KEY}&hash={hash}'
    elif buscar == 'comics' and not nombre:
        url = f'https://gateway.marvel.com:443/v1/public/comics?ts={ts}&apikey={PUBLIC_KEY}&hash={hash}'
    elif buscar == 'comics' and nombre:
        url = f'https://gateway.marvel.com:443/v1/public/comics?title={nombre}&ts={ts}&apikey={PUBLIC_KEY}&hash={hash}'

    print(url)
    r = requests.get(url)
    js = json.loads(r.text)
    resultados = js['data']['results']

    if buscar == 'personajes':
        personajes = []
        for personaje in resultados:
            personajes.append({
                'id': personaje['id'],
                'name': personaje['name'],
                'image': personaje['thumbnail']['path'],
                'appearances': len(personaje['comics']['items'])
            })
        return {"data": json.loads(json.dumps(personajes))}
    elif buscar == 'comics':
        comics = []
        for comic in resultados:
            comics.append({
                'id': comic['id'],
                'title': comic['title'],
                'image': comic['thumbnail']['path'],
                'OnSaleDate': comic['dates'][0]['date']
            })
        return {"data": json.loads(json.dumps(comics))}