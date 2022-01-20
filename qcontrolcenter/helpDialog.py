#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *

try:
    QString = unicode
except NameError:
    # Python 3
    QString = str

APPNAME = "qControlCenter"
VERSION = "v0.3"

class helpDialog(QtWidgets.QDialog):
	def __init__(self, parent):
		QtWidgets.QDialog.__init__(self, parent)

		title = QtWidgets.QLabel(
			"<table><tr>"
			"<td><BIG><b>" + APPNAME + "</b>&nbsp;" + VERSION + "</BIG></td>"
			"</tr></table>"
		)

		pbClose = QtWidgets.QPushButton("&Close")

		tabWidget = QtWidgets.QTabWidget(self)
		tabWidget.addTab(self.tabAbout(),"About")
		tabWidget.addTab(self.tabInstructions(),"Instructions")
		tabWidget.addTab(self.tabLicense(),"License")

		hlay = QtWidgets.QHBoxLayout()
		hlay.addStretch()
		hlay.addWidget(pbClose)

		vlay = QtWidgets.QVBoxLayout()
		vlay.addWidget(title)
		vlay.addWidget(tabWidget)
		vlay.addLayout(hlay)

		pbClose.clicked.connect(self.close)
		self.setLayout(vlay)
		self.setModal(True)
		self.setMinimumSize(512,360)

	def tabAbout(self):
		tab = QtWidgets.QWidget()
		label = QtWidgets.QLabel(
			"<p align='center'>"
			"<b>" + APPNAME + "</b>&nbsp;" + VERSION + "<br><br><i>Create your own control center quickly & easily.</i>"
			"<br><br>Copyright Thierry Deseez 2008"
			"<br>Copyright Didier Spaier 2016 (didier~at~slint~dot~fr)<br>"
			"<br>Copyright Dimitris Tzemos 2022 - Ported to python3 (dijemos~at~gmail~dot~com)<br>"
			"</p>"
		)
		vlay = QtWidgets.QVBoxLayout()
		vlay.addWidget(label)

		tab.setLayout(vlay)

		return tab

	def tabInstructions(self):
		tab = QtWidgets.QWidget()
		textView = QtWidgets.QTextBrowser()
		textContent = QString("")
		vlay = QtWidgets.QVBoxLayout()

		file = QtCore.QFile("/usr/share/qcontrolcenter/INSTRUCTIONS.txt")
		if (file.open(QtCore.QFile.ReadOnly)):
			text = file.readAll()
			codec = QtCore.QTextCodec.codecForHtml(text)
			textView.append(str(text.data().decode('UTF-8')).strip("\r\n"))
			textView.moveCursor(QtGui.QTextCursor.Start)
				
		textContent = None
		vlay.addWidget(textView)
		tab.setLayout(vlay)
		
		return tab

	def tabLicense(self):
		tab = QtWidgets.QWidget()
		textView = QtWidgets.QTextBrowser()
		textContent = QString("")
		vlay = QtWidgets.QVBoxLayout()

		file = QtCore.QFile("/usr/share/qcontrolcenter/LICENSE.html")
		if (file.open(QtCore.QFile.ReadOnly)):
			text = file.readAll()
			codec = QtCore.QTextCodec.codecForHtml(text)
			textView.append(str(text.data().decode('UTF-8')).strip("\r\n"))	
			textView.moveCursor(QtGui.QTextCursor.Start)
			
		textContent = None
		vlay.addWidget(textView)
		tab.setLayout(vlay)

		return tab
