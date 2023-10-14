from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = { 
    "josuemorales": {
        "username": "josuemorales",
        "full_name": "Josue Morales",
        "email": "josuemoralescam2011@gmail.com",
        "disabled": False,
        "password": "$2a$12$qAe/5/O/1EXLH7Q6s/3sOOELYYLKHKrc6eA/5IlgHdX6OWY5zyAN."
    },
    "josuemorales2": {
        "username": "josuemorales2",
        "full_name": "Josue Morales C",
        "email": "josuemoralescam2012@gmail.com",
        "disabled": True,
        "password": "$2a$12$hcMxhtTzICqsaX4wxWJ.V.gg8wT7ylKkVb4MkstH0GwEPKjC646eC"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])



@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El Usuario no es correcto"
        )
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La contraseña no es correcta"
        )
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)


    return {"access_token": user.username, "token_type": "bearer"}