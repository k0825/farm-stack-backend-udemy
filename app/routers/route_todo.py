from fastapi import APIRouter
from fastapi import Response, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import Todo, TodoBody, SuccessMsg
from database import (
    db_create_todo,
    db_get_todos,
    db_get_single_todo,
    db_update_todo,
    db_delete_todo,
)
from starlette.status import HTTP_201_CREATED
from typing import List

router = APIRouter()


@router.post("/api/todo", response_model=Todo)
async def create_todo(response: Response, data: TodoBody):
    todo = jsonable_encoder(data)
    res = await db_create_todo(todo)
    response.status_code = HTTP_201_CREATED

    if res:
        return res
    else:
        raise HTTPException(status_code=404, detail="Create task faild")


@router.get("/api/todo", response_model=List[Todo])
async def get_todos():
    res = await db_get_todos()
    return res


@router.get("/api/todo/{id}", response_model=Todo)
async def get_single_todo(id: str):
    res = await db_get_single_todo(id)
    if res:
        return res
    else:
        raise HTTPException(
            status_code=404, detail="Task of ID:{id} doesn't exists"
        )


@router.put("/api/todo/{id}", response_model=Todo)
async def get_update_todo(id: str, data: TodoBody):
    todo = jsonable_encoder(data)
    res = await db_update_todo(id, todo)
    if res:
        return res
    else:
        raise HTTPException(status_code=404, detail="Update task failed")


@router.delete("/api/todo/{id}", response_model=SuccessMsg)
async def get_delete_todo(id: str):
    res = await db_delete_todo(id)
    if res:
        return {"message": "Successfully deleted"}
    else:
        raise HTTPException(status_code=404, detail="Delete task failed")
