#from re import L
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True    
    
    
class PostCreate(PostBase):
    pass


# Response model
# ORM model 인것을 pydantic model에게 알려주어 
#   pydantic model이 해당 값을 pydantic model이 사용할 수 있는 형식(dict)으로
#   변환 할 수 있도록 해줌
# title~published는 PostBase class 값을 상속받음

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime    
    class Config:
        orm_mode = True   


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        orm_mode = True   


class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True  

        
class UserCreate(BaseModel):
    email: EmailStr
    password: str

    
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# schema for access_token
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)       # 1과 같거나 작은 값만 허용 (1:like, 0:cancel like)
    