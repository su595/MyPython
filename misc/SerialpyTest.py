from time import sleep
import serial

ser = serial.Serial(port='COM6', baudrate=9600, timeout=.1) # Establish the connection on a specific port

while True:
    data = ser.read()
    print(data)

