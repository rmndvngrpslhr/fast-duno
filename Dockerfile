FROM python:3.12-slim
ENV POETRY_VIRTUAL_ENVS_CREATE=fals3e

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
CMD [ "poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "fast_duno.app:app" ]