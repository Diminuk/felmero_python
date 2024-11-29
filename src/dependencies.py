from utils.models.models import MeasurementState
from utils.db.database import SessionLocal, engine

class MeasurementStatus:
    def __init__(self,):
        self.state: MeasurementState = MeasurementState(
            status="init",
            interpolation="Line",
            measuremode="Single"
        )

status = MeasurementStatus()

def get_status():
    return status.state

async def get_db():
    db = SessionLocal()
    try: 
        yield db 
    finally:
        db.close()
