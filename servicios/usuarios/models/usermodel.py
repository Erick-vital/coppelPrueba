from pydantic import BaseModel

class UserRequest(BaseModel):
    nombre: str 
    password: str 
    edad: int