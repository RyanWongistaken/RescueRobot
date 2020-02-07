import serial
import re

ser = serial.Serial('/dev/ttyUSB0', 115200, 8, 'N', 1, timeout = 5)

def GetData():
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    data = str(ser.readline())
    data = data[:-6]
    data = data.strip("b'")
    heading, tilt, temp, oxy = data.split(" ")
    heading = int(heading)
    tilt = int(tilt)
    temp = int(temp)
    oxy = int(oxy)
    senso = [heading, tilt, temp, oxy]
    return senso
GetData()