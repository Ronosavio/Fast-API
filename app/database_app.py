from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = 'postgressl://<username>:<password>@<ip-address/hostname>/<database_name>'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)