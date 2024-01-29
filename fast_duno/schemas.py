from pydantic import BaseModel, ConfigDict, EmailStr

from fast_duno.models import ToDoState


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Message(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ToDoSchema(BaseModel):
    title: str
    description: str
    state: ToDoState


class ToDoPublic(BaseModel):
    id: int
    title: str
    description: str
    state: ToDoState


class ToDoList(BaseModel):
    todos: list[ToDoPublic]


class ToDoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: str | None = None
