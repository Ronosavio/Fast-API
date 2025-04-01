from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

                           #'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQL_ALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost/postgres'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 

def get_db():
    db = sessionLocal()
    try:
       yield db
    finally:
       db.close()