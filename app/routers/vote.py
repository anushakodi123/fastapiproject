from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from sqlmodel import Session, select
from .. import schemas, database, models, oauth2

router = APIRouter(prefix="/vote", tags=['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, session: Session = Depends(database.get_session), current_user: int = Depends(oauth2.get_current_user)):
    post = session.exec(select(models.Post).where(models.Post.id == vote.post_id)).first()
    vote_query = session.exec(select(models.Vote).where(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
    ))
    found_vote = vote_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{vote.post_id} post doesn't exist")
    

    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{current_user.id} already voted")
        new_vote = models.Vote(post_id= vote.post_id, user_id= current_user.id)
        session.add(new_vote)
        session.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vode doesn't exist")
        session.delete(found_vote)
        session.commit()
        return {"message": "Vote deleted successfully"}
