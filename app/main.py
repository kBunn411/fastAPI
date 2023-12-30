import time
from typing import Optional,List
from fastapi import Body, FastAPI, Response, status,HTTPException,Depends
from fastapi.encoders import jsonable_encoder #used to get different warnings like 404 not found
from pydantic_settings import BaseSettings #use to make sure the data input is the input we want
from random import randrange
import pyodbc
from sqlalchemy.orm import Session
from . import models, schemas,utils
from . database import engine,SessionLocal,get_db

from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine) #creates the database


#origins = ["https://www.google.com"] can talk to google.com
# CORE STUFF IMPORTANT
app = FastAPI()

 #app.add_middleware(
  #  CORSMiddleware, #FUNCTION RUNS BEFORE EVERY REQUEST
  #  allow_origins=origins, #specify which domains can talk to api
  #  allow_credentials=True,
  #  allow_methods=["*"], #all certein methids lie get, post etc
  #  allow_headers=["*"],
#)



app.include_router(post.router)
# request goes to see what the code is in the router file
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": "successful"}


@app.get("/")  #path operation/route makes it into the path operation decoratoer / is path we go to in url
def root(): # name of function doesnt rlly matter
    return {"message": "Welcome to my APIIIIII"} #data sent back to the user


