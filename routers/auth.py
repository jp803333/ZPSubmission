from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from database.databasehelper.auth import *
from dependencies import *
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database.databasehelper.auth import create_user
from database.databasehelper.auth import get_user, fake_hash_password
from models.User import UserInDB


auth_router = APIRouter()


@auth_router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user: UserInDB = await get_user(form_data.username)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="Server issue")
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@auth_router.post("/signup")
async def singup(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user: UserInDB = await create_user(form_data.username, form_data.password)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="Server issue")
    if not user:
        raise HTTPException(
            status_code=400, detail="Error creating your account")
    return {"access_token": user.username, "token_type": "bearer"}
