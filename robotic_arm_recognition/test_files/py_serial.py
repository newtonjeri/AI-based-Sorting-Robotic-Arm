#!/usr/bin/env python3

import serial
import time

def main():
    data = "a180,b90,c90,d90,e0,\n"
    data_1 = "a0,b90,c90,d90,e0,\n"
    data_2 = "a180,b90,c90,d90,e0,\n"
    data_3 = "a0,b90,c90,d90,e0,\n"
    data_4 = "a90,b90,c90,d90,e0,\n"
    port = "/dev/ttyUSB0"
    ser = serial.Serial(port, 9600, timeout=1)
    time.sleep(2)

    try:
        ser.flush()
        ser.write(data.encode('utf-8'))
        ser.write(data_1.encode('utf-8'))
        ser.write(data_2.encode('utf-8'))
        ser.write(data_3.encode('utf-8'))
        ser.write(data_4.encode('utf-8'))

        print("Data sent to Arduino")

    except serial.SerialException as e:
        print(f"Error: Could not send data to Arduino due to {e}")


    finally:
        ser.close()


if __name__ == "__main__":
    main()
