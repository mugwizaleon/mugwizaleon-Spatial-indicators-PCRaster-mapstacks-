# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TimeSeries.ui'
#
# Created: Fri Jan 17 00:50:06 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PCRaster(object):
    def setupUi(self, PCRaster):
        PCRaster.setObjectName(_fromUtf8("PCRaster"))
        PCRaster.resize(535, 292)
        self.txtBaseDir2_5 = QtGui.QLineEdit(PCRaster)
        self.txtBaseDir2_5.setGeometry(QtCore.QRect(130, 10, 291, 31))
        self.txtBaseDir2_5.setObjectName(_fromUtf8("txtBaseDir2_5"))
        self.label_11 = QtGui.QLabel(PCRaster)
        self.label_11.setGeometry(QtCore.QRect(10, 20, 101, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setTextFormat(QtCore.Qt.AutoText)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.btnBaseDir_3 = QtGui.QPushButton(PCRaster)
        self.btnBaseDir_3.setGeometry(QtCore.QRect(450, 10, 47, 30))
        self.btnBaseDir_3.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/spatialmetrics/dir.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnBaseDir_3.setIcon(icon)
        self.btnBaseDir_3.setIconSize(QtCore.QSize(22, 22))
        self.btnBaseDir_3.setObjectName(_fromUtf8("btnBaseDir_3"))
        self.listWidget = QtGui.QListWidget(PCRaster)
        self.listWidget.setGeometry(QtCore.QRect(330, 80, 171, 191))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.pushButton_5 = QtGui.QPushButton(PCRaster)
        self.pushButton_5.setGeometry(QtCore.QRect(240, 200, 61, 27))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(PCRaster)
        self.pushButton_6.setGeometry(QtCore.QRect(240, 240, 61, 27))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_7 = QtGui.QPushButton(PCRaster)
        self.pushButton_7.setGeometry(QtCore.QRect(330, 50, 171, 27))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.comboBox = QtGui.QComboBox(PCRaster)
        self.comboBox.setGeometry(QtCore.QRect(10, 80, 221, 27))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.label_15 = QtGui.QLabel(PCRaster)
        self.label_15.setGeometry(QtCore.QRect(10, 60, 231, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setTextFormat(QtCore.Qt.AutoText)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.line_18 = QtGui.QFrame(PCRaster)
        self.line_18.setGeometry(QtCore.QRect(10, 180, 301, 20))
        self.line_18.setFrameShape(QtGui.QFrame.HLine)
        self.line_18.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_18.setObjectName(_fromUtf8("line_18"))
        self.line_19 = QtGui.QFrame(PCRaster)
        self.line_19.setGeometry(QtCore.QRect(10, 260, 301, 20))
        self.line_19.setFrameShape(QtGui.QFrame.HLine)
        self.line_19.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_19.setObjectName(_fromUtf8("line_19"))
        self.label_16 = QtGui.QLabel(PCRaster)
        self.label_16.setGeometry(QtCore.QRect(20, 200, 201, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setTextFormat(QtCore.Qt.AutoText)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.label_17 = QtGui.QLabel(PCRaster)
        self.label_17.setGeometry(QtCore.QRect(30, 240, 171, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setTextFormat(QtCore.Qt.AutoText)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.line_20 = QtGui.QFrame(PCRaster)
        self.line_20.setGeometry(QtCore.QRect(10, 220, 301, 20))
        self.line_20.setFrameShape(QtGui.QFrame.HLine)
        self.line_20.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_20.setObjectName(_fromUtf8("line_20"))
        self.line_5 = QtGui.QFrame(PCRaster)
        self.line_5.setGeometry(QtCore.QRect(0, 190, 20, 81))
        self.line_5.setFrameShape(QtGui.QFrame.VLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.line_6 = QtGui.QFrame(PCRaster)
        self.line_6.setGeometry(QtCore.QRect(220, 190, 20, 81))
        self.line_6.setFrameShape(QtGui.QFrame.VLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        self.line_7 = QtGui.QFrame(PCRaster)
        self.line_7.setGeometry(QtCore.QRect(300, 190, 20, 81))
        self.line_7.setFrameShape(QtGui.QFrame.VLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.label_18 = QtGui.QLabel(PCRaster)
        self.label_18.setGeometry(QtCore.QRect(10, 120, 231, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setTextFormat(QtCore.Qt.AutoText)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.comboBox_2 = QtGui.QComboBox(PCRaster)
        self.comboBox_2.setGeometry(QtCore.QRect(10, 140, 221, 27))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))

        self.retranslateUi(PCRaster)
        QtCore.QMetaObject.connectSlotsByName(PCRaster)

    def retranslateUi(self, PCRaster):
        PCRaster.setWindowTitle(QtGui.QApplication.translate("PCRaster", "visualization of PCRatser Timeseries", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("PCRaster", "Select Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBaseDir_3.setToolTip(QtGui.QApplication.translate("PCRaster", "Select a base directory", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setToolTip(QtGui.QApplication.translate("PCRaster", "Click to visualise", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("PCRaster", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_6.setToolTip(QtGui.QApplication.translate("PCRaster", "Click to visualise", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_6.setText(QtGui.QApplication.translate("PCRaster", "Graph", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_7.setText(QtGui.QApplication.translate("PCRaster", "PCRaster mapstacks ", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setToolTip(QtGui.QApplication.translate("PCRaster", "Available PCRatser map series", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("PCRaster", "List of corenames of the mapstacks ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("PCRaster", "visualisation of the mapstacks ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("PCRaster", "visualisation of TSS Graph", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("PCRaster", "List of Time series files", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setToolTip(QtGui.QApplication.translate("PCRaster", "Available PCRatser time series", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
