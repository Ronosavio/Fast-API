from fastapi import FastAPI

app  = FastAPI()

#path operation
@app.get("/")
def root():
   return{"message : Welcome to my api!!"}