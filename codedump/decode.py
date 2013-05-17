f = open("c.csv", 'r')
o = open("c.bin", 'w')

l = f.readlines()
begin = True
state = 1
val = 0
count = 8
c = 0
for item in l:
	c = c + 1
	item = item[item.find(",")+1:]
	item = item[:item.find(",")]
	if state == 1:
		if item!= "0":
			print "error1 "  + item + " " + str(c)
		state = 2
	elif state == 2:
		if item!= "1":
			print "error2 " + item + " " + str(c)
			state = 2
		else:
			state = 3
	elif state == 3:
		if item == "0":
			val = val << 1
			state = 2
		else:
			val = (val << 1) | 1
			state = 1
		count = count - 1
		if count == 0:
			count = 8
			o.write(chr(val))
			val = 0
		