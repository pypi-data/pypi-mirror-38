# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spectra_lexer\gui_qt\main_widget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName("MainWidget")
        MainWidget.resize(520, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWidget.sizePolicy().hasHeightForWidth())
        MainWidget.setSizePolicy(sizePolicy)
        MainWidget.setMinimumSize(QtCore.QSize(510, 400))
        self.layout_main = QtWidgets.QHBoxLayout(MainWidget)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setObjectName("layout_main")
        self.w_input = InputWidget(MainWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_input.sizePolicy().hasHeightForWidth())
        self.w_input.setSizePolicy(sizePolicy)
        self.w_input.setMinimumSize(QtCore.QSize(150, 0))
        self.w_input.setMaximumSize(QtCore.QSize(150, 16777215))
        self.w_input.setObjectName("w_input")
        self.layout_main.addWidget(self.w_input)
        self.w_output = OutputWidget(MainWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_output.sizePolicy().hasHeightForWidth())
        self.w_output.setSizePolicy(sizePolicy)
        self.w_output.setMinimumSize(QtCore.QSize(0, 0))
        self.w_output.setObjectName("w_output")
        self.layout_main.addWidget(self.w_output)

        self.retranslateUi(MainWidget)
        self.w_input.querySelected['QString','QString'].connect(MainWidget.query)
        self.w_input.queryBestStroke['PyQt_PyObject','QString'].connect(MainWidget.query_best)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        _translate = QtCore.QCoreApplication.translate
        MainWidget.setWindowTitle(_translate("MainWidget", "MAIN"))

from spectra_lexer.gui_qt.input_widget import InputWidget
from spectra_lexer.gui_qt.output_widget import OutputWidget
