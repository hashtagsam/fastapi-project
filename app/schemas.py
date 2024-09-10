from pydantic import BaseModel, EmailStr
from datetime import datetime

# class Post(BaseModel): # this is a schema. It is one of the data formats we want the user to provide input
#     title: str
#     content: str
#     # location: str = "London"
#     # rating: Optional[int] = None
#     published: bool

class PostBase(BaseModel):
    title: str
    content: str
    published: bool

class PostCreate(PostBase):
    pass

class Post(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True


### USERS' Schema ###
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str