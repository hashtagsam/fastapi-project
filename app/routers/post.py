from .. import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix='/posts',
    tags=['posts']
)

@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)): # get all posts
    # cursor.execute(""" SELECT * FROM "Post";""")
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.PostTable).all()

    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # print(post) # pydantic model. shows in console

    # post_dict = post.model_dump() # pydantic model to dictionary. 
    # post_dict['id'] = randrange(0, 1000000) 
    # my_posts.append(post_dict)
    # cursor.execute("""INSERT INTO "Post" (title, content, published) VALUES(%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published)
    #                )
    # new_post = cursor.fetchone()
    # conn.commit()

    # print(post.model_dump())
    new_post = models.PostTable(**post.model_dump()) # this unpacks the dictionary so that you don't have to type post.title, post.content, ...
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # this is the equivalent of RETURNING in sql

    return new_post # this line gets sent back to the user
    # return {'new_post': f"title {payload['title']}, content: {payload['content']}"}
# title str, content str

# def find_post(id: int):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_index_of_post(id: int):
#     for k, v in enumerate(my_posts):
#         if post['id'] == id:
#             return post


# Get single post
# Note: path parameters are always returned as a string. The id here is returned as string and hence must be converted to int
@router.get('/{id}', response_model=schemas.Post) 
def get_post(id: int, response: Response, db: Session = Depends(get_db)): 
    # print(id)
    # post = find_post(id)

    # cursor.execute("""SELECT * FROM "Post" WHERE id=%s RETURNING * """, str(id))
    # post = cursor.fetchone()

    post = db.query(models.PostTable).filter(models.PostTable.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} not found')

    # conn.commit()

    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # post_to_del = find_post(id)

    # cursor.execute("""DELETE FROM "Post" WHERE id=%s RETURNING * """, str(id))
    # deleted_post = cursor.fetchone()

    post = db.query(models.PostTable).filter(models.PostTable.id == id)#.first()

    if post.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'post with id: {id} does not exist')
    # else: 
    #     my_posts.remove()
    #     return {'message': f'post with id: {id} is deleted'}

    post.delete(synchronize_session=False)
    db.commit()

    return {'message': f'Post with id {id} has been deleted'}

@router.put('/{id}')
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # post_to_update = find_post(id)

    # cursor.execute("""UPDATE "Post" SET title = %s, content = %s, published = %s
    #                WHERE id=%s RETURNING * """, 
    #                ( post.title, post.content, post.published, str(id) )
    #                )
    # post_to_update = cursor.fetchone()

    post_query = db.query(models.PostTable).filter(models.PostTable.id == id)


    if post_query.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'post with id: {id} does not exist')
    # else: 
    #     post = post.model_dump()
    #     post_to_update['title'] = post['title']
    #     post_to_update['content'] = post['content']
    #     post_to_update['location'] = post['location']

    post_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()

    return {'message': f'post with id: {id} is updated'}
