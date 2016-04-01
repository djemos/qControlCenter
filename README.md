# qControlCenter
qControlCenter lets you easily and quickly build a control center for your distribution. Can be useful if you don't like the control center of your distro, or if you distro doesn't have any.


FEATURES:
- absolutely lightweight
- very quick & simple configuration
- few requirements
- should work on any distro

REQUIREMENTS:
- Qt (I mean qt4)
- python
- pyqt4 (qt4 bindings for python)

CHANGELOG:
  Version 0.1 (launched 2008/05/20)

INSTALL:
- click "Download ZIP" and unzip the zipped archive or clone the repository
- type the following commands :
  # cd qcontrolcenter
  # python qcontrolcenter.py
  or
  # python qcontrolcenter.py /path/to/a/spectific/structure/directory

SETUP:

STEP 1
In order to use qControlCenter you have to create a main structure directory. For instance : 

  # mkdir /etc/qcontrolcenter

By default, qControlCenter uses /etc/qcontrolcenter as base structure directory.

STEP 2
Inside the folder created above, create subdirectories corresponding to the control center categories. Example :

  # cd /etc/qcontrolcenter
  # mkdir Boot
  # mkdir Devices
  # mkdir NetworkAndInternet
  # mkdir Security
  # mkdir System

STEP 3
You have to fill those directories with some '.desktop' files. Most of them are usually located in '/usr/share/applications'. You may copy or link the .desktop files in a subdirectory of your choice. Example :

  # cd /etc/qcontrolcenter/Devices
  # ln -s /usr/share/applications/cups.desktop
  # ln -s /usr/share/applications/hplip.desktop
  # ln -s /usr/share/applications/nvidia-settings.desktop


STEP 4
You may create an icon for your section. qControlCenter uses the file named 'icon.png' in your subdirectory as icon for the section (example : /etc/qcontrolcenter/Devices/icon.png)


STEP 5
You also may want to customize the name of the section in your language. Create a file named 'folder.ini' (example : /etc/qcontrolcenter/Devices/folder.ini) and write it like this :

default=Hardware
fr=Périphériques
it=...
de=...
ru=...

qControlCenter detects automatically your language.
Note : 'default=' means english.

LICENSE:
  G.P.L. 2.0
 
HISTORY:
QControlCenter's author is Thierry Deseez.

On Thu, 22 Oct 2015 Thierry agreed that Didier Spaier take over the maintainance of the project.
