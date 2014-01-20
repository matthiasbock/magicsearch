#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

def identify(block):
	return '<xml'  in block or '<XML' in block

def recover(file_descriptor, ipos):
	print 'recovery module not ready'

if __name__ == '__main__':
	from sys import argv
	if len(argv) == 3:
		recover(argv[1], long(argv[2]))
	else:
		print 'Usage: '+argv[0]+' <device> <ipos>'

