#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# http://www.adobe.com/devnet/pdf/pdf_reference_archive.html

# PDFs start with %PDF-
# and end with %%EOF

def identify(block):
	return '%PDF-' in block

def identified(logentry):
	return 'PDF document' in logentry

def recover(file_descriptor, ipos):
	import os
	from shutil import move
	from math import ceil

	device = open(file_descriptor,'rb')
	device.seek(ipos)

	copied = 0
	maxcopy = 100*(1024**2)	# maximum filesize: 100 MB

	filename = str(ipos)+'.PDF'
	outfile = open(filename,'w')
	previous_block = ''
	block = device.read(512)
	if not identify(block):
		print 'Sorry, but there is no PDF on at '+str(ipos)
		return False
	print 'recovering PDF ... ',
	while (copied < maxcopy) and not ('%%EOF' in previous_block+block):
		outfile.write(block)
		copied += 512
		previous_block = block
		block = device.read(512)
	outfile.write(block)
	copied += 512
	outfile.close()
	if '%%EOF' in previous_block+block:
		print str(int(ceil(copied/float(1024**2))))+' MB, recovery successful.'
		title = ''
		data = open(filename).read()						# get PDF /Title()
		key = '/Title('
		p = data.find(key)
		if p > -1:
			q = data.find(')',p)
			title = data[p+len(key):q]

			title = title.strip().replace('.pdf','').replace('.PDF','')	# remove .pdf extension

			while '\\' in title:						# remove unicode characters
				p = title.find('\\')
				n = title[:p]
				if p+4 < len(title):
					n += title[p+4:]
				title = n

			dictionary = [chr(x) for x in range(ord('a'), ord('z')+1)]+[chr(x) for x in range(ord('A'), ord('Z')+1)]+[chr(x) for x in range(ord('0'), ord('9')+1)]
			for x in range(len(title)):					# replace non-printable characters
				if not title[x] in dictionary:
					n = title[:x]+'_'+title[x+1:]
					title = n

			if not os.path.exists(title+'.PDF'):				# rename output file
				print 'Renaming to '+title+'.PDF ...'
				move(filename, title+'.PDF')
			else:
				print 'Renaming to '+title+'-'+filename+' ...'
				move(filename, title+'-'+filename)
	else:
		print str(copied/(1024**2))+' MB. Unsuccessful: Aborting due to timeout.'
		print 'Increase "maxcopy", if you suspect the file to be larger than '+str(maxcopy/(1024**2))+' MB.'
		os.remove(filename)


if __name__ == '__main__':
	from sys import argv
	if len(argv) == 3:
		recover(argv[1], long(argv[2]))
	else:
		print 'Usage: '+argv[0]+' <device> <ipos>'

