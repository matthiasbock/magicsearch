#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

MTS1 = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x00)+chr(0x47)
MTS2 = chr(0x00)+chr(0x00)+chr(0x08)+chr(0xE2)+chr(0x47)

def identify(block):
	return block[:5] == MTS1 or block[:5] == MTS2

def recover(file, ipos):
	device = open(file,'rb')
	device.seek(ipos)
	
	filesize = 1024**3
	print 'recovering '+str(filesize/(1024**2))+' MB AVCHD ...',

	filename = str(ipos).zfill(12)+'.mts'
	copied = 0
	outfile = open(filename,'w')
	outfile.truncate(filesize)
	outfile.close()
	outfile = open(filename,'w')
	while copied < filesize:
		outfile.write( device.read(512) )
		copied += 512
	outfile.close()
	device.close()
	print 'done.'

if __name__ == '__main__':
	from sys import argv
	if len(argv) == 3:
		recover(argv[1], long(argv[2]))
	else:
		print 'Usage: '+argv[0]+' <device> <ipos>'

