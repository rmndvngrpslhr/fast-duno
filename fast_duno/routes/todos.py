from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_duno.database import get_session
from fast_duno.models import ToDo, User
from fast_duno.schemas import (
    Message,
    ToDoList,
    ToDoPublic,
    ToDoSchema,
    ToDoUpdate,
)
from fast_duno.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=ToDoList)
def list_todos(
    user: CurrentUser,
    session: Session = Depends(get_session),
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(ToDo).where(ToDo.user_id == user.id)

    if title:
        query = query.filter(ToDo.title.contains(title))

    if description:
        query = query.filter(ToDo.description.contains(description))

    if state:
        query = query.filter(ToDo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}


@router.post('/', response_model=ToDoPublic)
def create_todo(
    todo: ToDoSchema,
    user: CurrentUser,
    session: Session = Depends(get_session),
):
    db_todo: ToDo = ToDo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.patch('/{todo_id}', response_model=ToDoPublic)
def patch_todo(
    todo_id: int,
    todo: ToDoUpdate,
    user: CurrentUser,
    session: Session = Depends(get_session),
):
    db_todo = session.scalar(
        select(ToDo).where(ToDo.user_id == user.id, ToDo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(status_code=404, detail='Task not found')

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(
    todo_id: int, user: CurrentUser, session: Session = Depends(get_session)
):
    todo = session.scalar(
        select(ToDo).where(ToDo.user_id == user.id), ToDo.id == todo_id
    )

    if not todo:
        raise HTTPException(status_code=404, detail='Task not found.')

    session.delete(todo)
    session.commit()

    return {'detail': 'Task has been deleted successfully.'}
