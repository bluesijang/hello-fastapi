from os import access
from pyexpat import model
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
# def login(user_credentails: schemas.UserLogin, db:Session = Depends(database.get_db)):
def login(user_credentails: OAuth2PasswordRequestForm = Depends(), 
          db:Session = Depends(database.get_db)):
    
    # username =
    # password = 
    
    user = db.query(models.User).filter(
        models.User.email == user_credentails.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        
    if not utils.verify(user_credentails.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # Create a token
    # return token
    # 
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return {"access_token" : access_token, "token_type" : "bearer"}


    