from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Uuid
from sqlalchemy.orm import relationship

from .database import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    points = relationship("Point", back_populates="section")

    measurement_id = Column(Integer,ForeignKey("measurements.id"))
    measurement = relationship("Measurement",back_populates="sections")

class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True)

    h = Column(Integer)
    v = Column(Integer)
    l = Column(Integer)
    index = Column(Integer)

    section_id = Column(Integer, ForeignKey("sections.id"))
    section = relationship("Section", back_populates="points")

    calbase_id = Column(Integer,ForeignKey("calbases.id"))
    calbase = relationship("CalBase", back_populates="points")


class CalBase(Base):
    __tablename__ = "calbases"

    id = Column(Integer, primary_key=True)

    calpoints = relationship("CalPoint",back_populates="calbase")
    points = relationship("Point", back_populates="calbase")

    measurement_id = Column(Integer, ForeignKey("measurements.id"))
    measurement = relationship("Measurement", back_populates="calbases")


class CalPoint(Base):
    __tablename__ = "calpoints"

    id = Column(Integer, primary_key=True)

    h = Column(Integer)
    v = Column(Integer)
    l = Column(Integer)

    index = Column(Integer, index=True)

    calbase_id = Column(Integer,ForeignKey("calbases.id"))
    calbase = relationship("CalBase",back_populates="calpoints")


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True)

    boatname = Column(String)
    createdat = Column(DateTime)

    sections = relationship("Section", back_populates="measurement")
    calbases = relationship("CalBase", back_populates="measurement")

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="measurements")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    
    name = Column(String)
    hashedpassword = Column(String)
    role = Column(String)

    measurements = relationship("Measurement",back_populates="user")

# only for early testing 
    
class DummySection(Base):
    __tablename__ = "dummysections"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    points = relationship("DummyPoint", back_populates="section")

class DummyPoint(Base):
    __tablename__ = "dummypoints"

    id = Column(Integer, primary_key=True)

    h = Column(Integer)
    v = Column(Integer)
    l = Column(Integer)
    index = Column(Integer)

    section_id = Column(Integer, ForeignKey("dummysections.id"))
    section = relationship("DummySection", back_populates="points")