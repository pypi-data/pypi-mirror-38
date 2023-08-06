# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spectra_lexer\gui_qt\input_widget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_InputWidget(object):
    def setupUi(self, InputWidget):
        InputWidget.setObjectName("InputWidget")
        InputWidget.resize(150, 394)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(InputWidget.sizePolicy().hasHeightForWidth())
        InputWidget.setSizePolicy(sizePolicy)
        InputWidget.setMinimumSize(QtCore.QSize(150, 0))
        self.vboxlayout = QtWidgets.QVBoxLayout(InputWidget)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout.setObjectName("vboxlayout")
        self.w_input = QtWidgets.QLineEdit(InputWidget)
        self.w_input.setEnabled(False)
        self.w_input.setMinimumSize(QtCore.QSize(0, 22))
        self.w_input.setMaximumSize(QtCore.QSize(16777215, 22))
        self.w_input.setFrame(True)
        self.w_input.setReadOnly(False)
        self.w_input.setObjectName("w_input")
        self.vboxlayout.addWidget(self.w_input)
        self.w_words = InputListWidget(InputWidget)
        self.w_words.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_words.sizePolicy().hasHeightForWidth())
        self.w_words.setSizePolicy(sizePolicy)
        self.w_words.setMinimumSize(QtCore.QSize(0, 180))
        self.w_words.setAutoScroll(False)
        self.w_words.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.w_words.setProperty("showDropIndicator", False)
        self.w_words.setObjectName("w_words")
        self.vboxlayout.addWidget(self.w_words)
        self.w_bottom = QtWidgets.QFrame(InputWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_bottom.sizePolicy().hasHeightForWidth())
        self.w_bottom.setSizePolicy(sizePolicy)
        self.w_bottom.setMinimumSize(QtCore.QSize(0, 180))
        self.w_bottom.setMaximumSize(QtCore.QSize(16777215, 180))
        self.w_bottom.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.w_bottom.setFrameShadow(QtWidgets.QFrame.Raised)
        self.w_bottom.setLineWidth(0)
        self.w_bottom.setObjectName("w_bottom")
        self._2 = QtWidgets.QVBoxLayout(self.w_bottom)
        self._2.setContentsMargins(0, 0, 0, 0)
        self._2.setObjectName("_2")
        self.w_strokes = InputListWidget(self.w_bottom)
        self.w_strokes.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_strokes.sizePolicy().hasHeightForWidth())
        self.w_strokes.setSizePolicy(sizePolicy)
        self.w_strokes.setMinimumSize(QtCore.QSize(0, 120))
        self.w_strokes.setAutoScroll(False)
        self.w_strokes.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.w_strokes.setProperty("showDropIndicator", False)
        self.w_strokes.setObjectName("w_strokes")
        self._2.addWidget(self.w_strokes)
        self.w_regex = QtWidgets.QCheckBox(self.w_bottom)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_regex.sizePolicy().hasHeightForWidth())
        self.w_regex.setSizePolicy(sizePolicy)
        self.w_regex.setMinimumSize(QtCore.QSize(0, 0))
        self.w_regex.setObjectName("w_regex")
        self._2.addWidget(self.w_regex, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.vboxlayout.addWidget(self.w_bottom)

        self.retranslateUi(InputWidget)
        self.w_input.textEdited['QString'].connect(InputWidget.lookup)
        self.w_words.itemSelected['QString'].connect(InputWidget.choose_word)
        self.w_strokes.itemSelected['QString'].connect(InputWidget.choose_stroke)
        self.w_regex.toggled['bool'].connect(InputWidget.set_regex)
        QtCore.QMetaObject.connectSlotsByName(InputWidget)

    def retranslateUi(self, InputWidget):
        _translate = QtCore.QCoreApplication.translate
        InputWidget.setWindowTitle(_translate("InputWidget", "INPUT"))
        self.w_input.setPlaceholderText(_translate("InputWidget", "No dictionary."))
        self.w_regex.setText(_translate("InputWidget", "Regex Search"))

from spectra_lexer.gui_qt.input_list_widget import InputListWidget
