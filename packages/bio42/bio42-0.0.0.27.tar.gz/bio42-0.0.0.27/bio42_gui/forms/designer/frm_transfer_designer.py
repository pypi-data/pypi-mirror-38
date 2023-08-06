# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/martinrusilowicz/work/apps/bio42/bio42_gui/forms/designer/frm_transfer_designer.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def __init__(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(697, 487)
        Dialog.setStyleSheet("/**\n"
"    PURPOSE:\n"
"        This is the default style-sheet used by all Intermake dialogues.\n"
"        It needs to be processed by css_processing.py before it can be used. \n"
"        It can be retrieved in processed form by the `intermake_gui.default_style_sheet()` function.\n"
"\n"
"    USAGE:    \n"
"        You can replace this stylesheet with your own.\n"
"        If you blank the contents of this stylesheet, the OSs default controls will be used.\n"
"        If you delete this stylesheet, the program will crash.\n"
"        \n"
"    EXTENSIONS:\n"
"        Normally not permitted in Qt, the following values are read through Intermake.\n"
"            * #DEFINE X Y                    - replaces all text `X` with `Y`\n"
"            * #WHEN X Y Z                    - only executes the following lines if the current\n"
"                                               section is any of `X` `Y` or `Z`.\n"
"                                               The section is specified when the user selects a\n"
"                                               stylesheet.\n"
"            * `QApplication.style`           - one of the Qt styles\n"
"            * `QApplication.small_icon_size` - the menu icon size, permitted only if `style` is set\n"
"            * `QMdiArea.background`          - colour of the Mdi area\n"
"\n"
"    DETAILS:\n"
"        Follow standard Qt stylesheet guidelines.\n"
"        \n"
"        The `:root` section defines constants that may be used elsewhere. These constants are\n"
"        substituted during the the processing stage and the `:root` section is removed.\n"
"        \n"
"        Intermake controls may have a string property named \"theme\" assigned to to certain widgets.\n"
"        This specifies that a unique appearance for the widget is intended:\n"
"        \n"
"        WIDGET        | THEME             | APPEARANCE (GUIDE)            | USAGE (GUIDE)\n"
"        --------------+-------------------+-------------------------------+-------------------------------\n"
"        QLabel        | heading           | border, big, bold             | section titles \n"
"        QLabel        | subheading        | border, big, bold             | section titles \n"
"        QTextEdit     | console           | monospaced, black background  | code, console output\n"
"        QPushButton   | completed         |                               |\n"
"        QPushButton   | cancel            | red                           | abort button\n"
"        QFrame        | header            | border                        | section titles\n"
"        QFrame        | contents          | white                         | with objects in\n"
"        QToolButton   | listbutton        | condensed                     | buttons in lists\n"
"        QToolButton   | help              | help icon                     | help buttons\n"
"        QLabel        | helpbox           | tooltip background            | help labels\n"
"        QLabel        | icon              | background suitable for image | label showing an icon\n"
"        QLabel        | warning           | yellow background, red text   | warning messages     \n"
"        QMdiArea      | empty             | darker                        | when MDI area has no windows\n"
"        QToolButton   | combo             | white                         | when button presents a selection menu\n"
"        QToolButton   | item              | white background, borderless  | button in a \"contents\" frame, like a list item\n"
"        QFrame        | helpbox           | yellow background             | frame contains help\n"
"*/\n"
"\n"
"\n"
"\n"
"QMdiArea\n"
"{\n"
"    background : #E0E0E0;\n"
"}\n"
"\n"
"\n"
"QToolButton[style=\"listbutton\"]\n"
"{\n"
"    background   : #40C0FF;\n"
"    border-style : outset;\n"
"    border-width : 2px;\n"
"    border-color : transparent;\n"
"}\n"
"\n"
"QToolButton[style=\"listbutton\"]::hover\n"
"{\n"
"    background   : #B0D5E8;\n"
"    border-color : blue;\n"
"}\n"
"\n"
"QToolButton[style=\"listbutton\"]::pressed\n"
"{\n"
"    background   : #0040C0;\n"
"    border-style : inset;\n"
"}\n"
"\n"
"QLabel[style=\"icon\"]\n"
"{\n"
"    background    : #EEEEEE;\n"
"    border-radius : 8px;\n"
"}\n"
"\n"
"QFrame[style=\"title\"]\n"
"{\n"
"    margin-top     : 16px;\n"
"    margin-bottom  : 4px;\n"
"    margin-left    : 0px;\n"
"    margin-right   : 0px;\n"
"    border-radius  : 0px;\n"
"    border-bottom  : 2px solid silver;\n"
"    border-left    : none;\n"
"    border-right   : none;\n"
"    border-top     : none;\n"
"    padding-top    : 2px;\n"
"    padding-bottom : 2px;\n"
"    padding-left   : -4px;\n"
"    padding-right  : 0px;\n"
"    color          : black;\n"
"    font-size      : 18px;\n"
"}\n"
"\n"
"QLabel[style=\"title\"], QFrame[style=\"title\"]\n"
"{\n"
"    background    : #EEEEEE;\n"
"    border-radius : 4px;\n"
"    margin        : 2px;\n"
"    padding       : 2px;\n"
"    color         : black;\n"
"    font-size     : 18px;\n"
"}\n"
"\n"
"QLabel[style=\"title-embeded\"]\n"
"{\n"
"    background : #EEEEEE;\n"
"    color      : black;\n"
"    font-size  : 18px;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"QLabel[style=\"helpbox\"]\n"
"{\n"
"    background    : transparent;\n"
"    color         : steelblue;\n"
"    padding       : 2px;\n"
"    border-radius : 4px;\n"
"}\n"
"\n"
"QLabel[style=\"subheading\"]\n"
"{\n"
"    font-weight: bold;\n"
"    font-style: italic;\n"
"}\n"
"\n"
"QLabel[style=\"heading\"], QPushButton[style=\"heading\"]\n"
"{\n"
"    font-weight: bold;\n"
"    border-bottom  : 1px solid #404040;\n"
"    border-left    : none;\n"
"    border-right   : none;\n"
"    border-top     : none;\n"
"    color: #404040;\n"
"}\n"
"\n"
"\n"
"QTextEdit[style=\"console\"]\n"
"{\n"
"    font-family: \"Consolas\", monospace;\n"
"    background : black;\n"
"    color      : white;\n"
"}\n"
"\n"
"QTextEdit[style=\"monospaced\"]\n"
"{\n"
"    font-family: \"Consolas\", monospace;\n"
"}\n"
"\n"
"QPushButton[style=\"completed\"]\n"
"{\n"
"    background    : #00C080;\n"
"    border-color  : #00C080; \n"
"}\n"
"\n"
"QPushButton[style=\"cancel\"]\n"
"{\n"
"    background    : #C00000;\n"
"    color         : white;\n"
"    padding       : 8px;\n"
"    border-color  : white;\n"
"    border-width  : 1px;\n"
"    border-radius : 8px;\n"
"}\n"
"\n"
"QMdiArea[style=\"empty\"]\n"
"{\n"
"    background : #E0E0E0;\n"
"}\n"
"\n"
"QLabel[style=\"warning\"]\n"
"{\n"
"    background       : #FFFFD0;\n"
"    padding          : 8px;\n"
"    border-radius    : 8px;\n"
"    image            : url(\":/intermake/warning.svg\");\n"
"    image-position   : left;\n"
"    qproperty-indent : 24;\n"
"}\n"
"\n"
"QLabel[style=\"warning_no_icon\"]\n"
"{\n"
"    background       : #FFFF80;\n"
"    color            : #800000;          \n"
"    padding          : 8px;\n"
"    border-radius    : 8px;\n"
"}\n"
"\n"
"QToolButton[style=\"dropdown\"]\n"
"{\n"
"    qproperty-toolButtonStyle : ToolButtonTextBesideIcon;\n"
"    qproperty-icon            : url(:/intermake/dropdown.svg);\n"
"}\n"
"\n"
"QToolButton[style=\"refresh\"]\n"
"{\n"
"    qproperty-toolButtonStyle : ToolButtonTextBesideIcon;\n"
"    qproperty-icon            : url(:/intermake/refresh.svg);\n"
"}\n"
"\n"
"\n"
"QToolButton[style=\"combo\"]\n"
"{\n"
"    background: white;\n"
"}\n"
"\n"
"QFrame[style=\"contents\"]\n"
"{\n"
"    background: white;\n"
"    border: 1px inset silver;\n"
"}\n"
"\n"
"QToolButton[style=\"item\"]\n"
"{\n"
"    background: white;\n"
"    border: 1px solid white;\n"
"    color: black;\n"
"}\n"
"\n"
"QToolButton[style=\"item\"]:hover\n"
"{\n"
"    color: blue;\n"
"    text-decoration: underline;\n"
"    border: 1px dotted #8080FF;\n"
"}\n"
"\n"
"QToolButton[style=\"item\"]:pressed\n"
"{\n"
"    background: #B0D5E8;\n"
"}\n"
"\n"
"QToolButton[style=\"help\"]\n"
"{\n"
"    border: 1px solid transparent;\n"
"    background: transparent;\n"
"    qproperty-icon            : url(:/intermake/help.svg);\n"
"}\n"
"\n"
"QToolButton[style=\"help\"]:hover\n"
"{\n"
"    border: 1px outset silver;\n"
"}\n"
"\n"
"QToolButton[style=\"help\"]:pressed\n"
"{\n"
"    border: 1px inset silver;\n"
"}\n"
"\n"
"QPushButton[style=\"link\"]\n"
"{\n"
"    background: transparent;\n"
"    border: none;\n"
"    color: blue;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QPushButton[style=\"link\"]:hover\n"
"{\n"
"    color: blue;\n"
"    text-decoration: underline;\n"
"}\n"
"\n"
"QPushButton[style=\"link\"]:pressed\n"
"{\n"
"    color: red;\n"
"    text-decoration: underline;\n"
"    border: 1px solid blue;\n"
"}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LBL_TITLE = QtWidgets.QLabel(Dialog)
        self.LBL_TITLE.setObjectName("LBL_TITLE")
        self.verticalLayout.addWidget(self.LBL_TITLE)
        self.LBL_SOURCE = QtWidgets.QLabel(Dialog)
        self.LBL_SOURCE.setObjectName("LBL_SOURCE")
        self.verticalLayout.addWidget(self.LBL_SOURCE)
        self.CMB_SOURCE = QtWidgets.QComboBox(Dialog)
        self.CMB_SOURCE.setObjectName("CMB_SOURCE")
        self.verticalLayout.addWidget(self.CMB_SOURCE)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(32, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.horizontalFrame = QtWidgets.QFrame(Dialog)
        self.horizontalFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.horizontalFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalFrame.setProperty("style", "helpbox")
        self.horizontalFrame.setObjectName("horizontalFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LBL_SOURCE_5 = QtWidgets.QLabel(self.horizontalFrame)
        self.LBL_SOURCE_5.setMinimumSize(QtCore.QSize(24, 24))
        self.LBL_SOURCE_5.setMaximumSize(QtCore.QSize(24, 24))
        self.LBL_SOURCE_5.setText("")
        self.LBL_SOURCE_5.setPixmap(QtGui.QPixmap(":/bio42/information.svg"))
        self.LBL_SOURCE_5.setScaledContents(True)
        self.LBL_SOURCE_5.setObjectName("LBL_SOURCE_5")
        self.horizontalLayout.addWidget(self.LBL_SOURCE_5)
        self.LBL_SRC_INFO = QtWidgets.QLabel(self.horizontalFrame)
        self.LBL_SRC_INFO.setProperty("style", "helpbox")
        self.LBL_SRC_INFO.setObjectName("LBL_SRC_INFO")
        self.horizontalLayout.addWidget(self.LBL_SRC_INFO)
        self.horizontalLayout_4.addWidget(self.horizontalFrame)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.LBL_DEST = QtWidgets.QLabel(Dialog)
        self.LBL_DEST.setObjectName("LBL_DEST")
        self.verticalLayout.addWidget(self.LBL_DEST)
        self.CMB_DEST = QtWidgets.QComboBox(Dialog)
        self.CMB_DEST.setObjectName("CMB_DEST")
        self.verticalLayout.addWidget(self.CMB_DEST)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem1 = QtWidgets.QSpacerItem(32, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.horizontalFrame_2 = QtWidgets.QFrame(Dialog)
        self.horizontalFrame_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.horizontalFrame_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalFrame_2.setProperty("style", "helpbox")
        self.horizontalFrame_2.setObjectName("horizontalFrame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalFrame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LBL_SOURCE_6 = QtWidgets.QLabel(self.horizontalFrame_2)
        self.LBL_SOURCE_6.setMinimumSize(QtCore.QSize(24, 24))
        self.LBL_SOURCE_6.setMaximumSize(QtCore.QSize(24, 24))
        self.LBL_SOURCE_6.setText("")
        self.LBL_SOURCE_6.setPixmap(QtGui.QPixmap(":/bio42/information.svg"))
        self.LBL_SOURCE_6.setScaledContents(True)
        self.LBL_SOURCE_6.setObjectName("LBL_SOURCE_6")
        self.horizontalLayout_2.addWidget(self.LBL_SOURCE_6)
        self.LBL_DEST_INFO = QtWidgets.QLabel(self.horizontalFrame_2)
        self.LBL_DEST_INFO.setProperty("style", "helpbox")
        self.LBL_DEST_INFO.setObjectName("LBL_DEST_INFO")
        self.horizontalLayout_2.addWidget(self.LBL_DEST_INFO)
        self.horizontalLayout_5.addWidget(self.horizontalFrame_2)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.LBL_PROTO = QtWidgets.QLabel(Dialog)
        self.LBL_PROTO.setObjectName("LBL_PROTO")
        self.verticalLayout.addWidget(self.LBL_PROTO)
        self.CBM_PROTO = QtWidgets.QComboBox(Dialog)
        self.CBM_PROTO.setObjectName("CBM_PROTO")
        self.verticalLayout.addWidget(self.CBM_PROTO)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem2 = QtWidgets.QSpacerItem(32, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.horizontalFrame_3 = QtWidgets.QFrame(Dialog)
        self.horizontalFrame_3.setFrameShape(QtWidgets.QFrame.Panel)
        self.horizontalFrame_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalFrame_3.setObjectName("horizontalFrame_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalFrame_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.LBL_SOURCE_7 = QtWidgets.QLabel(self.horizontalFrame_3)
        self.LBL_SOURCE_7.setMinimumSize(QtCore.QSize(24, 24))
        self.LBL_SOURCE_7.setMaximumSize(QtCore.QSize(24, 24))
        self.LBL_SOURCE_7.setText("")
        self.LBL_SOURCE_7.setPixmap(QtGui.QPixmap(":/bio42/information.svg"))
        self.LBL_SOURCE_7.setScaledContents(True)
        self.LBL_SOURCE_7.setObjectName("LBL_SOURCE_7")
        self.horizontalLayout_3.addWidget(self.LBL_SOURCE_7)
        self.LBL_PROTO_INFO = QtWidgets.QLabel(self.horizontalFrame_3)
        self.LBL_PROTO_INFO.setProperty("style", "helpbox")
        self.LBL_PROTO_INFO.setObjectName("LBL_PROTO_INFO")
        self.horizontalLayout_3.addWidget(self.LBL_PROTO_INFO)
        self.horizontalLayout_6.addWidget(self.horizontalFrame_3)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.BTNBOX_MAIN = QtWidgets.QDialogButtonBox(Dialog)
        self.BTNBOX_MAIN.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.BTNBOX_MAIN.setObjectName("BTNBOX_MAIN")
        self.verticalLayout.addWidget(self.BTNBOX_MAIN)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.LBL_TITLE.setToolTip(_translate("Dialog", "Select where to acquire the data from. Click the help button for more information about the selected source."))
        self.LBL_TITLE.setText(_translate("Dialog", "Graph transfer"))
        self.LBL_TITLE.setProperty("style", _translate("Dialog", "title"))
        self.LBL_SOURCE.setToolTip(_translate("Dialog", "Select where to acquire the data from. Click the help button for more information about the selected source."))
        self.LBL_SOURCE.setText(_translate("Dialog", "Source"))
        self.LBL_SOURCE.setProperty("style", _translate("Dialog", "heading"))
        self.CMB_SOURCE.setToolTip(_translate("Dialog", "Select where to acquire the data from. Click the help button for more information about the selected source."))
        self.LBL_SOURCE_5.setToolTip(_translate("Dialog", "Select where to acquire the data from. Click the help button for more information about the selected source."))
        self.LBL_SRC_INFO.setToolTip(_translate("Dialog", "Select where to acquire the data from. Click the help button for more information about the selected source."))
        self.LBL_SRC_INFO.setText(_translate("Dialog", "Information"))
        self.LBL_DEST.setToolTip(_translate("Dialog", "Select where to send the data to. Click the help button for more information about the selected destination."))
        self.LBL_DEST.setText(_translate("Dialog", "Destination"))
        self.LBL_DEST.setProperty("style", _translate("Dialog", "heading"))
        self.CMB_DEST.setToolTip(_translate("Dialog", "Select where to send the data to. Click the help button for more information about the selected destination."))
        self.LBL_SOURCE_6.setToolTip(_translate("Dialog", "Select where to acquire the data from. Click the help button for more information about the selected source."))
        self.LBL_DEST_INFO.setToolTip(_translate("Dialog", "Select where to acquire the data from. Click the help button for more information about the selected source."))
        self.LBL_DEST_INFO.setText(_translate("Dialog", "Information"))
        self.LBL_PROTO.setToolTip(_translate("Dialog", "Select how to transfer the data. Click the help button for more information about the selected protocol."))
        self.LBL_PROTO.setText(_translate("Dialog", "Protocol"))
        self.LBL_PROTO.setProperty("style", _translate("Dialog", "heading"))
        self.CBM_PROTO.setToolTip(_translate("Dialog", "Select how to transfer the data. Click the help button for more information about the selected protocol."))
        self.horizontalFrame_3.setProperty("style", _translate("Dialog", "helpbox"))
        self.LBL_SOURCE_7.setToolTip(_translate("Dialog", "Select where to acquire the data from. Click the help button for more information about the selected source."))
        self.LBL_PROTO_INFO.setToolTip(_translate("Dialog", "Select where to acquire the data from. Click the help button for more information about the selected source."))
        self.LBL_PROTO_INFO.setText(_translate("Dialog", "Information"))


