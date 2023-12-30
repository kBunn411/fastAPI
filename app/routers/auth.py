from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..import database, schemas, models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags= ['Authentication'])

@router.post('/login',response_model=schemas.Token) # router for authentication
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    #username = is like the email in our case
    #password =

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() #query

    if not user: # if email is wrong
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Invalid Credentials")
     # if passwords doesn't match
    if not utils.verify(user_credentials.password,user.passwords):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Invalid Credentials")
    
    
    access_token = oauth2.create_access_token(data = {"user_id":user.id}) #gets the toen using the user_id
    return {"access_token" : access_token, "token_type": "bearer"}

# in postman was are in form data and just use username and password
