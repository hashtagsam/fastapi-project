from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import numpy as np
from random import random, randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel): # this is a schema. It is one of the data formats we want the user to provide input
    title: str
    content: str
    # location: str = "London"
    rating: Optional[int] = None
    published: bool

# connection to db
while True:
    try: 
        conn = psycopg2.connect(host='localhost', database='fastapi', \
                                user='postgres', password='nicole', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection successful!')
        break
    except Exception as error:
        print('Connection to database failed')
        print('Error:', error)
        # time.sleep(2)


@app.get('/')
def root():
    return {'message': 'Hello World'}

my_posts = [{'title': 'top houses in liswerry', 'content': 'I love these houses', 'location': 'Newport', 'id': 1},
            {'title': 'a great abuja', 'content': 'I love this country', 'location': 'fct', 'id': 2},
            {'title': 'top houses in gwent', 'content': 'I love these houses', 'location': 'Newport', 'id': 3},
            {'title': 'a great lekki', 'content': 'I love this country', 'location': 'Lagos', 'id': 4}]

@app.get('/posts')
def get_posts(): # get all posts
    cursor.execute(""" SELECT * FROM "Post";""")
    posts = cursor.fetchall()
    # print(posts)
    return {'data': posts}

@app.post('/createposts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # print(post) # pydantic model. shows in console

    # post_dict = post.model_dump() # pydantic model to dictionary. 
    # post_dict['id'] = randrange(0, 1000000) 
    # my_posts.append(post_dict)
    cursor.execute("""INSERT INTO "Post" (title, content, published) VALUES(%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published)
                   )
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post} # this line gets sent back to the user
    # return {'new_post': f"title {payload['title']}, content: {payload['content']}"}
# title str, content str

def find_post(id: int):
    for p in my_posts:
        if p['id'] == id:
            return p

# def find_index_of_post(id: int):
#     for k, v in enumerate(my_posts):
#         if post['id'] == id:
#             return post


# Get single post
# Note: path parameters are always returned as a string. The id here is returned as string and hence must be converted to int
@app.get('/posts/{id}') 
def get_post(id: int, response: Response): 
    # print(id)
    # post = find_post(id)

    cursor.execute("""SELECT * FROM "Post" WHERE id=%s RETURNING * """, str(id))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} not found')

    conn.commit()

    return {'post': post}

@app.delete('/posts/{id}')
def delete_post(id: int):
    # post_to_del = find_post(id)

    cursor.execute("""DELETE FROM "Post" WHERE id=%s RETURNING * """, str(id))
    deleted_post = cursor.fetchone()

    if deleted_post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'post with id: {id} does not exist')
    # else: 
    #     my_posts.remove()
    #     return {'message': f'post with id: {id} is deleted'}

    conn.commit()

    return {'message': f'Post with id {id} has been deleted'}

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    # post_to_update = find_post(id)

    cursor.execute("""UPDATE "Post" SET title = %s, content = %s, published = %s
                   WHERE id=%s RETURNING * """, 
                   ( post.title, post.content, post.published, str(id) )
                   )
    post_to_update = cursor.fetchone()

    if post_to_update == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'post with id: {id} does not exist')
    # else: 
    #     post = post.model_dump()
    #     post_to_update['title'] = post['title']
    #     post_to_update['content'] = post['content']
    #     post_to_update['location'] = post['location']

    conn.commit()

    return {'message': f'post with id: {id} is updated'}


    # return{'message': 'updated post'}