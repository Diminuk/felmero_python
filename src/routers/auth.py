from fastapi import APIRouter, Depends, HTTPException
from typing import List 
from utils.db import schemas, crud
from dependencies import get_db, get_status
from sqlalchemy.orm import Session 
from typing_extensions import Annotated
from utils.models.models import MeasurementState

router = APIRouter(prefix="/auth",
                   tags=["auth"])

StateDep = Annotated[MeasurementState,Depends(get_status)]

@router.post("/login/{user_id}")
async def login(user_id: int,db:Session = Depends(get_db), state: MeasurementState = Depends(get_status)):
    db_user = crud.get_user(db,user_id)
    if db_user is None:
        raise HTTPException(403, detail="Incorrect user id")
    state.userid = db_user.id
    return {"Status": "Success"}