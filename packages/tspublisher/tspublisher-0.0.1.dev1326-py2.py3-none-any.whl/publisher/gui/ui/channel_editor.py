# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'channel_editor.ui'
#
# Created: Wed Aug 22 16:50:02 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_channel_editor(object):
    def setupUi(self, channel_editor):
        channel_editor.setObjectName("channel_editor")
        channel_editor.resize(536, 424)
        self.verticalLayout_2 = QtGui.QVBoxLayout(channel_editor)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.header = QtGui.QFrame(channel_editor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        self.header.setFrameShape(QtGui.QFrame.StyledPanel)
        self.header.setFrameShadow(QtGui.QFrame.Raised)
        self.header.setObjectName("header")
        self.verticalLayout = QtGui.QVBoxLayout(self.header)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = TSTitle(self.header)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtGui.QFrame(self.header)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.verticalLayout_2.addWidget(self.header)
        self.channel_tbl = QtGui.QTableView(channel_editor)
        self.channel_tbl.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.channel_tbl.setAlternatingRowColors(True)
        self.channel_tbl.setSortingEnabled(True)
        self.channel_tbl.setObjectName("channel_tbl")
        self.channel_tbl.horizontalHeader().setStretchLastSection(False)
        self.channel_tbl.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.channel_tbl)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtGui.QLabel(channel_editor)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.msg = QtGui.QPlainTextEdit(channel_editor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.msg.sizePolicy().hasHeightForWidth())
        self.msg.setSizePolicy(sizePolicy)
        self.msg.setMaximumSize(QtCore.QSize(16777215, 50))
        self.msg.setObjectName("msg")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.msg)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.submit_btn = QtGui.QPushButton(channel_editor)
        self.submit_btn.setObjectName("submit_btn")
        self.verticalLayout_2.addWidget(self.submit_btn)
        self.add_row = QtGui.QAction(channel_editor)
        self.add_row.setObjectName("add_row")
        self.delete_row = QtGui.QAction(channel_editor)
        self.delete_row.setObjectName("delete_row")

        self.retranslateUi(channel_editor)
        QtCore.QMetaObject.connectSlotsByName(channel_editor)
        channel_editor.setTabOrder(self.channel_tbl, self.msg)
        channel_editor.setTabOrder(self.msg, self.submit_btn)

    def retranslateUi(self, channel_editor):
        channel_editor.setWindowTitle(QtGui.QApplication.translate("channel_editor", "Channel Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("channel_editor", "Channel Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("channel_editor", "Comment", None, QtGui.QApplication.UnicodeUTF8))
        self.submit_btn.setText(QtGui.QApplication.translate("channel_editor", "Save Changes", None, QtGui.QApplication.UnicodeUTF8))
        self.add_row.setText(QtGui.QApplication.translate("channel_editor", "Add Row", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_row.setText(QtGui.QApplication.translate("channel_editor", "Delete Row", None, QtGui.QApplication.UnicodeUTF8))

from publisher.gui.widgets import TSTitle
