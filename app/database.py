from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://postgres:Seneca%4012345%24@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
