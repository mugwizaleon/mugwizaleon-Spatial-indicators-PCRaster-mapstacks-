# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SIAnimation.ui'
#
# Created: Fri Jan 17 00:45:46 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SIDialog(object):
    def setupUi(self, SIDialog):
        SIDialog.setObjectName(_fromUtf8("SIDialog"))
        SIDialog.resize(309, 69)
        self.pushButton_2 = QtGui.QPushButton(SIDialog)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 20, 51, 41))
        self.pushButton_2.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/spatialmetrics/play1.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton = QtGui.QPushButton(SIDialog)
        self.pushButton.setGeometry(QtCore.QRect(70, 20, 51, 41))
        self.pushButton.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/spatialmetrics/maps.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_3 = QtGui.QPushButton(SIDialog)
        self.pushButton_3.setGeometry(QtCore.QRect(190, 20, 51, 41))
        self.pushButton_3.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/spatialmetrics/arrowright.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(SIDialog)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 20, 51, 41))
        self.pushButton_4.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/spatialmetrics/previous.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QtGui.QPushButton(SIDialog)
        self.pushButton_5.setGeometry(QtCore.QRect(250, 20, 51, 41))
        self.pushButton_5.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/spatialmetrics/next.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon4)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.txtBaseDir2_5 = QtGui.QLineEdit(SIDialog)
        self.txtBaseDir2_5.setGeometry(QtCore.QRect(250, 0, 31, 21))
        self.txtBaseDir2_5.setObjectName(_fromUtf8("txtBaseDir2_5"))
        self.label_15 = QtGui.QLabel(SIDialog)
        self.label_15.setGeometry(QtCore.QRect(110, 0, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_15.setFont(font)
        self.label_15.setTextFormat(QtCore.Qt.AutoText)
        self.label_15.setObjectName(_fromUtf8("label_15"))

        self.retranslateUi(SIDialog)
        QtCore.QMetaObject.connectSlotsByName(SIDialog)

    def retranslateUi(self, SIDialog):
        SIDialog.setWindowTitle(QtGui.QApplication.translate("SIDialog", "MAPS VIEW", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setToolTip(QtGui.QApplication.translate("SIDialog", "maps animation", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setToolTip(QtGui.QApplication.translate("SIDialog", "Go to the previous", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setStatusTip(QtGui.QApplication.translate("SIDialog", "Go to the next ", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setToolTip(QtGui.QApplication.translate("SIDialog", "Go to the start", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setToolTip(QtGui.QApplication.translate("SIDialog", "Go to the last ", None, QtGui.QApplication.UnicodeUTF8))
        self.txtBaseDir2_5.setText(QtGui.QApplication.translate("SIDialog", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("SIDialog", "Interval time for animation", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
