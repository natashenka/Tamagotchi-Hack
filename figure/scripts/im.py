import Image

f = open("e.txt", 'rb')

a = f.read()
s = ""
#offset = 0x201292
#offset = 0x257010
#offset = 0x2AB139
offset = 0x301292

a = a[offset:]

num = 0
o = 0

while True:
	width = ord(a[o])
	height = ord(a[o+1])
	print width,
	print height
	o = o + 2
	if( height > 0x60):
		print "end"
		print o + offset
		break

	if( height > 0x60):
		print "end"
		print o + offset
		break
	if ((width) % 4 != 0):
		while ((width) % 4 != 0):
			width = width + 1

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
	print o + offset
	image.save("./imgs/im-10-" + str(num) + ".bmp")
	num = num + 1

