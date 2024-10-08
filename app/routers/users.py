# from app import oauth2
from typing import List
from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import hash

router = APIRouter(
    prefix='/users',
    tags=['users']
)

#### USERS' ENDPOINT #####
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
   
    # Hash the password
    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 

@router.get('/{id}', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User with id {id} not found')
    
    return user

@router.get('/', response_model=List[schemas.UserOut])
def get_user(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users