from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)
#The main file that we run where everything is connected with the help of routers
# (The APIRouter  from fastapi helps in this process which is found in the post , auth and user  python file)
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
       
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
  



 

 
