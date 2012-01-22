#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#
# like the file console utility
# but checks every block of a given file or block device
#

from subprocess import Popen, PIPE
from shlex import split
import sys
from math import ceil

ipos = 0
blocksize = 512
count = 0		# 0 for infinite reading

intro = '/dev/stdin: '

def identify(block):
	p = Popen(['file','-'], stdin=PIPE, stdout=PIPE)
	p.stdin.write(block)
	return p

def readout(p):
	return p.communicate()[0].strip()[len(intro):]

interesting = ['playlist', 'audio', 'video', 'riff', 'container', 'office', 'ascii', 'html document', 'vcard', 'graphic', 'jpeg', 'pdf document']

def check_sense(result):
	result = result.lower()
	for keyword in interesting:
		if result.find(keyword) > -1:
			return True
	return False

device = open(sys.argv[1])
if ipos > 0:
	device.seek(ipos)

cachesize = 10
cache = []
process = []

fillcache()
startprocesses()
fillcache()
readprocesses()

#num = 0
p = []
block = [True]
while not (False in block): # and ((num < count) or (count == 0)):
	for i in range(10):
	p[i] = identify(block)
	if check_sense(result):
		print str(ipos)+': '+result
	ipos += blocksize
#	num += 1
	block = device.read(blocksize)

print "stopped reading at ipos "+str(ipos)

