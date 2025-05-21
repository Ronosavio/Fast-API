from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Annotated
from pydantic.types import conint
# this makes sure the format we send or recieve data is maintained without causing any datatype mismatch 
# Also making sure only the rquired fields are sent back as respone to the user
class PostBase(BaseModel):
    title : str
    content: str
    published: bool = True
     
    
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email:EmailStr
    created_at : datetime
    class Config:
        orm_mode = True
        
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
          orm_mode = True
          
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    


class UserLogin(BaseModel):
    email:str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id : Optional[str] = None

 
class Vote(BaseModel):
      post_id: int
      dir: Annotated[int, conint(ge=0, le=1)]