
from os import error
from fastapi import status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from models.User import UserInDB
from database.database import user_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_hash_password(password: str):
    return "fakehashed" + password


def fake_decode_token(token):
    user = get_user(token)
    return user


async def get_user(username: str):
    user = await user_collection.find_one({"username": username})
    if user:
        return UserInDB(**user)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def create_user(username: str, password: str):
    hashed_password = fake_hash_password(password)
    try:
        userResult = await user_collection.insert_one({'username': username, "hashed_password": hashed_password})
    except Exception as e:
        print(e)
    try:
        user = UserInDB(**await user_collection.find_one({"_id": userResult.inserted_id}))
    except Exception as e:
        print(e)

    return user
