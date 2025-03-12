from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Post(BaseModel):
   title: str
   content: str
   published : bool = True 
   rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favourite food", "content": "I like pizza", "id": 2}]

def find_post(id):
   for p in my_posts:
      if p['id'] == id:
         return  p
      
#path operation
@app.get("/")
def root():
   return{"message : Welcome to my api!!"}

@app.get("/login") 
def login():
    return {"You have entered the login page"}
 
@app.get("/posts")
def posts():
   return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}
 
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
   post = find_post(id)
   if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"post with id:{id} not found")
      # response.status_code = status.HTTP_404_NOT_FOUND
      # return {'message': f"post with id : {id} not found"}
   return {"Post_deatail": post}
