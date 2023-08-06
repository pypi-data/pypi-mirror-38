# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/martinrusilowicz/work/apps/bio42/bio42_gui/forms/designer/frm_getting_started_designer.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def __init__(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(706, 501)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.BTN_CREATE_PARCEL = QtWidgets.QCommandLinkButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/bio42/parcel.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_CREATE_PARCEL.setIcon(icon)
        self.BTN_CREATE_PARCEL.setIconSize(QtCore.QSize(48, 48))
        self.BTN_CREATE_PARCEL.setObjectName("BTN_CREATE_PARCEL")
        self.verticalLayout_2.addWidget(self.BTN_CREATE_PARCEL)
        self.BTN_PUT_DATA_IN = QtWidgets.QCommandLinkButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/bio42/taxonomy.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_PUT_DATA_IN.setIcon(icon1)
        self.BTN_PUT_DATA_IN.setIconSize(QtCore.QSize(48, 48))
        self.BTN_PUT_DATA_IN.setObjectName("BTN_PUT_DATA_IN")
        self.verticalLayout_2.addWidget(self.BTN_PUT_DATA_IN)
        self.BTN_OPEN_CONNECTION = QtWidgets.QCommandLinkButton(Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/bio42/wizard.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_OPEN_CONNECTION.setIcon(icon2)
        self.BTN_OPEN_CONNECTION.setIconSize(QtCore.QSize(48, 48))
        self.BTN_OPEN_CONNECTION.setObjectName("BTN_OPEN_CONNECTION")
        self.verticalLayout_2.addWidget(self.BTN_OPEN_CONNECTION)
        self.BTN_CREATE_DATABASE = QtWidgets.QCommandLinkButton(Dialog)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/bio42/send.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_CREATE_DATABASE.setIcon(icon3)
        self.BTN_CREATE_DATABASE.setIconSize(QtCore.QSize(48, 48))
        self.BTN_CREATE_DATABASE.setObjectName("BTN_CREATE_DATABASE")
        self.verticalLayout_2.addWidget(self.BTN_CREATE_DATABASE)
        self.BTN_EXPLORE_DATA = QtWidgets.QCommandLinkButton(Dialog)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/bio42/script.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_EXPLORE_DATA.setIcon(icon4)
        self.BTN_EXPLORE_DATA.setIconSize(QtCore.QSize(48, 48))
        self.BTN_EXPLORE_DATA.setObjectName("BTN_EXPLORE_DATA")
        self.verticalLayout_2.addWidget(self.BTN_EXPLORE_DATA)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 92, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Getting started"))
        self.label.setText(_translate("Dialog", "Things to do"))
        self.label.setProperty("style", _translate("Dialog", "title"))
        self.BTN_CREATE_PARCEL.setText(_translate("Dialog", "Create a parcel to put my data in"))
        self.BTN_PUT_DATA_IN.setText(_translate("Dialog", "Put some data in my parcel"))
        self.BTN_OPEN_CONNECTION.setText(_translate("Dialog", "Open a connection to Neo4j"))
        self.BTN_CREATE_DATABASE.setText(_translate("Dialog", "Create my database"))
        self.BTN_EXPLORE_DATA.setText(_translate("Dialog", "Explore my data"))


