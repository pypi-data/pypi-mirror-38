# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spectra_lexer\gui_qt\plover_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PloverDialog(object):
    def setupUi(self, PloverDialog):
        PloverDialog.setObjectName("PloverDialog")
        PloverDialog.resize(550, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PloverDialog.sizePolicy().hasHeightForWidth())
        PloverDialog.setSizePolicy(sizePolicy)
        PloverDialog.setSizeGripEnabled(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout(PloverDialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.w_main = MainWidget(PloverDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_main.sizePolicy().hasHeightForWidth())
        self.w_main.setSizePolicy(sizePolicy)
        self.w_main.setObjectName("w_main")
        self.horizontalLayout.addWidget(self.w_main)

        self.retranslateUi(PloverDialog)
        QtCore.QMetaObject.connectSlotsByName(PloverDialog)

    def retranslateUi(self, PloverDialog):
        _translate = QtCore.QCoreApplication.translate
        PloverDialog.setWindowTitle(_translate("PloverDialog", "Spectra Lexer"))

from spectra_lexer.gui_qt.main_widget import MainWidget
from . import resources_rc
