import os
from motor import motor_asyncio

# dbclient = motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
dbclient = motor_asyncio.AsyncIOMotorClient(os.environ['MONGODBURL'])
db: motor_asyncio.AsyncIOMotorClient = dbclient.ZupayTodo
todo_collection: motor_asyncio.AsyncIOMotorCollection = db.todo
user_collection: motor_asyncio.AsyncIOMotorCollection = db.user
