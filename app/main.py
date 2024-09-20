from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, users, auth, votes
from .config import settings

app = FastAPI()

# for the db connection (ORM)
models.Base.metadata.create_all(bind=engine)

# my_posts = [{'title': 'top houses in liswerry', 'content': 'I love these houses', 'location': 'Newport', 'id': 1},
#             {'title': 'a great abuja', 'content': 'I love this country', 'location': 'fct', 'id': 2},
#             {'title': 'top houses in gwent', 'content': 'I love these houses', 'location': 'Newport', 'id': 3},
#             {'title': 'a great lekki', 'content': 'I love this country', 'location': 'Lagos', 'id': 4}]


app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)



