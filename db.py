from sqlmodel import Session, create_engine
from typing import Annotated
from fastapi import Depends

SQLLITE_NAME = "db.sqlite3"
SQLITE_URL = f"sqlite:///{SQLLITE_NAME}"


engine = create_engine(SQLITE_URL)

def get_session():
    with Session(engine) as session:
        yield session

Sessiondep = Annotated[Session, Depends(get_session)]

