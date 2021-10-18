

from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from models.PyObjectId import PyObjectId


class User(BaseModel):
    username: str
    email: Optional[str] = None


class UserInDB(User):
    _id: Optional[PyObjectId]
    hashed_password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: lambda v: str(v)}
