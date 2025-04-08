from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth
from .config import Settings

models.Base.metadata.create_all(bind=engine)
#The main file that we run where everything is connected with the help of routers
# (The APIRouter  from fastapi helps in this process which is found in the post , auth and user  python file)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
  



 

 
