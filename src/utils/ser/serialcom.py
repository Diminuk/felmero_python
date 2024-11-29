import serial 
import threading
import json
from utils.db.database import SessionLocal
from utils.db import crud, schemas
from dependencies import get_status

class SerialCom:
    def __init__(self, PORT: str, BAUDRATE: int):
        self.ser = serial.Serial(PORT,BAUDRATE, timeout=1 )

    def listen_serial(self):
        while True:
            try:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line:
                        print("Received from serial:", line)
                        line_json = json.loads(line)
                        command = line_json.get("cmd")
                        if command == "data":
                            # simple point
                            measurement_status = get_status()
                            data = line_json.get("data")
                            print(data)
                            h = data.get("h")
                            v = data.get("v")
                            l = data.get("l")
                            with SessionLocal() as db_session:
                                #point = schemas.PointCreate(h=h, v=v, l=l, section_id=measurement_status.sectionid)
                                point = schemas.DummyPointCreate(h=h, v=v, l=l, section_id=measurement_status.sectionid)
                                #crud.create_point(db_session, point)
                                crud.create_dummypoint(db_session, point)

                        elif command == "new":
                            #change interpolation
                            pass 
                        elif command == "incfirst":
                            #change measuremode
                            pass

   
            except Exception as e:
                print("Error reading from serial:", e)

    def start_serial_listener(self):
        thread = threading.Thread(target=self.listen_serial)
        thread.daemon = True
        thread.start()