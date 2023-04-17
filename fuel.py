from SimConnect import *

import time
from arduino import connect_to_arduino
import sys
from serial import Serial

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


    if not ser or not ser.is_open:
        ser = connect_to_arduino(serial_port)
        
        if not ser:
            return

    try:
        if(not sm or not aq):
            sm = SimConnect()
            aq = AircraftRequests(sm, _time=2000)

        time.sleep(1)

        fuel_capacity = aq.find("FUEL_TOTAL_CAPACITY").value
        curr_fuel = aq.find("FUEL_TOTAL_QUANTITY").value
        
        if not curr_fuel or not fuel_capacity:
            print("failed reading values")
            return 
        
        curr_fuel_angle = int((curr_fuel * 340) / fuel_capacity)

        ser.write(str(curr_fuel_angle).encode())

        print("Sent value:", curr_fuel_angle)

        if ser.in_waiting > 0:
            arduino_output = ser.readline().decode().strip()
            print("Received from Arduino:", arduino_output)
    except Exception as e:
        
        print("waiting for p3d to open",e)
        
        if(sm):
            sm.exit()
            sm = None

        return 
    
if __name__ == "__main__":
    main()
