import RFIDler
import sys
import time

packet1 = [0xf0, 0, 0x0f, 1, 0, 0x2e, 0x25, 0, 2 , 0x80, 2, 0x7, 8, 0x01, 0x8, 0x1a, 0x1a, 0x1a]
	
packet2 = [0xf0, int(sys.argv[2]), 5, 1, int(sys.argv[2]), 0x2e, 0x25, 0x1] 


def send_byte(b):

	i = 0;

	result, data= rfidler.command("CLOCKH 125000")
	time.sleep(0.540/1000);
	result, data= rfidler.command("STOP")
	i = 7
	#print "send"
	while(i>=0):
		if (1):


			result, data= rfidler.command("STOP")
			time.sleep(1.650/1000);
			result, data= rfidler.command("CLOCKH 125000")
			time.sleep(0.150/1000);
		else:

			result, data= rfidler.command("STOP")
			time.sleep(0.270/1000);
			result, data= rfidler.command("CLOCKH 125000")
			time.sleep(0.150/1000);
		
		i = i - 1
	
	result, data= rfidler.command("STOP");
	time.sleep(0.210/1000);


def toBinary(n):
 #   print n
#    print ''.join(str(1 & int(n) >> i) for i in range(8)[::-1])
    return ''.join(str(1 & int(n) >> i) for i in range(8)[::-1])

port= sys.argv[1]
rfidler= RFIDler.RFIDler()
result, reason= rfidler.connect(port)

if not result:
	print 'Warning - could not open serial port:', reason

for i in range(6, 7):
	s = ""
	n = 0
	first = False
	for item in packet1:
		if (first==False):
			first = True
		else:
			n = n + item
		s = s + toBinary(item)
	s = s + toBinary(n&0xff)



	result, data= rfidler.command("PWM2 800 0 0 19 19 10 0 0 1 100 20 1 75 20");
	time.sleep(.1)
	result, data= rfidler.command("RWD2 " + s);

	print len(s)

	s = ""


	n = 0
	first = False
	packet2[1] = i
	packet2[4] = i
	for item in packet2:
		if (first==False):
			first = True
		else:
			n = n + item
		s = s + toBinary(item)
	s = s + toBinary(n&0xff)
	print len(s)

	print result
	print data
	time.sleep(0.1)
	result, data= rfidler.command("RWD2 " + s);

	print result
	print data
	
	time.sleep(2)
	print i





