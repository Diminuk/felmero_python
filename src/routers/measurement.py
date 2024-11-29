from fastapi import APIRouter, Depends, HTTPException
from utils.models.models import MeasurementState,ValidInterpolation, ValidStatus, ValidMeasureMode
from typing_extensions import Annotated
from dependencies import get_status, get_db
from utils.db import crud, models, schemas
from sqlalchemy.orm import Session


router = APIRouter(prefix="/measurement",
                   tags=["measurement"])


StateDep = Annotated[MeasurementState,Depends(get_status)]

@router.get("/get/status", response_model=MeasurementState)
async def getstatus(state: StateDep):
    return state.model_dump()

@router.post("/start")
async def startmeasurement(state: StateDep):
    if not state.running:
        state.running = True
        return state.model_dump()
    raise HTTPException(401,"Measurement already running")
    
@router.post("/stop")
async def stopmeasurement(state: StateDep):
    if state.running:
        state.running = False 
        return state.model_dump()
    raise HTTPException(401,"No measurement running currently")

@router.post("/set/mode/{mode}", response_model=MeasurementState)
async def set_mode(state:StateDep, mode: ValidMeasureMode ):
    state.measuremode = mode 
    return state.model_dump()

@router.post("/set/interpolation/{interpolationmode}", response_model=MeasurementState)
async def set_interpolation(state: StateDep, interpolationmode: ValidInterpolation):
    state.interpolation = interpolationmode
    return state.model_dump()

@router.post("/create-new-section")
async def create_new_section(state:StateDep, section: schemas.SectionCreate, db: Session = Depends(get_db)):
    db_section = crud.create_section(db, section)
    if db_section.id is not None:
        state.sectionid = db_section.id
    return db_section

# Dummy 
@router.post("/create-new-dummysection")
async def create_new_dummysection(state:StateDep, section: schemas.DummySectionCreate, db: Session = Depends(get_db)):
    db_section = crud.create_dummysection(db, section)
    if db_section.id is not None:
        state.sectionid = db_section.id
    return db_section


