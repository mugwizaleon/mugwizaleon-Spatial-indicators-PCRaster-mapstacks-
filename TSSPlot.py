# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TSSPlot.ui'
#
# Created: Thu Feb  6 13:44:50 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(531, 289)
        self.widget = matplotlibWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 10, 521, 271))
        self.widget.setObjectName(_fromUtf8("widget"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

from matplotlibwidgetFile import matplotlibWidget
