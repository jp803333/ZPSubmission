from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from typing import List
from bson import ObjectId
from models.User import User
from database.database import todo_collection
from database.databasehelper.auth import *
from dependencies import *
from models.Todo import Todo


todo_router = APIRouter()


@todo_router.get("/todos")
async def GetAllTodos(token: str = Depends(oauth2_scheme)):
    currentuser = await get_current_user(token)
    listOfTodos: List = []
    async for todo in todo_collection.find({"created_by.username": currentuser.username}):
        listOfTodos.append(Todo(**todo))
    return listOfTodos


@todo_router.get("/todo/{id}")
async def GetATodo(id: str, token: str = Depends(oauth2_scheme)):
    currentuser = await get_current_user(token)
    todo = await todo_collection.find_one({"_id": ObjectId(id), "created_by.username": currentuser.username})
    if todo is not None:
        return Todo(**todo)
    else:
        raise HTTPException(
            status_code=400, detail="Either you dont have permission to see this particular todo or the todo doesnt exists ")


@todo_router.post("/todos")
async def CreateATodo(todo: Todo, token: str = Depends(oauth2_scheme)):
    todo.created_by = await get_current_user(token)
    result = await todo_collection.insert_one(todo.dict())
    creadted_todo = Todo(** await todo_collection.find_one({"_id": result.inserted_id}))
    return creadted_todo


@todo_router.put("/todos/{id}")
async def UpdateATodo(id: str, todo: Todo, token: str = Depends(oauth2_scheme)):
    todoData = await todo_collection.find_one({"_id": ObjectId(id)})
    if todoData is not None:
        user = await get_current_user(token)
        oldtodo = Todo(**todoData)
        created_user = await get_user(oldtodo.created_by.username)
        if created_user == user:
            todo.created_by = oldtodo.created_by
            if not todo.created_at != None:
                todo.created_at = oldtodo.created_at
            updatedTodo = await todo_collection.update_one({"_id": ObjectId(id)}, {"$set": todo.dict()})
            if updatedTodo.modified_count == 1:
                return {"message": "Updated Successfully"}
            else:
                raise HTTPException(
                    status_code=400, detail="Some internal error occured")
        else:
            raise HTTPException(
                status_code=401, detail="You cannot change this todo")
    else:
        return {"message": "Todo doesnt exists of given id "}


@todo_router.delete("/todos/{id}")
async def DeleteATodo(id: str, token: str = Depends(oauth2_scheme)):
    todoData = await todo_collection.find_one({"_id": ObjectId(id)})
    if todoData is not None:
        user = await get_current_user(token)
        todo = Todo(**todoData)
        created_user = await get_user(todo.created_by.username)
        if created_user == user:
            await todo_collection.delete_one({"_id": ObjectId(id)})
            return {"message": "successfully deleted"}
        else:
            raise HTTPException(
                status_code=401, detail="You cannot delete this todo")
    else:
        return {"message": "Todo doesnt exists of given id "}
