#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys

ipos = 70*(1024**3)
blocksize = 512
count = 50

zeroes = chr(0)*blocksize

device = open(sys.argv[1])
if ipos > 0:
	device.seek(ipos)

last_data = 0
max_empty_bytes = 1024
message_printed = True

block = device.read(blocksize)
while block:
	if block != zeroes:
		if message_printed:
			print "since "+str(ipos)+": data, last data: "+str(last_data)
			message_printed = False
		last_data = ipos
	else:
		if not message_printed:
			print "since "+str(last_data+blocksize)+": zeroes, last data block size: "+str(ipos-last_data+blocksize)
			message_printed = True
	ipos += blocksize
	block = device.read(blocksize)

print "unable to read at ipos "+str(ipos)

