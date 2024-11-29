import serial 
import json
import time
import numpy as np

ser = serial.Serial("COM12", 9600, timeout=1)

HORIZONTAL_MAX = 228000
#HORIZONTAL_MAX = 205000
VERTICAL_MAX = 228000
#VERTICAL_MAX = 205000
LENGTH_MAX = 32767
LENGTH_MAX_VALUE_MM = 1830 # without offset

LENGTH_V_OFFSET = 8543

LENGTH_OFFSET = 155
LENGTH_OFFSET = 155+35+4

HEIGHT_OFFSET = 0

def convert_to_xyz(h, v, l):
    # Normalize h and v to radians between 0 and 2π using numpy
    h_angle = (h % HORIZONTAL_MAX) * (2 * np.pi / HORIZONTAL_MAX)
    v_angle = (v % VERTICAL_MAX) * (2 * np.pi / VERTICAL_MAX)
    
    # Compute the radial distance r
    r = (l - LENGTH_V_OFFSET)*(LENGTH_MAX_VALUE_MM/ (LENGTH_MAX-LENGTH_V_OFFSET)) 
    h_angle = np.rad2deg(h_angle)
    v_angle = np.rad2deg(v_angle)
    

    return h_angle, v_angle, r


ll = np.arange(0,1850,50) + 155+35 - 4
fll = np.array([
    8527,9137,9759,10429,11082,11751,12406,13088,13763,14456,15095,
    15785,16422,17132,17802,18443,19126,19784,20479,21122,
    21787,22484,23110,23789,24455,25109,25771,26493,27117,27792,
    28446,29146,29813,30477,31137,31804,32472
])

res = np.polyfit(fll,ll,1)
p = np.poly1d(res)



def listen_serial():
    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    print("Received from serial:", line)
                    # Store or process the incoming serial data
                    line_json = json.loads(line)
                    command = line_json.get("cmd")
                    if command == "data":
                        # simple point
                        data = line_json.get("data")
                        print(data)
                        h = data.get("h")
                        v = data.get("v")
                        l = data.get("l")
                        h_angle, v_angle, length = convert_to_xyz(h,v,l)
                        interp_length = p(l) + 4
                        print(f"H: {h_angle} | V: {v_angle}  | LL: {interp_length}")

                    elif command == "new":
                        #change interpolation
                        pass 
                    elif command == "incfirst":
                        #change measuremode
                        pass

                        
        except Exception as e:
            print("Error reading from serial:", e)

if __name__ == "__main__":
    listen_serial()