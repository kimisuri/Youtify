# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designs/get_music_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(782, 585)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.cancel_btn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Typewriter")
        font.setPointSize(12)
        self.cancel_btn.setFont(font)
        self.cancel_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancel_btn.setStyleSheet("QPushButton {\n"
"                        background-color: #bcbcbc;\n"
"                        border-style: solid;\n"
"                        border-radius: 10px;\n"
"                    }\n"
"                    QPushButton:pressed {\n"
"                        background-color: #DDA0DD;\n"
"                        border-style: inset;\n"
"                    }")
        self.cancel_btn.setObjectName("cancel_btn")
        self.gridLayout.addWidget(self.cancel_btn, 3, 1, 1, 1)
        self.ok_btn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Typewriter")
        font.setPointSize(12)
        self.ok_btn.setFont(font)
        self.ok_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ok_btn.setStyleSheet("QPushButton {\n"
"                        background-color: #bcbcbc;\n"
"                        border-style: solid;\n"
"                        border-radius: 10px;\n"
"                    }\n"
"                    QPushButton:pressed {\n"
"                        background-color: #DDA0DD;\n"
"                        border-style: inset;\n"
"                    }")
        self.ok_btn.setObjectName("ok_btn")
        self.gridLayout.addWidget(self.ok_btn, 3, 0, 1, 1)
        self.music_list = QtWidgets.QListWidget(Dialog)
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Typewriter")
        font.setPointSize(12)
        self.music_list.setFont(font)
        self.music_list.setStyleSheet("QListWidget\n"
"                        {\n"
"                            border : 1px solid black;\n"
"                            background : #eeeeee;\n"
"                            border-radius: 10px;\n"
"                                            }\n"
"                     QListWidget QScrollBar\n"
"                        {\n"
"                    background : #959995;\n"
"                        }\n"
"                            QListView::item:selected\n"
"                        {\n"
"                            border : 2px solid black;\n"
"                            background : #999999;\n"
"                        }")
        self.music_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.music_list.setObjectName("music_list")
        self.gridLayout.addWidget(self.music_list, 2, 0, 1, 2)
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Typewriter")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Results"))
        self.cancel_btn.setText(_translate("Dialog", "????????????"))
        self.ok_btn.setText(_translate("Dialog", "????"))
        self.label.setText(_translate("Dialog", "???????????????????? ????????????:"))
