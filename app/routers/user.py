from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from sqlmodel import select, Session
from .. import schemas, models
from ..database import get_session
from ..utils import hash

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, session: Session = Depends(get_session)):
    user = session.get(models.User, id)
    if not user:
         raise HTTPException(status_code=404, detail="Invalid Credentials")
    return user
