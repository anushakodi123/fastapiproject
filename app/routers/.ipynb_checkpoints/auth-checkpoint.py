from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import select, Session

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(database.get_session)):
    user = session.exec(
        select(models.User).where(models.User.email == user_credentials.username)
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with email {user_credentials.username} not found")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    acces_token =  oauth2.create_access_token(data= {"user_id": user.id})

    return {"access_token": acces_token, "token_type": "bearer"}