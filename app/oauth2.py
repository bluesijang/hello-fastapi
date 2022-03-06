from pyexpat import model
from tkinter import EXCEPTION
from fastapi import Depends
from jose import JWTError, jwt
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRETE_KEY
# Algorithm HS256
# Expiration time

# to get a string like this run:
# openssl rand -hex 32
# SECRETE_KEY = "ooooooooooooo"
# ALGORITHM = "oooooooooooo"
# ACCESS_TOKEN_EXPIRE_MINUTES= 60

SECRETE_KEY = settings.secrete_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES= settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    
    try:        
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])        
        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)    
        
    except JWTError:
        raise credentials_exception
    
    # token_data => like an ID
    return token_data
        

def get_current_user(token: str=Depends(oauth2_scheme), 
                     db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    
    #return verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user
