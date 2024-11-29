from fastapi import APIRouter, Depends, HTTPException
from typing import List 
from utils.db import schemas, crud
from dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/data",
                   tags=["data"])

@router.get("/get-sections", response_model = List[schemas.Section])
async def get_sections(db: Session = Depends(get_db)):
    db_sessions = crud.get_sections(db)
    if db_sessions is None:
        raise HTTPException(status_code=404, detail="No sections found")
    return db_sessions

@router.get("/get-section/{section_id}", response_model = schemas.Section)
async def read_section(section_id: str, db: Session = Depends(get_db)):
    db_section = crud.get_section(db, section_id=section_id)
    if db_section is None:
        raise HTTPException(status_code=404, deatil="Section not found")
    return db_section

@router.get("/get-measurements", response_model=List[schemas.MeasurementPublic])
async def read_measurements(db:Session = Depends(get_db)):
    db_measurements = crud.get_measurements(db)
    if db_measurements is None:
        raise HTTPException(status_code=404, detail="No measurements found")
    return db_measurements

@router.get("/get-measurement/{measurement_id}", response_model=schemas.MeasurementPublic)
async def read_measurement(measurement_id: int, db:Session = Depends(get_db)):
    db_measurement = crud.get_measurement(db, measurement_id)
    if db_measurement is None:
        raise HTTPException(status_code=404, detail="Measurement not found by id")
    return db_measurement

@router.get("/get-calbases", response_model=schemas.CalBasePublic)
async def read_calbases(db:Session = Depends(get_db)):
    db_calbases = crud.get_calbases(db)
    if db_calbases is None:
        raise HTTPException(status_code=404, detail="No calbases found")
    return db_calbases

# Dummy
@router.get("/get-dummysections", response_model = List[schemas.DummySection])
async def get_dummysections(db: Session = Depends(get_db)):
    db_sessions = crud.get_dummysections(db)
    if db_sessions is None:
        raise HTTPException(status_code=404, detail="No dummy sections found")
    return db_sessions