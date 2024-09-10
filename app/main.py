from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import numpy as np
from random import random, randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from .utils import hash
from .routers import post, users, auth

app = FastAPI()

# for the db connection (ORM)
models.Base.metadata.create_all(bind=engine)


# connection to db (postgres direct)
# while True:
#     try: 
#         conn = psycopg2.connect(host='localhost', database='fastapi', \
#                                 user='postgres', password='nicole', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection successful!')
#         break
#     except Exception as error:
#         print('Connection to database failed')
#         print('Error:', error)
        # time.sleep(2)


@app.get('/')
def root():
    return {'message': 'Hello World'}

# my_posts = [{'title': 'top houses in liswerry', 'content': 'I love these houses', 'location': 'Newport', 'id': 1},
#             {'title': 'a great abuja', 'content': 'I love this country', 'location': 'fct', 'id': 2},
#             {'title': 'top houses in gwent', 'content': 'I love these houses', 'location': 'Newport', 'id': 3},
#             {'title': 'a great lekki', 'content': 'I love this country', 'location': 'Lagos', 'id': 4}]

# Testing sqlalchemy connection
# @app.get('/sqlalchemy')
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.PostTable).all()
#     # print(posts)
#     return {'data': posts}

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)



