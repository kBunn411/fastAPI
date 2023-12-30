from fastapi import Body, FastAPI, Response, status,HTTPException,Depends,APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
router = APIRouter(
    prefix = "/vote",
    tags = ["Vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_currenet_user)):
        # sets up the scheme     allows us to add into database authenticates/ get the current user
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail = "Post with id {vote.post_id} does not esixt")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    # checks to see if the post has been liked and liked by the user already
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote: #if vote is found rasie error cuz already liked
            raise HTTPException (status_code=status.HTTP_409_CONFLICT, detail = f"user {current_user.id} has already voted on post {vote.post_id}")
        # adds new vote
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote: #vote is not there
            raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail = "Vote does not esixt")
        
        #deletes vote
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "sucessfully deleted vote"}
