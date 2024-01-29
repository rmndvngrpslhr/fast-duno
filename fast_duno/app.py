from fastapi import FastAPI

from fast_duno.routes import auth, todos, users

app = FastAPI()


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)


@app.get('/')
def read_root():
    return {'message': 'Olá, Mundo!'}
