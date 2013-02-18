import serial
import time

#enter your device file
arddev = 'COM5'
baud = 9600

#setup - if a Serial object can't be created, a SerialException will be raised.
while True:
    try:
        ser = serial.Serial(arddev, baud)

        #break out of while loop when connection is made
        break
    except serial.SerialException:
        print 'waiting for device ' + arddev + ' to be available'
        time.sleep(3)

#read lines from serial device
f = open("dump.txt", 'wb')
while True:
   	element = ser.read()
	f.write(element)
	f.flush()