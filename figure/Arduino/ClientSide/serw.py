import serial
import time

#enter your device file
arddev = 'COM5'
baud = 115200

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
f = open("in.txt", 'rb')
b = f.read()
a = 0;
while True:
	print ser.readline();
	#ser.write(chr((a & 0xff0000) >> 16))
	#ser.write(chr((a & 0xff00) >> 8))
	#ser.write(chr(a & 0xff))
	#ser.write('\x00');
	#ser.write('\x00');
	#ser.write('\x00');
	for i in range(0, 256):
		print str(ord(b[a +i]))
		ser.write(str(ord(b[a +i])) + "\n")
	a = a + 256
	#for i in range(0, 4):
	#	print ser.readline()
	print "address",
	print a	