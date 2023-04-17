from serial import Serial ,SerialException


def connect_to_arduino(serial_port="COM3",baudrate=9600):
    try:
        ser = Serial(serial_port, baudrate=baudrate)
        print(f"Connected to {serial_port}")
        return ser
    except SerialException:
        print(f"Arduino not yet connected, waiting...")
        return None