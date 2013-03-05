a = open("bytecoden.txt")

f = a.read()
f = f[f.find("001:"):]
t = f.split()

ops = []
o6502 = []
osun = []
b = []
index = 0
for item in t:
	if (len(item) ==3) and (item[2] == 'H') and (index != 2):
		o6502.append(int(item[:2], 16))
		index = 2
	elif (index == 1):
		ops.append(item)
		index = 57	
	elif (index == 2):
		osun.append(int(item[:2], 16))
		#print "added sun"
		index = 3
	elif (index == 3):
		b.append(int(item))
		index = 4
		#print "added b"
	elif (item.find(':') != -1):
		index = 1

#print len(osun)
#print len(b)

c = open("testbinary.bin", 'rb')

code = c.read()
osun.pop(ops.index("BRK"))
b.pop(ops.index("BRK"))
o6502.pop(ops.index("BRK"))
ops.pop(ops.index("BRK"))
#osun = o6502 #comment out for standard
i = 0
while(i < len(code)):
	if (osun.count(ord(code[i])) != 0):
		run = 1
		#print "inner " + str(i)
		ind = b[osun.index(ord(code[i]))]
		while osun.count(ord(code[i+ ind])) != 0:
			run = run + 1
			ind = ind + b[osun.index(ord(code[i + ind]))]
		if( run > 25):
			print "assembly found, size " + str(run) + " index " + str(i)
			y = 0
			for x in range(0, run):
				print ops[osun.index(ord(code[i + y]))],
				print "(" + str(osun[osun.index(ord(code[i + y]))]) + ")",
				#print b[osun.index(ord(code[i + y]))]
				for z in range(1, b[osun.index(ord(code[i + y]))]):
					print str(ord(code[i + y + z])),
				y = y + b[osun.index(ord(code[i + y]))]
				print " "
			i = i + run
	i = i + 1			

print b	
print o6502
print osun	
