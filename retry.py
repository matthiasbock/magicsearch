#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#
# read magicsearch.log recovery logfile,
# created by magicsearch.py in a previous run,
# and retry recovery of certain filetypes
# without searching the harddisk for magic blocks again
#
# Usage: retry.py /dev/sdb magicsearch.log
#

import sys
from subprocess import Popen,PIPE

dev = sys.argv[1]

logfile = 'magicsearch.log'
if len(sys.argv) > 2:
	logfile = sys.argv[2]

retrylog = 'retry.log'
def log(msg):
	print msg
	open(retrylog,'a').write(msg+'\n')

import Exif, html, JFIF, m3u, PDF, RIFF, vCard, xml
path = '/home/code/magicsearch/'
recipes = {
#		'Exif.py':	Exif.identified,
#		'html.py':	html.identified,
#		'JFIF.py':	JFIF.identified,
#		'm3u.py':	m3u.identified,
		'PDF.py':	PDF.identified,
#		'RIFF.py':	RIFF.identified,
#		'vCard.py':	vCard.identified,
#		'xml.py':	xml.identified
	}

print 'Analyzing logfile '+logfile+' ...'
mlog = open(logfile)
line = mlog.readline()
while line:
	if len(line.strip()) > 0 and ':' in line:
		s = line.split(':')
		ipos = s[0]
		filetype = ':'.join(s[1:]).strip()
		if '(' in ipos:
			s = ipos.split(' ')
			ipos = s[0]
		ipos = long(ipos)
		for recipe in recipes.keys():
			if recipes[recipe](filetype):
				log('retrying '+recipe+' on '+dev+' ipos '+str(ipos)+' ...')
				Popen([path+recipe,dev,str(ipos)])
	line = mlog.readline()
mlog.close()

