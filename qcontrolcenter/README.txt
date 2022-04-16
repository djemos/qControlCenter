- qControlCenter v0.3 -
----------------------

ABOUT:
------
 qControlCenter lets you easily and quickly build a control center for your distribution.
 Can be useful if you don't like the control center of your distro, or if your distro doesn't have any.

FEATURES:
---------
- absolutely lightweight
- very quick & simple configuration
- few requirements
- should work on any distro

REQUIREMENTS:
-------------
- Qt5
- python3
- pyqt5 (qt5 bindings for python3)

CHANGELOG:
----------
  Version 0.1 (launched 2008/05/20) - python2 and PyQt4
  Version 0.3 (launced 2020/01/21) - Ported to python3 and PyQt5
  
  NOTE: To open html pages in Version 0.3 from .desktop files use this syntax Exec=http://URL e.g. Exec=http://www.slackel.gr or
  Exec=https://slint.fr

INSTALL:
--------
- uncompress source tarball
- launch :
	# cd qcontrolcenter
	# python3 qcontrolcenter.py
	or
	# python3 qcontrolcenter.py /path/to/a/spectific/structure/directory

qControlCenter setup INSTRUCTIONS:
----------------------------------
	STEP 1
	------
	In order to use qControlCenter you have to create a main structure directory. For instance : 
	
	# mkdir /etc/qcontrolcenter
	
	By default, qControlCenter uses /etc/qcontrolcenter as base structure directory.
	
	
	STEP 2
	------
	Inside the folder created above, create subdirectories corresponding to the control center categories. Example :
	
	# cd /etc/qcontrolcenter
	# mkdir Boot
	# mkdir Devices
	# mkdir NetworkAndInternet
	# mkdir Security
	# mkdir System
	
	
	STEP 3
	------
	You have to fill those directories with some '.desktop' files. Most of them are usually located in '/usr/share/applications'.
	You may copy or link the .desktop files in a subdirectory of your choice. Example :
	
	# cd /etc/qcontrolcenter/Devices
	# ln -s /usr/share/applications/cups.desktop
	# ln -s /usr/share/applications/hplip.desktop
	# ln -s /usr/share/applications/nvidia-settings.desktop
	
	
	STEP 4
	------
	You may create an icon for your section. 
	qControlCenter uses the file named 'icon.png' in your subdirectory as icon for the section (example : /etc/qcontrolcenter/Devices/icon.png)
	
	
	STEP 5
	------
	You also may want to customize the name of the section in your language. 
	Create a file named 'folder.ini' (example : /etc/qcontrolcenter/Devices/folder.ini) and write it like this :
	
	default=Hardware
	fr=Périphériques
	it=...
	de=...
	ru=...
	
	qControlCenter detects automatically your language.
	Note : 'default=' means english.

LICENSE:
--------
 G.P.L. 2.0

CONTACT:
--------
 - author : Thierry Deseez
 - email : pizza~dot~tony~at~free~dot~fr
 - former maintainer : Didier Spaier
 - email : didier~at~slint~dot~fr
 - maintainer : Dimitris Tzemos
 - email: dijemos~at~gmail~dot~com
 - website : https://github.com/djemos/qControlCenter
