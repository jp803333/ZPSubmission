from datetime import datetime
from models.User import User
from models.PyObjectId import PyObjectId
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional


class Todo(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    title: str
    done: bool = False
    created_at: datetime = datetime.now()
    created_by: Optional[User]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: lambda v: str(v)}
