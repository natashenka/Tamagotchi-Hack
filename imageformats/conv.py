f = open("Untitled.bmp")
p = f.read()
s = ""
tmp = 0
rol = 0

import Image

im = Image.open("Untitled.bmp")

def tofourbit(a):
	#print a
	if ((a > -1) and (a < 5)):
		return 2;
	if ((a > 4) and (a < 8)):
		return 2;
	if ((a > 7) and (a < 12 )):
		return 1;
	if (a > 11):
		return 0;

def conv(a):

	t = 0;
	t = t | (tofourbit(ord(a) & 0x0f) << 2)
	t = t | (tofourbit((ord(a) & 0xf0) >> 4))
	return t
i = 0
width = 48
while ( i < (width * 32) ):
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
			

	print tmp
	s = s + chr(tmp)
	

for i in range(0, len(s)):

	print "0x%x, " % ord(s[i]),

