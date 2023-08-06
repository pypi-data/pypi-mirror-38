# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/martinrusilowicz/work/apps/bio42/bio42_gui/forms/designer/frm_endpoint_list_designer.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def __init__(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(976, 690)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TVW_MAIN = QtWidgets.QTreeWidget(Dialog)
        self.TVW_MAIN.setObjectName("TVW_MAIN")
        self.TVW_MAIN.headerItem().setText(0, "1")
        self.horizontalLayout.addWidget(self.TVW_MAIN)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.BTN_ADD = QtWidgets.QCommandLinkButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/bio42/add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_ADD.setIcon(icon)
        self.BTN_ADD.setIconSize(QtCore.QSize(32, 32))
        self.BTN_ADD.setObjectName("BTN_ADD")
        self.verticalLayout.addWidget(self.BTN_ADD)
        self.BTN_REMOVE = QtWidgets.QCommandLinkButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/bio42/disconnect.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_REMOVE.setIcon(icon1)
        self.BTN_REMOVE.setIconSize(QtCore.QSize(32, 32))
        self.BTN_REMOVE.setObjectName("BTN_REMOVE")
        self.verticalLayout.addWidget(self.BTN_REMOVE)
        self.BTN_DELETE = QtWidgets.QCommandLinkButton(Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/bio42/delete.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_DELETE.setIcon(icon2)
        self.BTN_DELETE.setIconSize(QtCore.QSize(32, 32))
        self.BTN_DELETE.setObjectName("BTN_DELETE")
        self.verticalLayout.addWidget(self.BTN_DELETE)
        self.BTN_REFRESH = QtWidgets.QCommandLinkButton(Dialog)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/bio42/refresh.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_REFRESH.setIcon(icon3)
        self.BTN_REFRESH.setIconSize(QtCore.QSize(32, 32))
        self.BTN_REFRESH.setObjectName("BTN_REFRESH")
        self.verticalLayout.addWidget(self.BTN_REFRESH)
        self.BTN_OK = QtWidgets.QCommandLinkButton(Dialog)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/bio42/verify.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_OK.setIcon(icon4)
        self.BTN_OK.setIconSize(QtCore.QSize(32, 32))
        self.BTN_OK.setObjectName("BTN_OK")
        self.verticalLayout.addWidget(self.BTN_OK)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.BTN_ADD.setText(_translate("Dialog", "Add"))
        self.BTN_ADD.setDescription(_translate("Dialog", "Add a new endpoint"))
        self.BTN_REMOVE.setText(_translate("Dialog", "Remove"))
        self.BTN_REMOVE.setDescription(_translate("Dialog", "Remove the selected endpoint (but not from disk)"))
        self.BTN_DELETE.setText(_translate("Dialog", "Delete"))
        self.BTN_DELETE.setDescription(_translate("Dialog", "Delete the selected endpoint\'s contents from disk"))
        self.BTN_REFRESH.setText(_translate("Dialog", "Refresh"))
        self.BTN_REFRESH.setDescription(_translate("Dialog", "Refresh the information"))
        self.BTN_OK.setText(_translate("Dialog", "OK"))
        self.BTN_OK.setDescription(_translate("Dialog", "Close this window"))


