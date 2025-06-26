from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from sqlmodel import select, Session
from .. import schemas, models
from ..database import get_session

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/")
def get_posts(session: Session = Depends(get_session)):
    posts = session.exec(select(models.Post)).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: models.Post, session: Session = Depends(get_session)):
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(models.Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    return post

@router.delete("/{post_id}")
def delete_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(models.Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    session.delete(post)
    session.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, session: Session = Depends(get_session)):
    post_db = session.get(models.Post, post_id)
    if not post_db:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    post_data = post.model_dump(exclude_unset=True)
    post_db.sqlmodel_update(post_data)
    session.add(post_db)
    session.commit()
    session.refresh(post_db)
    return post_db
