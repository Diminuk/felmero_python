from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, List, Union
from utils.db import models
from utils.db.database import  engine
from routers import measurement, data, users, auth
from contextlib import asynccontextmanager
from utils.ser.serialcom import SerialCom

PORT = 8000
SERIALPORT = "COM12"
BAUDRATE = 9600

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    #mySerial = SerialCom(SERIALPORT, BAUDRATE)
    #mySerial.start_serial_listener()
    print("Serial listener started")
    yield 
    print("Serial listener stopped")


app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(measurement.router)
app.include_router(data.router)
app.include_router(users.router)
app.include_router(auth.router)



if __name__ == "__main__":
    import uvicorn 
    print(f"Starting communication server on port: {PORT}")
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)