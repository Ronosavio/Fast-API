from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
   title: str
   content: str
   published : bool = True 
   rating: Optional[int] = None

#path operation
@app.get("/")
def root():
   return{"message : Welcome to my api!!"}

@app.get("/login") 
def login():
    return {"You have entered the login page"}
 
@app.get("/post")
def posts():
   return {"These are the overall post"}

@app.post("/createpost")
def create_post(new_post: Post):
    print(new_post.dict())
    return {"data":"new_post"}
 
 #title str, content str, 
 

   