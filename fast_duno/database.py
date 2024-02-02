from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_duno.settings import Settings

Settings().DATABASE_URL

engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
