from typing import Optional
from pydantic import BaseModel,EmailStr, conint
from datetime import datetime



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #defaluts to True if not given a value optional value
    # rating: Optional[int] = None # fully optional field


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True
    
   


class UserCreate(BaseModel):
    email: EmailStr
    passwords: str






class UserLogin(BaseModel):
     email: EmailStr
     passwords: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None #had to change this from str to int

class Vote(BaseModel):
    post_id : int
    dir: conint(ge=0, le=1)


class PostOut(BaseModel):
    id: int
    title : str
    content: str
    published : bool
    created_at: datetime
    owner_id: int
    owner_email: EmailStr
    owner_created_at:  datetime
    votes: int

    
    