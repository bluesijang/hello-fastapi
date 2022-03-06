from inspect import isroutine
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from app import oauth2
from .. import models, schemas, oauth2
from ..database import get_db


# tags => localhost:8000/docs 에서 볼수 있는 API 구분을
# Posts 로 groupping 지어줌
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# using query
#@router.get("/", response_model=List[schemas.Post])      
@router.get("/", response_model=List[schemas.PostOut])      
#@router.get("/")
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip:int = 0,search: Optional[str] = ""):        
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()    
    print(limit)
    print(search)
    
    # 1) shows all the messages whoever posted them
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
       
    # 2) shows only a messages of the owner
    # posts = db.query(models.Post).fileter(models.Post.owner_id == current_user.id).all()
    
    # 3) vote 필드 추가
    # SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content 
    # AS posts_content, posts.published AS posts_published, posts.created_at 
    # AS posts_created_at, posts.owner_id AS posts_owner_id, count(votes.post_id) 
    # AS count_1 FROM posts LEFT OUTER JOIN votes ON votes.post_id = posts.id
    # GROUP BY posts.id
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    
    
    #print(posts)
    return results


# pydantic이 data
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(post: Post):
#     # post_dict = post.dict()
#     # post_dict['id'] = randrange(0, 10000000)
#     # my_posts.append(post_dict)

#     # f"" 사용하지 않음 : sqlinjection 에 취약
#     # %s를 사용하여면 각 library (psycopg2등..)에서 점검을 해줌
#     cursor.execute("""INSERT INTO posts (title, content, published) 
#         VALUES (%s, %s, %s) RETURNING * """, 
#         (post.title, post.content, post.published))

# following line exp => userid = Depends~ 
#     : force a user to login to create a post 

def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),                 
                 current_user: int = Depends(oauth2.get_current_user)):    
    
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)       # Retrive (RUTURNING *)
    return new_post
    

# def create_posts(payLoad: dict = Body(...)):
#     return {"new_post": f"title {payLoad['title']} content{payLoad['contents']}"}

# title str, content str, ...
 
# @router.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail" : post}


# 순서대로 실행되어 아래 path 함수가 윗 함수보다 밑에 있어야 함
#@router.get("/{id}", response_model = schemas.Post)
@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    #print(post)
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'messages': f"post with id: {id} was not found"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # sql --> ORM 으로 ...
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    
    #if deleted_post == None:
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist")    
        
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):        
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s 
    #     WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    #if updated_post == None:
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()

