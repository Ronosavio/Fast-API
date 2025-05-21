from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, o_authent2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, db:Session = Depends(database.get_db), current_user: int = Depends(o_authent2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote =  models.Vote(post_id=vote.post_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")   
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}
        
    
        