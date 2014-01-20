#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# http://en.wikipedia.org/wiki/Exchangeable_image_file_format

def identify(block):
	return 'Exif' in block

def recover(file_descriptor, ipos):

	device = open(file_descriptor,'rb')
	device.seek(ipos)

	outfile = open(str(ipos)+'.jpg', 'w')
	
	M = 1024**2
	for i in range(5):
		outfile.write(device.read(M))
	
	outfile.close()
	device.close()

if __name__ == '__main__':
	from sys import argv
	if len(argv) == 3:
		recover(argv[1], long(argv[2]))
	else:
		print 'Usage: '+argv[0]+' <device> <ipos>'

