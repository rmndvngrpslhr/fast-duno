#!/bin/sh

<<<<<<< HEAD
poetry run alembic upgrade head

poetry run uvicorn --host 0.0.0.0 --port 8000 fast_duno.app:app
=======
# Executa as migrações do banco de dados
poetry run alembic upgrade head

# Inicia a aplicação
poetry run uvicorn --host 0.0.0.0 --port 8000 fast_duno.app:app
>>>>>>> 4a92694ac858e9c86263e19d6cfdce9ea6b6d813
