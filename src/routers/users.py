from fastapi import APIRouter, Depends, HTTPException
from typing import List 
from utils.db import schemas, crud
from dependencies import get_db
from sqlalchemy.orm import Session 

router = APIRouter(prefix="/users",
                   tags=["users"])


@router.get("/get-user/{user_id}", response_model=schemas.UserPublic)
async def read_user(user_id: int, db:Session = Depends(get_db)):
    db_user = crud.get_user(db,user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/get-users", response_model=List[schemas.UserPublic])
async def read_users(db:Session = Depends(get_db)):
    db_users = crud.get_users(db)
    if db_users is None:
        raise HTTPException(status_code=404, detail="No user found in database")
    return db_users

@router.post("/create-user", response_model=schemas.UserPublic)
async def create_user(newuser: schemas.UserCreate,db:Session = Depends(get_db)):
    db_user = crud.create_user(db,newuser)
    return db_user