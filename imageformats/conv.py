f = open("../documents/gagnam.bmp")
p = f.read()
s = ""
tmp = 0
rol = 0

import Image

im = Image.open("../documents/item.bmp")

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
i = 0
width = im.size[0]
height = im.size[1]
while ( i < (width * height) ):
	tmp = 0;
	#print "start"
	#if( (i + 1)% 17) == 0:
	#	tmp = tmp | tofourbit(im.getpixel(((i)%17, (i)/17)))
	#	i = i + 1	
	#	tmp = tmp << 6

	#else:
	if(1):
		for j in range(0, 4):
			
			tmp = tmp | tofourbit(im.getpixel(((i)%width, (i)/width)))
			
			i =  i + 1
			if j != 3:
				tmp = tmp * 4
			#print tmp
			

	#print tmp
	s = s + chr(tmp)
	
f = open("pic.txt", 'wb')
f.write(s)
print len(s)

