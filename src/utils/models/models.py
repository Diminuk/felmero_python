from pydantic import BaseModel, PositiveInt
from typing import List, Union , Literal

ValidStatus = Literal["init", "measure", "basechange", "done"]
ValidInterpolation= Literal["Line", "Spline", "Arc", "Circle"]
ValidMeasureMode = Literal["Single", "Recursion"]

class MeasurementState(BaseModel):
    running: bool = False
    status: ValidStatus
    interpolation:ValidInterpolation
    measuremode: ValidMeasureMode
    boatid: str = ""
    measurementid : str = ""
    pointindex :int = 1
    recursion_buffer: List = []
    radius: float = 1
    sectionid: int = 0
    sectionname: str = ""
    userid: int = -1