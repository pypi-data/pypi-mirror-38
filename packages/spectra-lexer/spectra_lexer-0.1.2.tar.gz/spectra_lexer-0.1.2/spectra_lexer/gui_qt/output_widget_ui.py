# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spectra_lexer\gui_qt\output_widget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OutputWidget(object):
    def setupUi(self, OutputWidget):
        OutputWidget.setObjectName("OutputWidget")
        OutputWidget.resize(330, 394)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OutputWidget.sizePolicy().hasHeightForWidth())
        OutputWidget.setSizePolicy(sizePolicy)
        OutputWidget.setMinimumSize(QtCore.QSize(330, 0))
        self.vboxlayout = QtWidgets.QVBoxLayout(OutputWidget)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout.setObjectName("vboxlayout")
        self.w_title = QtWidgets.QLineEdit(OutputWidget)
        self.w_title.setMinimumSize(QtCore.QSize(0, 22))
        self.w_title.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.w_title.setFont(font)
        self.w_title.setFrame(True)
        self.w_title.setReadOnly(True)
        self.w_title.setPlaceholderText("")
        self.w_title.setObjectName("w_title")
        self.vboxlayout.addWidget(self.w_title)
        self.w_text = OutputTextWidget(OutputWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_text.sizePolicy().hasHeightForWidth())
        self.w_text.setSizePolicy(sizePolicy)
        self.w_text.setMinimumSize(QtCore.QSize(0, 180))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.w_text.setFont(font)
        self.w_text.setUndoRedoEnabled(False)
        self.w_text.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.w_text.setReadOnly(True)
        self.w_text.setAcceptRichText(False)
        self.w_text.setObjectName("w_text")
        self.vboxlayout.addWidget(self.w_text)
        self.w_info = QtWidgets.QFrame(OutputWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_info.sizePolicy().hasHeightForWidth())
        self.w_info.setSizePolicy(sizePolicy)
        self.w_info.setMinimumSize(QtCore.QSize(0, 180))
        self.w_info.setMaximumSize(QtCore.QSize(16777215, 180))
        self.w_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.w_info.setObjectName("w_info")
        self.layout_info = QtWidgets.QVBoxLayout(self.w_info)
        self.layout_info.setContentsMargins(6, 6, 6, 6)
        self.layout_info.setSpacing(0)
        self.layout_info.setObjectName("layout_info")
        self.w_desc = QtWidgets.QLabel(self.w_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.w_desc.sizePolicy().hasHeightForWidth())
        self.w_desc.setSizePolicy(sizePolicy)
        self.w_desc.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.w_desc.setFont(font)
        self.w_desc.setLineWidth(1)
        self.w_desc.setText("")
        self.w_desc.setTextFormat(QtCore.Qt.AutoText)
        self.w_desc.setAlignment(QtCore.Qt.AlignCenter)
        self.w_desc.setWordWrap(True)
        self.w_desc.setObjectName("w_desc")
        self.layout_info.addWidget(self.w_desc)
        self.w_board = OutputBoardWidget(self.w_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.w_board.sizePolicy().hasHeightForWidth())
        self.w_board.setSizePolicy(sizePolicy)
        self.w_board.setMinimumSize(QtCore.QSize(310, 120))
        self.w_board.setMaximumSize(QtCore.QSize(310, 120))
        self.w_board.setObjectName("w_board")
        self.layout_info.addWidget(self.w_board, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.vboxlayout.addWidget(self.w_info)

        self.retranslateUi(OutputWidget)
        self.w_text.ruleSelected['QString','QString'].connect(OutputWidget.send_rule_info)
        QtCore.QMetaObject.connectSlotsByName(OutputWidget)

    def retranslateUi(self, OutputWidget):
        _translate = QtCore.QCoreApplication.translate
        OutputWidget.setWindowTitle(_translate("OutputWidget", "OUTPUT"))
        self.w_text.setPlaceholderText(_translate("OutputWidget", "Stroke a word to see its breakdown."))

from spectra_lexer.gui_qt.output_board_widget import OutputBoardWidget
from spectra_lexer.gui_qt.output_text_widget import OutputTextWidget
