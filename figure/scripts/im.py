import Image

f = open("C:\\Users\\Natalie\\Downloads\\dumps\\dumps\\cst-007-10-130-violetchi.bin", 'rb')

a = f.read()
s = ""
#offset = 0x201292
#offset = 0x257010
#offset = 0x2AB139
offset = 0

a = a[offset:]

num = 0
o =  0x1539

while True:
	width = ord(a[o])
	#//while (width == 0):
	#//	o = o + 1
	#//	width = ord(a[o])
	height = ord(a[o+1])
	print width,
	print height
	o = o + 2
	if( height > 0x60):
		print "end"
		print o + offset
		break
	extra = 0
	if( height > 0x60):
		print "end"
		print o + offset
		break
	if ((width) % 4 != 0):
		while ((width) % 4 != 0):
			width = width + 1
	if ((height) % 4 != 0):
		#for t in range(0, (height) % 4):
		#height  = height + 1

		print "Padded to " + str(width) + " by " + str(height)
	s = ""
	for i in range(0, height*width/4 + 1):
		for j in range(0, 4):
			#print ord(a[i])
			#print (0x03 << ((3- j)*2))
			k = ord(a[i+o]) & (0x03 << ((3- j)*2))

			l = ((k) >> ((3-j)*2))
		
			s = s + chr(0xFF&(~(l*(255/4))))
	o = o + height*width/4
	#print s

	image = Image.fromstring(
        "L", (width, height), s, "raw", 
        "L"
        )
	print "img " + str(num) + " at " + str(o)
	image.save("../ROMDump/vimages/im-" + str(num) + ".bmp")
	num = num + 1

