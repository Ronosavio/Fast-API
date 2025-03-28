from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, sessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = sessionLocal()
    try:
       yield db
    finally:
       db.close()
       
class Post(BaseModel):
   title: str  
   content: str
   published : bool = True 
   #rating: Optional[int] = None
while True:
   try:
      conn = psycopg2.connect(host = 'localhost', database= 'postgres', user = 'postgres', password = '1234', cursor_factory=RealDictCursor)
      cursor = conn.cursor()
      print('database connection was successful')
      break
   except Exception as error:
      print("Connecting to a database failed")
      print("Error: ", error)
      time.sleep(2)

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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
   return {"Ststus Success"}
 
@app.get("/posts")
def posts():
   cursor.execute("""SELECT * FROM public.posts """)
   posts = cursor.fetchall()
   print(posts)
   return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO public.posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """
                   , (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}
 
@app.get("/posts/{id}")
def get_post(id: int):
   cursor.execute("""SELECT * FROM public.posts WHERE id = %s""", (str(id)))
   post = cursor.fetchone()
   if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"post with id:{id} not found")
      # response.status_code = status.HTTP_404_NOT_FOUND
      # return {'message': f"post with id : {id} not found"}
   return {"Post_deatail": post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM public.posts WHERE id = %s RETURNING * """, (str(id)),)
    del_post  = cursor.fetchone()
    conn.commit()
    if del_post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post with id:{id} does not exist')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id : int, post:Post):
    cursor.execute("""UPDATE public.posts SET title = %s, content = %s , published = %s  WHERE id = %s RETURNING * """, (post.title, post.content, post.published , (str(id)),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post with id:{id} does not exist')
    
    return {"data": updated_post}