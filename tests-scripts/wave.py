#!/usr/bin/python


import sys
try:
	import scribus
except ImportError:
	print "This script only works from within Scribus"
	sys.exit(1)

obj = scribus.getSelectedObject(0)
fs = 8
sdir = 1
tl = scribus.getTextLength()
for c in range(tl - 1):
	scribus.selectText(c, 1, obj)
	if(sdir == 1):
		fs += 0.01
		if(fs > 10):
			sdir = 0
	else:
		fs -= 0.01
		if(fs < 6):
			sdir = 1
	scribus.setFontSize(fs,obj)