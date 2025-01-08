from fastapi import FastAPI
from fastapi.params import Body

app  = FastAPI()

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
def create_post(payload: dict = Body(...)):
    return {"new_post":f"title {payload['title']} content:{payload['content']}"}