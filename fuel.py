from SimConnect import *
import time
from arduino import connect_to_arduino
import sys
from serial import Serial
import re
import struct

KEYS_H = "./keys.h"

#loads the keys from the keys.h header file
pattern = re.compile(r'#define\s+(\w+)\s+(\d+)')

with open(KEYS_H, 'r') as f:
    contents = f.read()

pairs = pattern.findall(contents)

plane_values = {key: int(value) for key, value in pairs}



ser:Serial = None
sm:SimConnect = None
aq:AircraftRequests = None

def main():
    if len(sys.argv) < 2:
        serial_port = "COM3"
    else:
        serial_port = sys.argv[1]
         
    while True:
        loop(serial_port)
        time.sleep(1)

def loop(serial_port):
    global ser
    global sm
    global aq
    values_to_reads = ["FUEL_LEFT_CAPACITY","FUEL_RIGHT_CAPACITY","FUEL_LEFT_QUANTITY","FUEL_RIGHT_QUANTITY"]

    if not ser or not ser.is_open:
        ser = connect_to_arduino(serial_port)
        if not ser:
            return

    try:
        if(not sm or not aq):
            sm = SimConnect()
            aq = AircraftRequests(sm, _time=2000)

        time.sleep(3)
        
        values_read = {}
        print("Wrote")
        for value_key in values_to_reads:
            values_read[value_key] =int(aq.find(value_key).value)

            if not values_read[value_key]:
                print("failed reading value ",value_key)
                return
            print(str(plane_values[value_key]) + ',' + str(values_read[value_key]))
            
            ser.write(bytes(str(plane_values[value_key]) + ',' + str(values_read[value_key]) + '\n', 'utf-8'))
            

        while ser.in_waiting > 0:
            arduino_output = ser.readline().decode().strip()
            print("Received from Arduino: ", arduino_output)


    except Exception as e:
        
        print("waiting for p3d to open",e)
        
        if(sm):
            sm.exit()
            sm = None

        return 
    
if __name__ == "__main__":
    main()
