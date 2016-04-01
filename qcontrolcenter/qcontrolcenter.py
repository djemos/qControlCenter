#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os#, string
from PyQt4 import QtCore, QtGui
from helpDialog import helpDialog

# *** SOME GENERAL FUNCTIONS ***
def getBaseStructureDirectoryPath():
	base_dir = "/etc/qcontrolcenter"
	tmp_dir = ""
	
	if len(sys.argv) > 1:
		tmp_dir =  sys.argv[len(sys.argv)-1]
		if os.path.exists( tmp_dir ):
			base_dir = tmp_dir
	
	return base_dir

def getLanguage():
	lng = str(QtCore.QLocale.system().name()).split("_")[0]
	if lng == "en" or lng == "us":
		lng = "default"
	return lng

# *** GLOBAL VARIABLES ***
#APP_CONF = QtCore.QSettings("qcontrolcenter")
#CONFIG_DIR = str(APP_CONF.value("base_directory").toString())
CONFIG_DIR = getBaseStructureDirectoryPath()#"/etc/archcontrol"
#APP_CONF.setValue("basedir", QtCore.QVariant(CONFIG_DIR))
PIXMAPS_DIR = "/usr/share/pixmaps"
ICONS_DIR = "/usr/share/icons"
KDE_DIR = unicode(os.getenv('KDEDIR'))
FOLDER_INI = "folder.ini"
FOLDER_ICON = "icon.png"
LANG = getLanguage()
TRUC = " [qControlCenter]"

#if not APP_CONF.value("basedir").toString().isEmpty():
	#CONFIG_DIR = unicode(APP_CONF.value("basedir").toString())

print TRUC, "Started ..."
print TRUC, "Base strutcure directory used =", CONFIG_DIR
print TRUC, "Language used =", LANG

# *** MAIN CLASS ***
class ConfigDialog(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		self.process = QtCore.QProcess()
		
		dock = QtGui.QDockWidget(self.tr("Categories"), self)
		dock.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
		font = dock.font()
		font.setBold(True)
		dock.setFont( QtGui.QFont(font) )
		#dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
		
		self.contentsWidget = QtGui.QListWidget(dock)
		self.contentsWidget.setMaximumWidth(200)
		self.contentsWidget.setSpacing(1)
		self.contentsWidget.setAlternatingRowColors(True)
		#self.contentsWidget.setViewMode(QtGui.QListView.IconMode)
		#self.contentsWidget.setIconSize(QtCore.QSize(48, 48))
		#self.contentsWidget.setMovement(QtGui.QListView.Static)
		
		#dock2 = QtGui.QDockWidget(self)
		#dock2.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
		#self.label = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, dock2)

		
		self.textBrowser = QtGui.QTextBrowser()
		self.textBrowser.setOpenLinks(False)

		self.setCentralWidget(self.textBrowser)
		
		self.connect(self.process, QtCore.SIGNAL("finished(int)"), self.processFinished)
		self.connect(self.textBrowser, QtCore.SIGNAL("anchorClicked(const QUrl &)"), self.launchProgram)
		self.connect(self.contentsWidget, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.changePage)
		#self.connect(self.contentsWidget, QtCore.SIGNAL("currentTextChanged(const QString &)"), self.changePage)
		
		self.initContentsWidget()
		self.contentsWidget.setCurrentRow(0)
		
		dock.setWidget(self.contentsWidget)
		
		helpButton = QtGui.QPushButton(QtGui.QIcon("icons/info.png"),"")
		quitButton = QtGui.QPushButton(QtGui.QIcon("icons/exit.png"),"")
		self.statusBar().addPermanentWidget(helpButton, 0)
		self.statusBar().addPermanentWidget(quitButton, 0)
		self.connect(helpButton, QtCore.SIGNAL("clicked()"), self.showAbout)
		self.connect(quitButton, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))
		
		self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
		#self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock2)
		self.statusBar().showMessage(self.tr("> Select a program"), 0)
		self.setWindowTitle(self.tr("qControlCenter"))
		self.setWindowIcon(QtGui.QIcon("icons/arch-logo.png"))
		self.setMinimumSize(640,480)
		
		#if not os.path.exists(CONFIG_DIR):
			#self.createStructure()
		
		#print "Directory structure used :", CONFIG_DIR
		
	def showAbout(self):
		helpDlg = helpDialog(self)
		helpDlg.show()
	
	def createStructure(self):
		global CONFIG_DIR

		text, ok = QtGui.QInputDialog.getText(
										self,
										self.tr("Create Directory Strucure ?"),
										self.tr(
											"No directory structure found.\n"
											"Please provide a base strucutre directory :"
											),
										QtGui.QLineEdit.Normal,
										CONFIG_DIR
										)
		if ok and not text.isEmpty():
			if not os.path.exists(text):
				if os.mkdir(text):
					CONFIG_DIR = text
				else:
					print TRUC, "could not create directory", text
					self.close()
				
			folder = QtCore.QDir(CONFIG_DIR)
			folder.setFilter(QtCore.QDir.AllDirs)
			if folder.entryList().count() == 0:
				jojo = ["System", "Software", "Devices", "Regional"]
				for jo in jojo:
					os.mkdir( os.path.join(CONFIG_DIR, jo) )
		else:
			self.close()
		
	def launchProgram(self, programName):
		self.process.start(programName.toString())
		
		if not self.process.waitForStarted():
			print TRUC, "Error : program %s could not be started." % ( str(programName.toString()) )
			self.statusBar().showMessage(self.tr("program '%1' could not be started.").arg(programName.toString()), 0)
			return
		
		print TRUC, "Program %s started ..." % ( str(programName.toString()) )
		
		QtGui.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)
		self.setDisabled(True)
		self.contentsWidget.setDisabled(True)
		self.textBrowser.setDisabled(True)
		self.statusBar().showMessage(self.tr("Program '%1' launched ...").arg(programName.toString()), 0)
	
	def processFinished(self):
		print TRUC, "Program ended."
		
		QtGui.QApplication.restoreOverrideCursor()
		self.setDisabled(False)
		self.contentsWidget.setDisabled(False)
		self.textBrowser.setDisabled(False)
		self.statusBar().showMessage(self.tr("> Select a program"), 0)

	def changePage(self):
		# init values
		#self.contentsWidget.currentItem().setSelected(True)
		sectionName = self.contentsWidget.currentItem().data(QtCore.Qt.UserRole).toString()
		commentName = ""
		commentNameLng = ""
		genericName = ""
		genericNameLng = ""
		programName = ""
		execName = ""
		iconName = ""
		html = ""
		current_dir = os.path.join( CONFIG_DIR, unicode(sectionName) )
		current_column = 1
		
		# retrieve program informations from '.desktop' files
		folder = QtCore.QDir(current_dir)
		folder.setFilter(QtCore.QDir.Files)
		for fileName in folder.entryInfoList():
			if fileName.fileName().endsWith(".desktop"):
				current_file_name = os.path.join( current_dir, unicode( fileName.fileName() ) )

				settings = QtCore.QSettings(current_file_name, QtCore.QSettings.IniFormat)
				settings.beginGroup("Desktop Entry")
				execName = settings.value("Exec").toString()
				commentName = settings.value("Comment").toString()
				genericName = settings.value("GenericName").toString()
				programName = settings.value("Name").toString()
				iconName = settings.value("Icon").toString()
				if len(LANG) == 2:
					commentNameLng = unicode(settings.value("Comment[" + LANG + "]").toString(), "utf-8")
					genericNameLng = unicode(settings.value("GenericName[" + LANG + "]").toString(), "utf-8")
				settings.endGroup()
				
				if len(commentNameLng) > 0:
					commentName = commentNameLng
				elif len(genericNameLng) > 0:
					commentName = genericNameLng
				 
				if len(commentName) < 1:
					commentName = genericName
				"""
				if len(LANG) > 1:
					if ( settings.value("Comment[" + LANG + "]").toString() ) != "":
						commentName = unicode(settings.value("Comment[" + LANG + "]").toString(), "utf-8")
					elif ( settings.value("GenericName[" + LANG + "]").toString() ) != "":
						commentName = unicode(settings.value("GenericName[" + LANG + "]").toString(), "utf-8")
				if len(commentName) < 1:
					commentName = settings.value("GenericName").toString()
				settings.endGroup()
				"""
				
				# build icon name
				iconName = self.iconNameBuilder(iconName)
				
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

	def iconNameBuilder(self, name):
		# this is a full path icon name
		if name.contains("/"):
			return name
		
		# check extension
		if name.indexOf(".", name.size()-4) < 0:
			name.append(".png")#print "index of" , name, "found"
		
		# guess icon path from multiple possible locations
		nameFound = "icons/unknown.png"
		locations =[
					os.path.join(PIXMAPS_DIR, unicode(name)),
					os.path.join(ICONS_DIR, unicode(name)),
					os.path.join(ICONS_DIR + "/hicolor/48x48/apps", unicode(name)),
					os.path.join(ICONS_DIR + "/hicolor/32x32/apps", unicode(name)),
					os.path.join(KDE_DIR + "/share/icons/default.kde/48x48/apps", unicode(name)),
					os.path.join(KDE_DIR + "/share/icons/default.kde/32x32/apps", unicode(name)),
					os.path.join(KDE_DIR + "/share/icons/hicolor/48x48/apps", unicode(name)),
					os.path.join(KDE_DIR + "/share/icons/hicolor/32x32/apps", unicode(name)),
					os.path.join(KDE_DIR + "/share/icons/kdeclassic/48x48/apps", unicode(name)),
					os.path.join(KDE_DIR + "/share/icons/kdeclassic/32x32/apps", unicode(name))
					]
		
		for location in locations:
			if os.path.exists(location):
				nameFound = location
				break
		
		return nameFound

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

	def initContentsWidget(self):
		folder = QtCore.QDir(CONFIG_DIR)
		folder.setFilter(QtCore.QDir.AllDirs)
		
		for folderName in folder.entryInfoList():
			if folderName.fileName().size() > 2:
				current_dir = os.path.join( CONFIG_DIR, unicode(folderName.fileName()) )
				
				configButton = QtGui.QListWidgetItem( self.contentsWidget)
				configButton.setIcon( QtGui.QIcon( os.path.join(current_dir, FOLDER_ICON) ) )
				configButton.setText( self.getSectionTitle(current_dir) )#configButton.setText(folderName.fileName())
				configButton.setTextAlignment( QtCore.Qt.AlignLeft )
				configButton.setData( QtCore.Qt.UserRole, QtCore.QVariant( folderName.fileName()) )
				#configButton.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
				#configButton.setFlags( QtCore.Qt.ItemIsEnabled)
				font = configButton.font()
				font.setBold(True)
				configButton.setFont( QtGui.QFont(font) )

	def getSectionTitle(self, dir_name):
		titleList = unicode(dir_name).split("/")
		title = titleList[len(titleList)-1]
		
		file_name = os.path.join(dir_name, FOLDER_INI)
		
		if not os.path.exists(file_name):
			return title
		
		settings = QtCore.QSettings(file_name, QtCore.QSettings.IniFormat)
		if settings.value(LANG).toString().trimmed() != "":
			title = unicode(settings.value(LANG).toString(), "utf-8")
		"""
		#if len(LANG) > 1:
		if settings.value(LANG).toString() != "":
			title = unicode(settings.value(LANG).toString(), "utf-8")
		elif settings.value("default").toString() != "":
			title = unicode(settings.value("default").toString(), "utf-8")
		"""
		return title

# *** MAIN LOOP ***
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	dialog = ConfigDialog()
	dialog.show()
	sys.exit(app.exec_())
