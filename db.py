from sqlmodel import Session, create_engine, SQLModel
from typing import Annotated
from fastapi import Depends, FastAPI

SQLLITE_NAME = "db.sqlite3"
SQLITE_URL = f"sqlite:///{SQLLITE_NAME}"

engine = create_engine(SQLITE_URL)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

Sessiondep = Annotated[Session, Depends(get_session)]

