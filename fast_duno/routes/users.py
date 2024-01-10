from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_duno.database import get_session
from fast_duno.models import User
from fast_duno.schemas import Message, UserList, UserPublic, UserSchema
from fast_duno.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=UserList)
def read_users(session: Session, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return {'users': users}


@router.post('/', response_model=UserPublic, status_code=201)
def create_user(session: Session, user: UserSchema):
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )
    if db_user:
        raise HTTPException(
            status_code=400, detail='Username already registered'
        )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username, password=hashed_password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    session: Session,
    user_id: int,
    user: UserSchema,
    current_user: CurrentUser,
):

    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')
    if current_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    current_user.username = user.username
    current_user.password = user.password
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):

    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    if current_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    session.delete(current_user)
    session.commit()

    return {'detail': 'User deleted'}
