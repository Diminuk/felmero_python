from typing import Union, List
from pydantic import BaseModel
import datetime

# Point
class PointBase(BaseModel):
    h: int
    v: int 
    l: int 

    section_id: int 
    calbase_id: int

class PointCreate(PointBase):
    pass 

class Point(PointBase):
    id: int

    class Config:
        orm_mode = True


# Section
class SectionBase(BaseModel):
    name: str

class SectionCreate(SectionBase):
    measurement_id: int 

class Section(SectionBase):
    id: int 
    points: List[Point] = []
    measurement_id: int 
    class Config:
        orm_mode = True


# CalPoint
class CalPointBase(BaseModel):
    h: int 
    v: int 
    l: int 
    index: int

class CalPointCreate(CalPointBase):
    calbase_id: int 

class CalPointPublic(CalPointBase):
    id: int 
    calbase_id: int
    class Config:
        orm_mode = True


# CalBase 
class CalBaseBase(BaseModel):
    measurement_id: int 

class CalBaseCreate(CalBaseBase):
    pass

class CalBasePublic(CalBaseBase):
    id: int 
    calpoints: List[CalPointPublic] = []
    points: List[Point] = []
    class Config:
        orm_mode = True
    

# Measurement 
class MeasurementBase(BaseModel):
    boatname: str 
    createdat: datetime.datetime

class MeasurementCreate(MeasurementBase):
    user_id: int 

class MeasurementPublic(MeasurementBase):
    id: int 
    sections: List[Section] = []
    calbases: List[CalBasePublic] = []
    class Config:
        orm_mode = True


# User 
class UserBase(BaseModel):
    name: str
    role: str 
    hashedpassword: str 

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: int 
    measurements: List[MeasurementPublic] = []
    class Config:
        orm_mode = True


# DummyPoint
class DummyPointBase(BaseModel):
    h: int
    v: int 
    l: int 

    section_id: int 

class DummyPointCreate(DummyPointBase):
    pass 

class DummyPoint(DummyPointBase):
    id: int

    class Config:
        orm_mode = True


# DummySection
class DummySectionBase(BaseModel):
    name: str

class DummySectionCreate(DummySectionBase):
    pass

class DummySection(DummySectionBase):
    id: int 
    points: List[DummyPoint] = []
    class Config:
        orm_mode = True