from fastapi import FastAPI
from routers.todos import todo_router
from routers.auth import auth_router
app = FastAPI()

app.include_router(todo_router, prefix="")
app.include_router(auth_router, prefix="")
