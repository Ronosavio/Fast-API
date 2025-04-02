from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


       

# while True:
#    try:
#       conn = psycopg2.connect(host = 'localhost', database= 'postgres', user = 'postgres', password = '1234', cursor_factory=RealDictCursor)
#       cursor = conn.cursor()
#       print('database connection was successful')
#       break
#    except Exception as error:
#       print("Connecting to a database failed")
#       print("Error: ", error)
#       time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favourite food", "content": "I like pizza", "id": 2}]

def find_post(id):
   for p in my_posts:
      if p['id'] == id:
         return  p
      
def find_index(id):
   for i , p in enumerate(my_posts):
       if p['id'] == id:
          return i
       
      
#path operation
@app.get("/")
def root():
   return{"message : Welcome to my api!!"}

@app.get("/login") 
def login():
    return {"You have entered the login page"}
 
@app.get("/posts", response_model= List[schemas.Post])
def posts(db: Session = Depends(get_db)):
   # cursor.execute("""SELECT * FROM public.posts """)
   # posts = cursor.fetchall()
   post = db.query(models.Post).all()
   return  post

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
   #  cursor.execute("""INSERT INTO public.posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """
   #                 , (post.title, post.content, post.published))
   #  new_post = cursor.fetchone()
   #  conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # helps in retriveing or viewing the new post 
    return new_post
 
@app.get("/posts/{id}", response_model= schemas.Post)
def get_post(id: int, db: Session = Depends(get_db) ):
   # cursor.execute("""SELECT * FROM public.posts WHERE id = %s""", (str(id)))
   # post = cursor.fetchone()
   post = db.query(models.Post).filter(models.Post.id == id).first()
   if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"post with id:{id} not found")
      # response.status_code = status.HTTP_404_NOT_FOUND
      # return {'message': f"post with id : {id} not found"}
   return  post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
   #  cursor.execute("""DELETE FROM public.posts WHERE id = %s RETURNING * """, (str(id)),)
   #  del_post  = cursor.fetchone()
   #  conn.commit()
    del_post = db.query(models.Post).filter(models.Post.id == id)
    if del_post.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post with id:{id} does not exist')
    del_post.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model= schemas.Post)
def update_post(id : int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
   #  cursor.execute("""UPDATE public.posts SET title = %s, content = %s , published = %s  WHERE id = %s RETURNING * """, (post.title, post.content, post.published , (str(id)),))
   #  updated_post = cursor.fetchone()
   #  conn.commit()
    query_post = db.query(models.Post).filter(models.Post.id == id)
    post = query_post.first()
    if post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post with id:{id} does not exist')
   
    query_post.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    
    return query_post.first()