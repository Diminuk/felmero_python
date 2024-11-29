import numpy as np 
import serial 
import json

V_SCALE = [
    1729, 2158, 2593, 3029, 3467, 
    3892, 4328, 4784, 5233, 5668, 
    6103, 6549, 7003, 7428, 7863, 
    8314, 8777, 9212, 9648, 10097, 
    10551, 10980, 11432, 11879, 12334, 
    12780, 13217, 13663, 14112, 14545, 
    14990, 15436, 15887, 16333, 16756, 
    17210, 17656, 18092, 18544, 18993, 
    19449, 19892, 20331, 20786, 21232,
    21668, 22113, 22559, 23012, 23448, 
    23878, 24329, 24776, 25220, 25666,
    26115, 26571
]
MM_CSALE = np.arange(200,3050,50)

LENGTH_OFFSET = 170 + 35 - 2 + 18 
def calc_length(read):
    if read < V_SCALE[0]:
        return -1
    return np.interp([read], V_SCALE, MM_CSALE) + LENGTH_OFFSET


if __name__ == "__main__":
    ser = serial.Serial("COM12")
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                line_json = json.loads(line)
                command = line_json.get("cmd")
                if command == "data":
                    # simple point
                    data = line_json.get("data")
                    h = data.get("h")
                    v = data.get("v")
                    l = data.get("l")

                    print(f"LENGTH: {calc_length(l)}")