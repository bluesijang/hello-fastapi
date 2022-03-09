# 강의 : https://www.youtube.com/watch?v=0sOvCWFmrtA&list=PPSV
#       Python API Development - Comprehensive Course for Beginners

# Uvicorn is an ASGI web server implementation for Python.
# https://www.uvicorn.org/
# https://fastapi.tiangolo.com/tutorial/first-steps/

# PostgreSQL DB driver 
# https://www.psycopg.org/
### server API 실행 방법
### eg) uvicon main:app -reload``


from fastapi import FastAPI
from passlib.context import CryptContext
from . import models
from .database import engine
from .routers import post, vote, user, auth
from .config import settings
from fastapi.middleware.cors import CORSMiddleware




# hashing algorithm : bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# DB가 없으면 model 파일을 보고 schema를 만듬
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = ["*"]       # every domain
origins = ["https://www.google.com", "https://www.youtube.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(post.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(vote.router)

# For CORS test from local computer chrome browser
# without origins options, 
# connectting from outside such as youtube, google etc..
# to local is not accepted ()
@app.get("/")
def root():
    return {"messages": "Hello World !!!~~~~"}

# Using ORM
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
    
#     posts = db.query(models.Post).all()
#     print(posts)
#     return {"data" : posts }

