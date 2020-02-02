import sys
try:
	import armasm
except:
	print "armasm is required https://github.com/stephanh42/armasm"
try:
	import Image
except:
	print "PIL is required"
from sets import Set

if len(sys.argv) < 4:
	print "makegame.py assembly image_listing outfile"


f = open("gametemp", 'rb')
gtemp = f.read()
f.close()

index = 0x3690
gtemp = gtemp[:index]
import random

def addimage(path):
	global gtemp, index
	im = Image.open(path)
	px = im.load() 
	s = Set()

	for y in range(0, im.height):
		for x in range(0, im.width):
			s.add(px[x,y])
	if len(s) > 16:
		print "image" + path + " has too many colors"
		exit()
	while len(s) != 15:
		s.add((random.randrange(0, 255), 0, 0))

	img = ""
	img = img + chr(im.width) + chr(im.height) # add width and height
	img = img + chr(len(s)&0xff) + chr(len(s)>>8)
	img = img + "\x01\xff"

	clist = []
	j = 0
	for item in s:
		clist.append(item)
		b = item[0]/8
		r = item[2]/8
		g = item[1]/4

		b1 = (r <<3) + (g >> 3)
		b2 = ((g& 7) << 5) + b
		print "index", j, hex(b1), hex(b2), item
		j = j + 1
		img = img + chr(b1) + chr(b2)

	p = ""
	for y in range(0, im.height):
		for x in range(0, im.width):
			#print px[x,y]
			v = clist.index(px[x,y])
			if v > 16:
				print v
				exit()
			p = p + chr(v)

	t = ""

	i = 0
	print "p", len(p)
	pad = False
	lasfull = 0
	if im.width %2 != 0:
		pad = True
		lastfull = im.width/2*2
		if(lastfull %2!=0):
			print "error"
			exit()
	while i < len(p)-1:
	#print hex(ord(p[i]))
	#print hex(ord(p[i+1]))
	#print(hex(ord(p[i]) + (ord(p[i+1])<<4)))
		if pad:
			if i % im.width == lastfull:
				t = t + chr(ord(p[i]) + 0)
				i = i + 1	
			else:
				t = t + chr(ord(p[i]) + (ord(p[i+1])<<4))
				i = i + 2	
		else:
			t = t + chr(ord(p[i]) + (ord(p[i+1])<<4))

			i = i + 2
	img = img + t
	old_index = len(gtemp)
	gtemp = gtemp + img
	

	if len(gtemp)%4 !=0:
		index = index + (4-index%4)
		while len(gtemp) %4 != 0:
			gtemp = gtemp + '\x00' 
	return 0x207F0000+ old_index





ftable = {"show_game_image": 0x200008FE, "set_image_mode" : 0x20003B0E, "set_mem_0": 0x2000074E, "sub_20000A36" : 0x20000A36, "wait_for_button" : 0x20000932, "set_option_1" : 0x20000454, "set_option_2": 0x20000460, "set_option_3": 0x20000448, "check_option_1": 0x20000430, "check_option_2": 0x2000043C, "check_option_3": 0x20000424}
itable = {}

f = open(sys.argv[2], 'r')
images = f.readlines()
f.close()

for item in images:
	i = item.split()
	if len(i) == 0:
		continue
	if(len(i) !=2):
		print "error splitting image"
		exit()
	name = i[0]
	loc = i[1]
	addr = addimage(loc)
       # print "image at", hex(addr)
	itable[name] = addr

f = open(sys.argv[1])
assembly = f.read()
f.close()

for item in ftable:
	#print item
	assembly = assembly.replace("(" + item + "+1)", hex(ftable[item]+1))

for item in ftable:
	#print item
	assembly = assembly.replace(item, hex(ftable[item]))

for item in itable:
	#print item
	assembly = assembly.replace(item, hex(itable[item]))

#print assembly

compiled = armasm.asm("str -> i", assembly)
code = compiled.__armasm_code__
code_index = 0x336c
cstr = ""
for i in range(0, len(code)):
	num = code[i]
	cstr = cstr + chr(num&0xff) + chr((num&0xff00)>>8) + chr((num&0xff0000)>>16) + chr((num&0xff000000)>>24)

print hex(code_index+len(cstr))
gtemp = gtemp[:code_index] + cstr + gtemp[code_index+len(cstr):]
gamelen = len(gtemp)
gls = chr((gamelen &0xff000000)>>24)+chr((gamelen &0xff0000)>>16)+chr((gamelen &0xff00)>>8)+chr(gamelen &0xff)
gtemp = gtemp[:72]+gls+gtemp[76:]


f = open(sys.argv[3], 'wb')
f.write(gtemp)
f.close()











