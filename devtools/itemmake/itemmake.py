import sys
import Image

def tofourbit(a):
	#print a
	if ((a > -1) and (a < 1)):
		return 3;
	if ((a > 0) and (a < 8)):
		return 2;
	if ((a > 7) and (a < 10 )):
		return 1;
	if (a > 9):
		return 0;
def conv(a):

	t = 0;
	t = t | (tofourbit(ord(a) & 0x0f) << 2)
	t = t | (tofourbit((ord(a) & 0xf0) >> 4))
	return t

def getnote(n):
	a = ["C", "D", "E", "F", "G", "A", "B", "HC", "HD", "HE", "HF", "HG"]
	q = a.index(str(n))
	return q + 0x54


def imconv(path):

	s = ""
	tmp = 0
	rol = 0
	im = Image.open(path)

	i = 0
	width = im.size[0]
	height = im.size[1]
	while ( i < (width * height) ):
		tmp = 0;
		for j in range(0, 4):
			
			tmp = tmp | tofourbit(im.getpixel(((i)%width, (i)/width)))
			
			i =  i + 1
			if j != 3:
				tmp = tmp * 4
			#print tmp

		s = s + chr(tmp)
	
	#f = open("pic.txt", 'ab')
	r = ""
	r = r + chr(width)
	r = r + chr(height)
	r = r + s
	return r


f = open(sys.argv[1], 'r')
script = f.readlines()
f.close()
f = open("template.txt", 'rb')
t = f.read()
t = bytearray(t)
f.close()
sm = 0
if( script.pop(0).strip("\n\r") != "SOUND MULTIPLIER:"):
	print "error"
script.pop(0)

sm = int(script.pop(0).strip("\n\r"))

print sm
script.pop(0)

if( script.pop(0).strip("\n\r") != "IMAGE TABLE:"):
	print "error"

script.pop(0)

i = script.pop(0).strip("\n\r")
imagetable = []

while(i != ""):
	imagetable.append(i)
	i = script.pop(0).strip("\n\r")

imdata = ""
imptr = 0x50000
imptrptr = 0x4f1

t[0x2cc] = imptr & 0xff
t[0x2cd] = (imptr & 0xff00) >> 8
t[0x2ce] = (imptr & 0xff0000) >> 16

d = imconv(imagetable[0])
timptr = imptr + len(d)

t[0x2a8] = timptr & 0xff
t[0x2a9] = (timptr & 0xff00) >> 8
t[0x2aa] = (timptr & 0xff0000) >> 16

for item in imagetable:
	d = imconv(item)
	imdata = imdata + d
	t[imptrptr] = imptr & 0xff
	t[imptrptr + 1] = (imptr & 0xff00) >> 8
	t[imptrptr + 2] = (imptr & 0xff0000) >> 16
	imptrptr = imptrptr + 3
	imptr = imptr + len(d)



for j in range(0, len(imdata)):
	t[0x50000 + 0x10 + j] = imdata[j]

ftable = []
for item in imagetable:
	index = item.find('.')
	s = item[:index]
	s = s[s.rfind('\\')+1:]
	ftable.append(s)
print ftable

cbuf = ""
on = True

while on:
	command = script.pop(0).strip("\n\r")
	if(command == "IMAGE:"):
		script.pop(0).strip("\n\r")
		im, time = script.pop(0).strip("\n\r").split(' ')
		cbuf =  cbuf + chr(ftable.index(im) + 0xb1)
		cbuf = cbuf + "\x80\x00\x00\x00" + chr(int(time, 16))
		script.pop(0).strip("\n\r")
	if(command == "NOTE:"):
		script.pop(0).strip("\n\r")
		#print script.pop(0).strip("\n\r")
		im, note, time = script.pop(0).strip("\n\r").split(' ')
		b = "\xfe\xff" + chr(getnote(note)) + "\x00\x00\x00"
		cbuf = cbuf + chr(ftable.index(im) + 0xb1)  + "\x80\x00\x00\x00\x01"
		b = b + "\xb0\x80\x00\x00\x00\x03"
		for j in range(0, sm * int(time, 16)):
			cbuf = cbuf + b
		script.pop(0).strip("\n\r")
	if(command == "END"):
		cbuf = cbuf + "\xff\xff"
		on = False
	
for j in range(0, len(cbuf)):
	t[0x250c4 + j] = cbuf[j]

f = open(sys.argv[2], 'wb')
f.write(t)
f.close()

	