#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright Thierry Deseez 2008
# Copyright Didier Spaier 2016, 2017
# Copyright Dimitris Tzemos 2022 - Ported to python3

import sys, os, shutil

if sys.version_info[0] >= 3:
	unicode = str
	
from PyQt5.QtWidgets import *
import xdg.DesktopEntry
import xdg.IconTheme
# import xdg.Exceptions as exc
# import xdg.BaseDirectory as bd
from PyQt5 import QtCore, QtGui, QtWidgets #works for pyqt5
from PyQt5.QtCore import QUrl, QObject, pyqtSignal
from PyQt5.QtGui import QDesktopServices
from helpDialog import helpDialog

# *** SOME GENERAL FUNCTIONS ***
# We recommend that the sysadmin or distribution maintainer installs the
# base structure as /etc/skel/.qcontrolcenter
# In that case a user created after that will get a copy of this structue as
# ~/.qcontrolcenter
def getBaseStructureDirectoryPath():
	home_dir = os.path.expanduser("~")
	base_dir = os.path.join(home_dir,".qcontrolcenter")
	if len(sys.argv) == 2:
		tmp_dir = sys.argv[len(sys.argv)-1]
		if os.path.exists( tmp_dir ):
			base_dir = tmp_dir
	return base_dir
# The window title is set to the argument of the command case occuring,
# else to the value of the environment variable QCONTROLCENTERTITLE if set
# else to qControlCenter.
# 

def getWindowTitle():
	#window_title = "qControlCenter"
	window_title = "Slackel Control Center"
	if os.getenv('QCONTROLCENTERTITLE') != None:
		window_title = os.getenv('QCONTROLCENTERTITLE')
	return window_title

def getLanguage():
	lng = str(QtCore.QLocale.system().name()).split("_")[0]
	if lng == "en" or lng == "us":
		lng = "default"
	return lng

# *** GLOBAL VARIABLES ***
CONFIG_DIR = getBaseStructureDirectoryPath()
PIXMAPS_DIR = "/usr/share/pixmaps"
ICONS_DIR = "/usr/share/icons"
FOLDER_INI = "folder.ini"
FOLDER_ICON = "icon.png"
LANG = getLanguage()
TITLE = getWindowTitle()
TRUC = "qControlCenter"
print (TRUC, "Started ...")
print (TRUC, "window title =", TITLE)
print (TRUC, "tree =", CONFIG_DIR)
print (TRUC, "Language used =", LANG)
if not os.path.exists(CONFIG_DIR):
	if os.path.exists('/etc/skel/.qcontrolcenter'):
		shutil.copytree('/etc/skel/.qcontrolcenter',CONFIG_DIR)
	else:
		print ("No base structure directory found.")
		print ("Please read the instructions in this document:")
		print ("/usr/share/qcontrolcenter/INSTRUCTIONS.txt")

# *** MAIN CLASS ***
"""
layout:
	dock (QtWidgets.QDockWindow)
		# List widget docked on the left on the windows
		# It will site the categories (sub-directories of base_dir)
		self.contentsWidget (QtWidgets.QlistWidget(dock))
	self.textBrowser (QtWidgets.QTextBroowser)
		# Text browser in the left space in the window, hnece one the
		# right of the lsit widget.
		self.setCentralWidget (self.textBrowser)"""
class ConfigDialog(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.process = QtCore.QProcess()
		dock = QtWidgets.QDockWidget(self.tr(u"Categories"), self)
# The dock be non movable, non closable and non floatable by the user. 
		dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
		dock.font().setBold(True)
#		dock.setFont( QtWidgets.QFont(dock.font()) )
		self.contentsWidget = QtWidgets.QListWidget(dock)
		self.contentsWidget.setSpacing(1)
		self.contentsWidget.setAlternatingRowColors(True)
		self.contentsWidget.setIconSize(QtCore.QSize(32, 32))
		self.textBrowser = QtWidgets.QTextBrowser()
		self.textBrowser.setOpenLinks(False)
		self.setCentralWidget(self.textBrowser)
# When an URL is clicked in the central widget (text widget),
# the corresponding program is launched
		self.textBrowser.anchorClicked.connect(self.launchProgram)
# When the item (category) in the list widget is changed we change the
# page seen in the text browser, that will include information taken from
# the .desktop files in that category (folder in CONFIG_DIR).
		self.contentsWidget.currentItemChanged[QListWidgetItem, QListWidgetItem].connect(self.changePage)
		# initialize (populates) the main window
		# This populates the dock with the list of categories
		self.initContentsWidget()
		# Set the initially  highligted category to be the first one.
		self.contentsWidget.setCurrentRow(0)
		# set the widget for the dock widget to the list of categories
		# whose we just defined the layout in initContentsWidget.
		# This implicitely shows (displays) the widget as the dock widget
		# was not yet visible
		dock.setWidget(self.contentsWidget)
		helpButton = QtWidgets.QPushButton(QtGui.QIcon("/usr/share/qcontrolcenter/icons/info.png"),"")
		quitButton = QtWidgets.QPushButton(QtGui.QIcon("/usr/share/qcontrolcenter/icons/exit.png"),"")
		self.statusBar().addPermanentWidget(helpButton, 0)
		self.statusBar().addPermanentWidget(quitButton, 0)
		helpButton.clicked.connect(self.showAbout)
		quitButton.clicked.connect(self.close)
		self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
		self.setWindowTitle(self.tr(getWindowTitle()))
		self.setWindowIcon(QtGui.QIcon("icons/arch-logo.png"))
		self.setMinimumSize(640,480)
	

		def show_monitor_temp(self, URL):
			print("show_monitor_temp")
			print(URL.toString())
        		
	def showAbout(self):
		helpDlg = helpDialog(self)
		helpDlg.show()
		
	def launchProgram(self, programName):
		if programName.toString().startswith("http://") or programName.toString().startswith("https://"): # If it is an Url link, open it with openUrl()
			QDesktopServices.openUrl(QUrl(programName.toString()))
		else:	
			self.process.startDetached(programName.toString())

	def changePage(self):
		# init values
		#self.contentsWidget.currentItem().setSelected(True)
		sectionName = self.contentsWidget.currentItem().data(QtCore.Qt.UserRole).strip()
		html = ""
		current_dir = os.path.join( CONFIG_DIR, unicode(sectionName) )
		current_column = 1
		
		# retrieve program informations from '.desktop' files
		folder = QtCore.QDir(current_dir)
		folder.setFilter(QtCore.QDir.Files)
		# filename include all info about each file in the current
		# directory, whose name is set as the current (highlighted) item
		# i.e. category in the dock. 
		for fileName in folder.entryInfoList():
			if not fileName.fileName().endswith(".desktop"):
				continue
			current_file_name = os.path.join( current_dir, unicode( fileName.fileName() ) )
			# Store the settings found in the .desktop file
			settings = xdg.DesktopEntry.DesktopEntry(filename=os.path.join( current_dir, (fileName.fileName())) )
			onlyShowIn = settings.getOnlyShowIn()
			notShowIn = settings.getNotShowIn()
			if 'XDG_CURRENT_DESKTOP' in os.environ and len(onlyShowIn) >0 and not os.environ['XDG_CURRENT_DESKTOP'] in onlyShowIn:
				continue
			if 'XDG_CURRENT_DESKTOP' in os.environ and len(notShowIn) >0 and os.environ['XDG_CURRENT_DESKTOP'] in notShowIn:
				continue
			if not 'XDG_CURRENT_DESKTOP' in os.environ and len(onlyShowIn) >0:
				continue
			beginGroup = settings.get("Desktop Entry")
			execName = settings.getExec()
			commentName = settings.getComment()
			genericName = settings.getGenericName()
			programName = settings.getName()
			iconFileName = settings.getIcon()
			# We display the first found icon among the themes list below.
			# TODO: allow to provide a list of themes in a configuration file
			# like /etc/slaptgetrc, that could also set the window title.
			# As is, the themes are those shipped in Slint.
			iconName = xdg.IconTheme.getIconPath(iconFileName,64, "Adwaita")
			if (iconName == None):
				# package oxygen-icons
				iconName = xdg.IconTheme.getIconPath(iconFileName,64, "oxygen")
			if (iconName == None):
				# nuvola is shipped in kdeartwork
				iconName = xdg.IconTheme.getIconPath(iconFileName,64, "nuvola")
			if (iconName == None):
				# packages tango-icon-themes{,-extra} 
				iconName = xdg.IconTheme.getIconPath(iconFileName,64, "Tango")
			if (iconName == None):
				# hicolor is shipped in gnome_themes_standard
				# It is the default.
				iconName = xdg.IconTheme.getIconPath(iconFileName,64, "hicolor")
			# build cells in html page
			if current_column == 1:
				html += (
						"<tr>" +
						self.cellBuilder(iconName, programName, commentName, execName) +
						"<td width='10%'>&nbsp;</td>"
						)
			elif current_column == 2:
				html += (
						self.cellBuilder(iconName, programName, commentName, execName) +
						"</tr><tr><td colspan='5'><hr></td></tr>"
						)

			if current_column == 1 : current_column += 1
			elif current_column == 2: current_column -= 1
				
		if current_column == 2:
			html += "</tr><tr><td colspan='5'><hr></td></tr>"
				
		# display html page in text browser
		self.textBrowser.setHtml(
				"<style type='text/css'>"
				"a:link {color: black;font-style: normal;text-decoration: none;}"
				"#a:hover {color: red;font-style: normal;font-weight:bold;text-decoration: none;}"
				"a:active {color: red;font-style: normal;font-weight:bold;text-decoration: none;}"
				".title {background-color: grey;color: white;}"
				".bob {background-color: #FFFFFF;}"
				".joe {background-color: #FFFFFF;}"
				".joe:hover {background-color: gray;}"
				"</style>"
				"<P align='center' valign='middle' class='title'>"
				"<strong><big>" + self.getSectionTitle(current_dir) + "</big></strong>"
				"</P><p></p>"
				"<table align='center' valign='top' bgcolor='white' border='0' cellpadding='0' cellspacing='0' width='100%'>"
				+ html +
				"</table>"
				)

	def cellBuilder(self, iconName, programName, commentName, execName):
		cell = (
				u"<td width='60' class='joe' valign='middle' align='left'>"
				u"<a href='" + unicode(execName) + u"'><img width='48' height='48' src='" + unicode(iconName) + u"'></a>"
				u"</td>"
				u"<td width='30%'>"
				u"<a href='" + unicode(execName) + u"'><b>"+ unicode(programName) + u"</b><br><em>" + unicode(commentName) + u"</em></a>"
				u"</td>"
				)
		
		return cell
    # This method populates the list of categories in the left hand dock.
	def initContentsWidget(self):
		folder = QtCore.QDir(CONFIG_DIR)
		folder.setFilter(QtCore.QDir.AllDirs)
		# Loop inside the categories in the config tree
		for folderName in folder.entryInfoList():
			# Condider only category names of al laast three characters
			if len(folderName.fileName()) > 2:
				current_dir = os.path.join( CONFIG_DIR, unicode(folderName.fileName()) )
				# Bear in mind that self.contentsWidget is a docked list item
				# configButton is an item in that list
				configButton = QtWidgets.QListWidgetItem( self.contentsWidget)
				configButton.setIcon(QtGui.QIcon( os.path.join(current_dir, FOLDER_ICON) ) )
				configButton.setText( self.getSectionTitle(current_dir) )	
							
				#configButton.setText(folderName.fileName())
				
				configButton.setTextAlignment( QtCore.Qt.AlignLeft )
				# Align center vertically (Didier)
				configButton.setTextAlignment( QtCore.Qt.AlignVCenter )
				configButton.setData( QtCore.Qt.UserRole, QtCore.QVariant( folderName.fileName()) )
				configButton.setFont(QtGui.QFont("DejaVu Sans", 11, QtGui.QFont.Bold))

	def getSectionTitle(self, dir_name):
		titleList = unicode(dir_name).split("/")
		title = titleList[len(titleList)-1]
		
		file_name = os.path.join(dir_name, FOLDER_INI)
		
		if not os.path.exists(file_name):
			return title
		
		settings = QtCore.QSettings(file_name, QtCore.QSettings.IniFormat)
		QtCore.QSettings.setIniCodec(settings,"UTF-8") # Sets the codec for accessing INI files (including .conf files on Unix) 

		if settings.value(LANG).strip() != "":
			title = unicode(settings.value(LANG).strip())

		"""
		#if len(LANG) > 1
		if settings.value(LANG).toString() != "":
			title = unicode(settings.value(LANG).toString(), "utf-8")
		elif settings.value("default").toString() != "":
			title = unicode(settings.value("default").toString(), "utf-8")
		"""
		return title

# *** MAIN LOOP ***
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	dialog = ConfigDialog()
	dialog.show()
	sys.exit(app.exec_())
