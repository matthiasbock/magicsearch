#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# http://en.wikipedia.org/wiki/JPEG_File_Interchange_Format

# Citing http://msdn.microsoft.com/en-us/library/ms779636(VS.85).aspx :

# The RIFF header has the following form:
#
# 'RIFF' fileSize fileType (data)
#
# where 'RIFF' is the literal FOURCC code 'RIFF', fileSize is a 4-byte value giving
# the size of the data in the file, and fileType is a FOURCC that identifies the
# specific file type. The value of fileSize includes the size of the fileType
# FOURCC plus the size of the data that follows, but does not include the size
# of the 'RIFF' FOURCC or the size of fileSize. The file data consists of chunks and lists, in any order.

def identify(block):
	return 'JFIF' in block

def recover(file_descriptor, ipos):
	from utils import LittleEndian

	device = open(file_descriptor,'rb')
	device.seek(ipos)
	magic = device.read(2)
	filesize = LittleEndian(device.read(2))
	format = device.read(4).strip()

	if magic != chr(0xFF)+chr(0xE0):
		print 'Warning: APP0 marker not found at '+str(ipos)

	def JFIF():
		print 'recovering '+str(filesize/(1024**2))+' MB JFIF ...',
		device.seek(ipos)
		copied = 0
		filename = str(ipos)+'.JPG'
		outfile = open(filename,'w')
		outfile.truncate(filesize)
		outfile.close()
		outfile = open(filename,'w')
		while copied < filesize:
			outfile.write( device.read(512) )
			copied += 512
		print 'done.'

	def JFXX():
		print 'JFXX recovery not supported yet'

	if format == 'JFIF':
		JFIF()
	elif format == 'JFXX':
		JFXX()
	else:
		print 'Unrecognized format: '+format

if __name__ == '__main__':
	from sys import argv
	if len(argv) == 3:
		recover(argv[1], long(argv[2]))
	else:
		print 'Usage: '+argv[0]+' <device> <ipos>'

