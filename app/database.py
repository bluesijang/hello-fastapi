# 참고 : https://fastapi.tiangolo.com/tutorial/sql-databases/

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# format
# 'postgresql://<username>:<password>@<ip addr/hostname>/<database_name> '
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# to create DB session
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


###
#  followings are for using postgres driver
###
# while True:
#     try:
#         conn = psycopg2.connect(host='oooo', database='oooo', 
#                 user='oooo', password='oooo',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as err:
#         print("Connection to database failed!")
#         print("Error: ", err)
#         time.sleep(3)