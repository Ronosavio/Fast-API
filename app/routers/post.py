from .. import models, schemas, o_authent2
from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db

#handles all the Api requests for the post table in the data base

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
#, user_id: int = Depends(o_authent2.get_current_user)):
@router.get("/", response_model= List[schemas.Post])
def posts(db: Session = Depends(get_db), user_id: int = Depends(o_authent2.get_current_user)):
   # cursor.execute("""SELECT * FROM public.posts """)
   # posts = cursor.fetchall()
   post = db.query(models.Post).all()
   return  post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(o_authent2.get_current_user)):
   #  cursor.execute("""INSERT INTO public.posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """
   #                 , (post.title, post.content, post.published))
   #  new_post = cursor.fetchone()
   #  conn.commit()
    print(current_user.email)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # helps in retriveing or viewing the new post 
    return new_post
 
@router.get("/{id}", response_model= schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(o_authent2.get_current_user)):
   # cursor.execute("""SELECT * FROM public.posts WHERE id = %s""", (str(id)))
   # post = cursor.fetchone()

   post = db.query(models.Post).filter(models.Post.id == id).first()
   if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"post with id:{id} not found")
      # response.status_code = status.HTTP_404_NOT_FOUND
      # return {'message': f"post with id : {id} not found"}
   return  post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(o_authent2.get_current_user) ):
   #  cursor.execute("""DELETE FROM public.posts WHERE id = %s RETURNING * """, (str(id)),)
   #  del_post  = cursor.fetchone()
   #  conn.commit()
    del_post = db.query(models.Post).filter(models.Post.id == id)
    if del_post.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post with id:{id} does not exist')
    del_post.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model= schemas.Post)
def update_post(id : int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(o_authent2.get_current_user)):
   #  cursor.execute("""UPDATE public.posts SET title = %s, content = %s , published = %s  WHERE id = %s RETURNING * """, (post.title, post.content, post.published , (str(id)),))
   #  updated_post = cursor.fetchone()
   #  conn.commit()
    query_post = db.query(models.Post).filter(models.Post.id == id)
    post = query_post.first()
    if post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post with id:{id} does not exist')
   
    query_post.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    
    return query_post.first()