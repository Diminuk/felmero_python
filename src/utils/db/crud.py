from typing import List
from sqlalchemy.orm import Session 

from . import models, schemas

# Section
def get_section(db: Session, section_id: int ):
    return db.query(models.Section).filter(models.Section.id == section_id).first()

def get_sections(db:Session):
    return db.query(models.Section)

def create_section(db:Session, section: schemas.SectionCreate):
    db_section = models.Section(name=section.name)
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return db_section

# Point
def get_point(db:Session, point_id: int):
    return db.query(models.Point).filter(models.Point.id == point_id).first()

def get_points(db:Session, point_ids: List[int]):
    pass 

def create_point(db:Session, point: schemas.PointCreate):
    db_point = models.Point(h= point.h, v= point.v, l = point.l, section_id = point.section_id)
    print(f"db point: {db_point}")
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point

# CalBase
def get_calbase(db:Session, calbase_id: int):
    return db.query(models.CalBase).filter(models.CalBase.id == calbase_id)

def get_calbases(db:Session):
    return db.query(models.CalBase)

def create_calbase(db:Session):
    db_calbase = models.CalBase()
    db.add(db_calbase)
    db.commit()
    db.refresh(db_calbase)
    return db_calbase

# CalPoint 
def get_calpoint(db:Session, calpoint_id: int):
    return db.query(models.CalPoint).filter(models.CalPoint.id == calpoint_id).first()

def get_calpoints(db:Session):
    return db.query(models.CalPoint)

def create_calpoint(db:Session, calpoint: schemas.CalPointCreate):
    db_calpoint = models.CalPoint(**calpoint)
    db.add(db_calpoint)
    db.commit()
    db.refresh(db_calpoint)

# Measurement 
def get_measurement(db:Session, measurement_id: int):
    return db.query(models.Measurement).filter(models.Measurement.id == measurement_id).first()

def get_measurements(db:Session):
    return db.query(models.Measurement)

def create_measurement(db:Session, measurement: schemas.MeasurementCreate):
    db_measurement = models.Measurement(**measurement)
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    return db_measurement

# User
def get_user(db:Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db:Session):
    return db.query(models.User)

def create_user(db:Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, hashedpassword = user.hashedpassword, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# DummyPoint 
def get_dummypoint(db:Session, point_id: int):
    return db.query(models.DummyPoint).filter(models.DummyPoint.id == point_id).first()

def get_dummypoints(db:Session, point_ids: List[int]):
    pass 

def create_dummypoint(db:Session, point: schemas.DummyPointCreate):
    db_point = models.DummyPoint(h= point.h, v= point.v, l = point.l, section_id = point.section_id)
    print(point.section_id)
    print(f"db point: {db_point}")
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point

# DummySection
def get_dummysection(db: Session, section_id: int ):
    return db.query(models.DummySection).filter(models.DummySection.id == section_id).first()

def get_dummysections(db:Session):
    return db.query(models.DummySection)

def create_dummysection(db:Session, section: schemas.DummySectionCreate):
    db_section = models.DummySection(name=section.name)
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return db_section
