
from sqlalchemy import func
from .. import models, schemas,oauth2
from fastapi import Body, FastAPI, Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from typing import List, Optional

router = APIRouter( 
    prefix= "/posts",
    tags=['Posts']
)
 # response_model=List[schemas.PostOut] works without the response model
@router.get("/",response_model=List[schemas.PostOut]) #/posts in me web browser and I get that message if same path, goes to first one order matters
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_currenet_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
   # cursor.execute("""SELECT * FROM posts """)
    # rows = cursor.fetchall()
    
    
    # got it ot work :)
    # posts = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).order_by(models.Post.id).limit(limit).offset(skip).all()# defualut value is 10 can change in postman by ?limit = num limits how many posts are retrevied # can skip if wanted too needed order_by for the order of the ids
      # gets all the post from the user = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    results = (
    db.query(
        models.Post.id,
        models.Post.title,  # Include the non-aggregated column in GROUP BY
        models.Post.content,
        models.Post.published,
        models.Post.created_at,
        models.Post.owner_id,
        func.count(models.Vote.post_id).label("votes"),
        models.User.id.label("owner_id"),
        models.User.email.label("owner_email"),
        models.User.created_at.label("owner_created_at"),
    )
    .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
    .join(models.User, models.User.id == models.Post.owner_id)
    .filter(models.Post.title.contains(search))
    .group_by(
        models.Post.id,
        models.Post.title,  # Include the non-aggregated column in GROUP BY
        models.Post.content,
        models.Post.published,
        models.Post.created_at,
        models.Post.owner_id,
        models.User.id,
        models.User.email,
        models.User.created_at,  #10:10 chatgbt ask why
        
    ).order_by(models.Post.id)
    .limit(limit)
    .offset(skip)
    .all()
)
    results = list ( map (lambda x : x._mapping, results) ) #read in comments
    return results

  
        ## defalut is left inner join isouter makes it outer and in mysql, thats the default
     # in postmant shows the array


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_currenet_user)): #returns the id  # the user has to be loged in, uses the funtion in oauth2 to see if the token is valid and that the time iis not expired
    # validates and evauatng scheme for us               inside functionpayload: dict = Body(...) extracts fields from body, convert to dictoanry into var payload body is in postman raw Json
    #print(post)  #extract data for us based on whats defined in postman      
   # print(post.dict()) #converts pydantic model to a dictionary
   # post_dict = post.dict() # makes python object which is the dictionary
   # post_dict['id'] = randrange(0,100000000000) #for the id, make it a random value
    #my_posts.append(post_dict) # appeneds it to the array
   # post_dict = jsonable_encoder(post)
   # cursor.execute("INSERT INTO posts (title, content, published) OUTPUT INSERTED.*  VALUES (?, ?, ?);", #Ask about
    #           post_dict['title'], post_dict['content'], post_dict['published'])
    
   
    #conn.commit()
   # inserted_row = cursor.fetchone()


    
    
    #new_post = dict(zip([column[0] for column in cursor.description], inserted_row))

    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) #scheme #passes the owner id for foreign key

    db.add(new_post) #adds to database
    db.commit() #committ the change
    db.refresh(new_post) #put it back into new_post
    return  new_post # returns the new post 
 #"new_posts":f"title {payload['title']} content: {payload['content']} "

#we want a title str, content str,
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int,response : Response,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_currenet_user)): #checks to make sure ths is an int, and for status code
                     #  cursor.execute("""SELECT * from posts WHERE id = ?""",(str(id)))
                       # rows = cursor.fetchall() # ask about why not work with .fetchone
                         #print(rows)
    post2 = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = (
    db.query(
        models.Post.id,
        models.Post.title,  # Include the non-aggregated column in GROUP BY
        models.Post.content,
        models.Post.published,
        models.Post.created_at,
        models.Post.owner_id,
        func.count(models.Vote.post_id).label("votes"),
        models.User.id.label("owner_id"),
        models.User.email.label("owner_email"),
        models.User.created_at.label("owner_created_at"),
    )
    .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
    .join(models.User, models.User.id == models.Post.owner_id)
    .filter(models.Post.id == id)
       .group_by(
        models.Post.id,
        models.Post.title,
        models.Post.content,
        models.Post.published,
        models.Post.created_at,
        models.Post.owner_id,
        models.User.id,
        models.User.email,
        models.User.created_at,
    )
    .first()
    )

    
    






    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, #Http exception is used for if not valid
                           detail = f"post with id: {id} was not found")
        
    
    # post = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    return post

@router.delete("/{id}")
def delete_post(id: int,statuscode=status.HTTP_204_NO_CONTENT, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_currenet_user)): # makes sure id is an int and status code for delete
    
                        # cursor.execute(""" DELETE FROM posts  WHERE id = ? """,(str(id))) # delete works, just dont knowhow to show input on postman
    post_query = db.query(models.Post).filter(models.Post.id == id)
                        #  conn.commit()
                          # delete_post = cursor.fetchall()
                   
                              # index = find_index_post(id) #function that finds the index to be deleted
    post = post_query.first()
    if post == None: #if index not found, raise an error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'Post with id {id} does not exist')
     #remove from array
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    post_query.delete( synchronize_session=False)
    db.commit()
   # return the status code no need to return a value

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id : int, updated_post : schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_currenet_user)): #make sure comes in with right scheme
    
                              #cursor.execute("""UPDATE posts SET title = ?, content = ?, published = ? WHERE id = ?""",(post.title,post.content,post.published,str(id)))
                                #conn.commit()
                             # rows = cursor.fetchone() # Changes everything ask
                                 # index = find_index_post(id) #function that finds the index to be updated
    
    post_query = db.query(models.Post).filter(models.Post.id == id) #query
    post = post_query.first() #runs the query
    if post == None: #if index not found, raise an error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'Post with id {id} does not exist')
    
                  #post_dict = post.dict() # convert to python dict
                 #post_dict['id'] = id # put that id we want to update into the new updated post
               #              my_posts[index] = post_dict # put the dict into the array

     # upost = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]   
    
    if post.owner_id != current_user.id:# makes sure the owner is the person logged in as
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)   
    db.commit()

    return post_query.first()