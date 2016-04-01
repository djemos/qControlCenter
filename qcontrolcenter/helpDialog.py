#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

APPNAME = "qControlCenter"
VERSION = "v0.1"

class helpDialog(QtGui.QDialog):
	def __init__(self, parent):
		QtGui.QDialog.__init__(self, parent)
		
		title = QtGui.QLabel(
			"<table><tr>"
			"<td><img src='icons/arch-logo.png'></td><td<&nbsp;</td>"
			"<td><BIG><b>" + APPNAME + "</b>&nbsp;" + VERSION + "</BIG></td>"
			"</tr></table>"
		)
		
		pbClose = QtGui.QPushButton("&Close")
		
		tabWidget = QtGui.QTabWidget(self)
		tabWidget.addTab(self.tabAbout(),"About")
		tabWidget.addTab(self.tabInstructions(),"Instructions")
		tabWidget.addTab(self.tabLicense(),"License")
		
		hlay = QtGui.QHBoxLayout()
		hlay.addStretch()
		hlay.addWidget(pbClose)
		
		vlay = QtGui.QVBoxLayout()
		vlay.addWidget(title)
		vlay.addWidget(tabWidget)
		vlay.addLayout(hlay)
		
		self.connect(pbClose, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))
		self.setLayout(vlay)
		self.setModal(True)
		self.setMinimumSize(512,360)

	def tabAbout(self):
		tab = QtGui.QWidget()
		label = QtGui.QLabel(
			"<P align='center'>"
			"<b>" + APPNAME + "</b>&nbsp;" + VERSION + "<br><br><i>Create your own control center quickly & easily.</i>"
			"<br><br>(c) 2008 Thierry Deseez"
			"</P>"
		)
		vlay = QtGui.QVBoxLayout()
		vlay.addWidget(label)
		
		tab.setLayout(vlay)
		
		return tab
	
	def tabInstructions(self):
		tab = QtGui.QWidget()
		textView = QtGui.QTextBrowser()
		textContent = QtCore.QString("")
		vlay = QtGui.QVBoxLayout()
		
		file = QtCore.QFile("data/INSTRUCTIONS.txt")
		if file.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
			while not file.atEnd():
				textContent.append( QtCore.QString.fromUtf8( file.readLine().data() ) )

		textView.setText(textContent)
		textContent = None
		vlay.addWidget(textView)
		tab.setLayout(vlay)
		
		return tab
	
	def tabLicense(self):
		tab = QtGui.QWidget()
		textView = QtGui.QTextBrowser()
		textContent = QtCore.QString("")
		vlay = QtGui.QVBoxLayout()
		
		file = QtCore.QFile("data/LICENSE.html")
		if file.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
			while not file.atEnd():
				textContent.append( QtCore.QString.fromUtf8( file.readLine().data() ) )

		textView.setHtml(textContent)
		textContent = None
		
		vlay.addWidget(textView)
		tab.setLayout(vlay)
		
		return tab