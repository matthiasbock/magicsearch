#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#
# like the file console utility
# but checks every block of a given file or block device
#

import sys

ipos = 54640401408
blocksize = 512
count = 0		# 0 for infinite reading

intro = '/dev/stdin: '
logfile = '/media/magicsearch.log'

interesting = ['Exif', 'JFIF', 'EXTM3U', 'RIFF', '<html', '<HTML', 'BEGIN:VCARD', '%PDF-']

def search_magic(result):
	for keyword in interesting:
		if result.find(keyword) > -1:
			return keyword
	return None

def exitfunction():
	l = "stopped reading at ipos "+str(ipos)
	print l
	open(logfile,'a').write(l+'\n')

sys.exitfunc = exitfunction

device = open(sys.argv[1])
if ipos > 0:
	device.seek(ipos)

#num = 0
block = device.read(blocksize)
while block: # and ((num < count) or (count == 0)):
	hit = search_magic(block)
	if hit is not None:
		hit = str(ipos)+': '+hit
		print hit
		open(logfile,'a').write(hit+'\n')
	ipos += blocksize
#	num += 1
	block = device.read(blocksize)

