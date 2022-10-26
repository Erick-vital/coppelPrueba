from fastapi import FastAPI, Depends
from routers import users
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware  
from routers.users import login_for_access_token

app = FastAPI()

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # posiblemente lleva await
    token = login_for_access_token(form_data)
    return token
