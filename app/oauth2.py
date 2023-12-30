from jose import JWTError, jwt
from datetime import datetime,timedelta
from fastapi import Depends, status, HTTPException
from . import schemas,database,models
#Secret_key Alogorithm #experiation time
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login') #endpoint

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data : dict): #retrns the token with the expiration date 
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):


    try :
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]) #decode token

        u_id:str =payload.get("user_id") #get the id

        if u_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=u_id) #validate the token data
    except JWTError:
        raise credentials_exception
    return token_data #return the data

def get_currenet_user(token: str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"Could not validate credentials", headers = {"WWW-Authenticate" : "Bearer"})
    
    token = verify_access_token(token,credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user #fetch the uer from the database
    
