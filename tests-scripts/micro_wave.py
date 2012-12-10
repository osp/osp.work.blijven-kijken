# -*- coding: utf-8 -*-

import scribus
from PyQt4 import Qt


methodList = [method for method in dir(scribus) if callable(getattr(scribus, method))]


class MicroWave():
	"""
	Class qui va persister et prendre en charge la lecture/ecriture sur le socket
	"""
	def __init__(self):
		self.widget = Qt.QWidget()
		self.val = Qt.QDoubleSpinBox()
		self.val.setMaximum(100.0)
		self.submit = Qt.QPushButton("DO IT!")
		
		l = Qt.QVBoxLayout()
		l.addWidget(self.val)
		l.addWidget(self.submit)
		
		Qt.QObject.connect(self.submit, Qt.SIGNAL("clicked()"), self.slotDoIt)
		
		self.widget.setLayout(l)
		self.widget.show()
		
	def slotDoIt(self):
		nfs = self.val.value()
		obj = scribus.getSelectedObject(0)
		t = scribus.getText(obj)
		scribus.deselectAll()
		t0 = scribus.getText(obj)
		fs = scribus.getFontSize(obj)
		tl = scribus.getTextLength(obj)
		idx = t0.find(t) + (len(t) / 2)
		base = fs
		#print t0
		#print t
		#print "FS %i NFS %i IDX %i START %i" % (fs,nfs,idx,idx - int((nfs - fs) / 0.1))
		for i in xrange(max(idx - int((nfs - fs) * 10), 0), idx):
			scribus.selectText(i, 1, obj)
			base += 0.1
			scribus.setFontSize(base,obj)
		for i in xrange(idx, min(idx + int((nfs - fs) * 10), tl - 1)):
			scribus.selectText(i, 1, obj)
			base -= 0.1
			scribus.setFontSize(base,obj)
		scribus.setRedraw(True)
		scribus.selectObject(obj)

mc = MicroWave()

