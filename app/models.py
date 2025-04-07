from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from .database import Base

# the model of our table designed using python for our data base 
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, default = True)
    created_at = Column(TIMESTAMP(timezone= True),
                        nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique= True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone= True),
                        nullable=False, server_default=text('now()'))
    