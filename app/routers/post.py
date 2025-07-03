from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from sqlmodel import select, Session, func
from .. import schemas, models
from ..database import get_session
from .. import oauth2
from typing import List
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[schemas.PostWithVotes])
def get_posts(
    session: Session = Depends(get_session),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: str = ""
):
    statement = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .where(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .options(selectinload(models.Post.user))
    )
    results = session.exec(statement).all()

    response = []
    for post, vote_count in results:
        response.append({
            "Post": post,
            "votes": vote_count
        })

    return response

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: models.Post, session: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, session: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    # post = session.get(models.Post, post_id)
    statement = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .where(models.Post.id == post_id)
        .options(selectinload(models.Post.user))  # eager load user
    )

    post = session.exec(statement).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    return post

@router.delete("/{post_id}")
def delete_post(post_id: int, session: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    post = session.get(models.Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform reqested action")
    session.delete(post)
    session.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, session: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    print("curennnttt", current_user)
    post_db = session.get(models.Post, post_id)
    if not post_db:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    post_data = post.model_dump(exclude_unset=True)
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform reqested action")
    post_db.sqlmodel_update(post_data)
    session.add(post_db)
    session.commit()
    session.refresh(post_db)
    return post_db
