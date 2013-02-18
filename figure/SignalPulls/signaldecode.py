f = open("clock.csv")
l = []
t = 0
t= f.readline()
print "here"
print t
while(True):
	try:
		t= f.readline()
		l.append(t.split(',')[3])
	
	except:
		break

for i in range(0, len(l)):
	#print i
	if int(l[i], 16) == 3:

		#print "read",
		a = (int(l[i+1], 16) << 16 ) | (int(l[i+2], 16) << 8 ) | int(l[i+3], 16)
		if (a == 1):
			print "BREAK"
		print "%x" % a