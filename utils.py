#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

def LittleEndian(string):
	if len(string) == 4:
		b = [ord(c) for c in string[::-1]]	# inverse byte order
		return long(b[0] << 24 | b[1] << 16 | b[2] << 8 | b[3])
	if len(string) == 2:
		return long(ord(string[1]) << 8 | ord(string[0]))
	else:
		return False

def hex2string(hexstring):
	hexstring = hexstring.replace(' ','')
	result = ''
	for i in range(len(hexstring)/2):
		result += chr( int(hexstring[i*2]+hexstring[i*2+1], 16) )
	return result

def format(size):
	suffices = ['PB', 'TB', 'GB', 'MB', 'KB', 'Byte']
	suffix = suffices[5]
	for i in range(len(suffices)):
		exponent = len(suffices)-1-i
		divisor = 1024**exponent
		if size >= divisor:
			size = size/divisor
			suffix = suffices[i]
			break
	return str(size)+' '+suffix

def ggT(a, b):
	if a < b:
		a, b = b, a
	while a % b != 0:
		a, b = b, a % b
	return b

def fileutil(fname):
	return Popen('file '+fname, shell=True, stdout=PIPE).communicate()[0].strip()[len('/dev/stdin: '):]

def log(msg):
	print msg
	open('magicsearch.log','a').write(msg+'\n')

