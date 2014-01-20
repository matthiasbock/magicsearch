#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#
# recipe to recover
# Microsoft Office Open XML Format
# docx, pptx and xlsx
#
# http://www.garykessler.net/library/file_sigs.html
# ftp://ftp.astron.com/pub/file/
#   magic/Magdir/msooxml

"""
#------------------------------------------------------------------------------
# $File: msooxml,v 1.1 2011/01/25 18:36:19 christos Exp $
# msooxml:  file(1) magic for Microsoft Office XML
# From: Ralf Brown <ralf.brown@gmail.com>

# .docx, .pptx, and .xlsx are XML plus other files inside a ZIP
#   archive.  The first member file is normally "[Content_Types].xml".
# Since MSOOXML doesn't have anything like the uncompressed "mimetype"
#   file of ePub or OpenDocument, we'll have to scan for a filename
#   which can distinguish between the three types

# start by checking for ZIP local file header signature
0               string          PK\003\004
# make sure the first file is correct
>0x1E           string          [Content_Types].xml
# skip to the second local file header
#   since some documents include a 520-byte extra field following the file
#   header,  we need to scan for the next header
>>(18.l+49)     search/2000     PK\003\004
# now skip to the *third* local file header; again, we need to scan due to a
#   520-byte extra field following the file header
>>>&26          search/1000     PK\003\004
# and check the subdirectory name to determine which type of OOXML
#   file we have
>>>>&26         string          word/           Microsoft Word 2007+
!:mime application/msword
>>>>&26         string          ppt/            Microsoft PowerPoint 2007+
!:mime application/vnd.ms-powerpoint
>>>>&26         string          xl/             Microsoft Excel 2007+
!:mime application/vnd.ms-excel
>>>>&26         default         x               Microsoft OOXML
!:strength +10
"""

from utils import hex2string

def identify(block):
	key1 = hex2string('50 4B 03 04 14 00 06 00')
	key2 = '[Content_Types].xml'
	return block[:8] == key1 and block[0x1E:(0x1E+len(key2))] == key2

def recover(dev, ipos):
	device = open(dev, 'rb')
	device.seek(ipos)

	copied = 0
	maxcopy = 500*(1024**2)	# maximum filesize: 100 MB

	filename = str(ipos)+'.ZIP'
	outfile = open(filename, 'w')
	previous_block = ''
	block = device.read(512)
	print 'recovering ZIP ... ',
	key = hex2string('50 4B 05 06') # end of central dir signature
	while (copied < maxcopy) and not (key in previous_block+block):
		outfile.write(block)
		copied += 512
		previous_block = block
		block = device.read(512)
	outfile.write(block)
	copied += 512
	outfile.close()
	print 'ZIP recovery finished.'

if __name__ == '__main__':
	from sys import argv
	if len(argv) == 3:
		recover(argv[1], long(argv[2]))
	else:
		print 'Usage: '+argv[0]+' <device> <ipos>'

