from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends
from .config import settings
from urllib.parse import quote_plus

encoded_password = quote_plus(settings.database_password)

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{encoded_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def create_db_and_tables():
    ...
    # SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
