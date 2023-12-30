from .database import Base
from sqlalchemy import CHAR, DATETIME, TIMESTAMP, Column, ForeignKey,Integer,String,Boolean, UniqueConstraint, text
from sqlalchemy.sql.expression import null
from sqlalchemy.sql import func
from sqlalchemy import Index
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True, server_default=text("IDENTITY(1,1)"))
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='True',nullable = False)
    created_at = Column(DATETIME(timezone=True), nullable= False,server_default=text('GETDATE()'))

    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False )
   #has all of our columns
    owner = relationship("User") #class fetch all of the user information based on the owner_id


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, server_default=text("IDENTITY(1,1)"))
    email = Column(CHAR(255), nullable=False, unique=True)
    passwords = Column(String, nullable=False)
    created_at = Column(DATETIME(timezone=True), nullable= False,server_default=text('GETDATE()'))
    
    
    
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id"),primary_key=True)  #composite keys