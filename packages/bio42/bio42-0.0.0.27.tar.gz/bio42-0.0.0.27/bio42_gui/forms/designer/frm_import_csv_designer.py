# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/martinrusilowicz/work/apps/bio42/bio42_gui/forms/designer/frm_import_csv_designer.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def __init__(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(880, 599)
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
"        QLabel        | helpbox           | tooltip background            | help labels\n"
"        QLabel        | icon              | background suitable for image | label showing an icon\n"
"        QLabel        | warning           | yellow background, red text   | warning messages     \n"
"        QMdiArea      | empty             | darker                        | when MDI area has no windows\n"
"        ﻿QToolButton   | combo             | white                         | when button presents a selection menu\n"
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
"}\n"
"")
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.BTN_BACK = QtWidgets.QPushButton(Dialog)
        self.BTN_BACK.setObjectName("BTN_BACK")
        self.horizontalLayout_4.addWidget(self.BTN_BACK)
        self.BTN_NEXT = QtWidgets.QPushButton(Dialog)
        self.BTN_NEXT.setObjectName("BTN_NEXT")
        self.horizontalLayout_4.addWidget(self.BTN_NEXT)
        self.BTN_OK = QtWidgets.QPushButton(Dialog)
        self.BTN_OK.setObjectName("BTN_OK")
        self.horizontalLayout_4.addWidget(self.BTN_OK)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.STACK_MAIN = QtWidgets.QStackedWidget(Dialog)
        self.STACK_MAIN.setObjectName("STACK_MAIN")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page_4)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_19 = QtWidgets.QLabel(self.page_4)
        self.label_19.setObjectName("label_19")
        self.verticalLayout_3.addWidget(self.label_19)
        self.label_20 = QtWidgets.QLabel(self.page_4)
        self.label_20.setObjectName("label_20")
        self.verticalLayout_3.addWidget(self.label_20)
        self.CMB_DESTINATION = QtWidgets.QComboBox(self.page_4)
        self.CMB_DESTINATION.setObjectName("CMB_DESTINATION")
        self.verticalLayout_3.addWidget(self.CMB_DESTINATION)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.BTN_DESTINATION = QtWidgets.QPushButton(self.page_4)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/bio42/parcel.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_DESTINATION.setIcon(icon)
        self.BTN_DESTINATION.setObjectName("BTN_DESTINATION")
        self.horizontalLayout_3.addWidget(self.BTN_DESTINATION)
        self.BTN_REFRESH_DESTINATION = QtWidgets.QPushButton(self.page_4)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/bio42/refresh.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_REFRESH_DESTINATION.setIcon(icon1)
        self.BTN_REFRESH_DESTINATION.setObjectName("BTN_REFRESH_DESTINATION")
        self.horizontalLayout_3.addWidget(self.BTN_REFRESH_DESTINATION)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.STACK_MAIN.addWidget(self.page_4)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_13 = QtWidgets.QLabel(self.page)
        self.label_13.setObjectName("label_13")
        self.verticalLayout.addWidget(self.label_13)
        self.label_16 = QtWidgets.QLabel(self.page)
        self.label_16.setObjectName("label_16")
        self.verticalLayout.addWidget(self.label_16)
        self.label = QtWidgets.QLabel(self.page)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CMB_FILENAME = QtWidgets.QComboBox(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CMB_FILENAME.sizePolicy().hasHeightForWidth())
        self.CMB_FILENAME.setSizePolicy(sizePolicy)
        self.CMB_FILENAME.setEditable(True)
        self.CMB_FILENAME.setObjectName("CMB_FILENAME")
        self.horizontalLayout.addWidget(self.CMB_FILENAME)
        self.BTN_FILENAME = QtWidgets.QPushButton(self.page)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/bio42/browse.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_FILENAME.setIcon(icon2)
        self.BTN_FILENAME.setObjectName("BTN_FILENAME")
        self.horizontalLayout.addWidget(self.BTN_FILENAME)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_8 = QtWidgets.QLabel(self.page)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.gridFrame = QtWidgets.QFrame(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridFrame.sizePolicy().hasHeightForWidth())
        self.gridFrame.setSizePolicy(sizePolicy)
        self.gridFrame.setObjectName("gridFrame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridFrame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.CMB_DELIMITER = QtWidgets.QComboBox(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CMB_DELIMITER.sizePolicy().hasHeightForWidth())
        self.CMB_DELIMITER.setSizePolicy(sizePolicy)
        self.CMB_DELIMITER.setObjectName("CMB_DELIMITER")
        self.gridLayout_3.addWidget(self.CMB_DELIMITER, 0, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 0, 0, 1, 1)
        self.CMB_ARRAY_DELIMITER = QtWidgets.QComboBox(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CMB_ARRAY_DELIMITER.sizePolicy().hasHeightForWidth())
        self.CMB_ARRAY_DELIMITER.setSizePolicy(sizePolicy)
        self.CMB_ARRAY_DELIMITER.setObjectName("CMB_ARRAY_DELIMITER")
        self.gridLayout_3.addWidget(self.CMB_ARRAY_DELIMITER, 1, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setObjectName("label_21")
        self.gridLayout_3.addWidget(self.label_21, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.gridFrame)
        self.CHK_F_HEADERS = QtWidgets.QCheckBox(self.page)
        self.CHK_F_HEADERS.setObjectName("CHK_F_HEADERS")
        self.verticalLayout.addWidget(self.CHK_F_HEADERS)
        self.CHK_F_TYPE_INFO = QtWidgets.QCheckBox(self.page)
        self.CHK_F_TYPE_INFO.setObjectName("CHK_F_TYPE_INFO")
        self.verticalLayout.addWidget(self.CHK_F_TYPE_INFO)
        self.CHK_F_FILENAME_LABELS = QtWidgets.QCheckBox(self.page)
        self.CHK_F_FILENAME_LABELS.setObjectName("CHK_F_FILENAME_LABELS")
        self.verticalLayout.addWidget(self.CHK_F_FILENAME_LABELS)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.STACK_MAIN.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.page_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_17 = QtWidgets.QLabel(self.page_2)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_2.addWidget(self.label_17)
        self.LST_ENTITIES = QtWidgets.QTreeWidget(self.page_2)
        self.LST_ENTITIES.setObjectName("LST_ENTITIES")
        self.LST_ENTITIES.headerItem().setText(0, "1")
        self.verticalLayout_2.addWidget(self.LST_ENTITIES)
        self.FRA_ADD_EDGES = QtWidgets.QFrame(self.page_2)
        self.FRA_ADD_EDGES.setObjectName("FRA_ADD_EDGES")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.FRA_ADD_EDGES)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.LBL_ADD_ENTITY_2 = QtWidgets.QLabel(self.FRA_ADD_EDGES)
        self.LBL_ADD_ENTITY_2.setObjectName("LBL_ADD_ENTITY_2")
        self.gridLayout_5.addWidget(self.LBL_ADD_ENTITY_2, 0, 0, 1, 5)
        self.LBL_ENT_DEST = QtWidgets.QLabel(self.FRA_ADD_EDGES)
        self.LBL_ENT_DEST.setAlignment(QtCore.Qt.AlignCenter)
        self.LBL_ENT_DEST.setObjectName("LBL_ENT_DEST")
        self.gridLayout_5.addWidget(self.LBL_ENT_DEST, 2, 3, 1, 1)
        self.CMB_EDGE_SOURCE = QtWidgets.QComboBox(self.FRA_ADD_EDGES)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CMB_EDGE_SOURCE.sizePolicy().hasHeightForWidth())
        self.CMB_EDGE_SOURCE.setSizePolicy(sizePolicy)
        self.CMB_EDGE_SOURCE.setEditable(True)
        self.CMB_EDGE_SOURCE.setObjectName("CMB_EDGE_SOURCE")
        self.gridLayout_5.addWidget(self.CMB_EDGE_SOURCE, 3, 1, 1, 1)
        self.CMB_EDGE_LABEL = QtWidgets.QComboBox(self.FRA_ADD_EDGES)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CMB_EDGE_LABEL.sizePolicy().hasHeightForWidth())
        self.CMB_EDGE_LABEL.setSizePolicy(sizePolicy)
        self.CMB_EDGE_LABEL.setEditable(True)
        self.CMB_EDGE_LABEL.setObjectName("CMB_EDGE_LABEL")
        self.gridLayout_5.addWidget(self.CMB_EDGE_LABEL, 3, 2, 1, 1)
        self.CMB_EDGE_DEST = QtWidgets.QComboBox(self.FRA_ADD_EDGES)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CMB_EDGE_DEST.sizePolicy().hasHeightForWidth())
        self.CMB_EDGE_DEST.setSizePolicy(sizePolicy)
        self.CMB_EDGE_DEST.setEditable(True)
        self.CMB_EDGE_DEST.setObjectName("CMB_EDGE_DEST")
        self.gridLayout_5.addWidget(self.CMB_EDGE_DEST, 3, 3, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.RAD_EDGE = QtWidgets.QRadioButton(self.FRA_ADD_EDGES)
        self.RAD_EDGE.setObjectName("RAD_EDGE")
        self.horizontalLayout_2.addWidget(self.RAD_EDGE)
        self.RAD_NODE = QtWidgets.QRadioButton(self.FRA_ADD_EDGES)
        self.RAD_NODE.setObjectName("RAD_NODE")
        self.horizontalLayout_2.addWidget(self.RAD_NODE)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.BTN_ADD_EDGE = QtWidgets.QPushButton(self.FRA_ADD_EDGES)
        self.BTN_ADD_EDGE.setObjectName("BTN_ADD_EDGE")
        self.horizontalLayout_2.addWidget(self.BTN_ADD_EDGE)
        self.BTN_REMOVE_ENTITY = QtWidgets.QPushButton(self.FRA_ADD_EDGES)
        self.BTN_REMOVE_ENTITY.setObjectName("BTN_REMOVE_ENTITY")
        self.horizontalLayout_2.addWidget(self.BTN_REMOVE_ENTITY)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 1, 1, 1, 4)
        self.LBL_ENT_LABEL = QtWidgets.QLabel(self.FRA_ADD_EDGES)
        self.LBL_ENT_LABEL.setAlignment(QtCore.Qt.AlignCenter)
        self.LBL_ENT_LABEL.setObjectName("LBL_ENT_LABEL")
        self.gridLayout_5.addWidget(self.LBL_ENT_LABEL, 2, 2, 1, 1)
        self.LBL_ENT_SOURCE = QtWidgets.QLabel(self.FRA_ADD_EDGES)
        self.LBL_ENT_SOURCE.setAlignment(QtCore.Qt.AlignCenter)
        self.LBL_ENT_SOURCE.setObjectName("LBL_ENT_SOURCE")
        self.gridLayout_5.addWidget(self.LBL_ENT_SOURCE, 2, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.FRA_ADD_EDGES)
        self.STACK_MAIN.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.page_3)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7)
        self.label_18 = QtWidgets.QLabel(self.page_3)
        self.label_18.setObjectName("label_18")
        self.verticalLayout_4.addWidget(self.label_18)
        self.TVW_FIELDS = QtWidgets.QTreeWidget(self.page_3)
        self.TVW_FIELDS.setRootIsDecorated(False)
        self.TVW_FIELDS.setItemsExpandable(False)
        self.TVW_FIELDS.setObjectName("TVW_FIELDS")
        self.TVW_FIELDS.headerItem().setText(0, "1")
        self.verticalLayout_4.addWidget(self.TVW_FIELDS)
        self.label_15 = QtWidgets.QLabel(self.page_3)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_4.addWidget(self.label_15)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.LBL_E_TYPE = QtWidgets.QLabel(self.page_3)
        self.LBL_E_TYPE.setObjectName("LBL_E_TYPE")
        self.gridLayout.addWidget(self.LBL_E_TYPE, 0, 1, 1, 1)
        self.CMB_E_TYPE = QtWidgets.QComboBox(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CMB_E_TYPE.sizePolicy().hasHeightForWidth())
        self.CMB_E_TYPE.setSizePolicy(sizePolicy)
        self.CMB_E_TYPE.setObjectName("CMB_E_TYPE")
        self.gridLayout.addWidget(self.CMB_E_TYPE, 1, 1, 1, 1)
        self.CMB_ENTITY = QtWidgets.QComboBox(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CMB_ENTITY.sizePolicy().hasHeightForWidth())
        self.CMB_ENTITY.setSizePolicy(sizePolicy)
        self.CMB_ENTITY.setObjectName("CMB_ENTITY")
        self.gridLayout.addWidget(self.CMB_ENTITY, 1, 0, 1, 1)
        self.LBL_E_NAME = QtWidgets.QLabel(self.page_3)
        self.LBL_E_NAME.setObjectName("LBL_E_NAME")
        self.gridLayout.addWidget(self.LBL_E_NAME, 0, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.page_3)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.CMB_E_NAME = QtWidgets.QComboBox(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CMB_E_NAME.sizePolicy().hasHeightForWidth())
        self.CMB_E_NAME.setSizePolicy(sizePolicy)
        self.CMB_E_NAME.setEditable(True)
        self.CMB_E_NAME.setObjectName("CMB_E_NAME")
        self.gridLayout.addWidget(self.CMB_E_NAME, 1, 2, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.STACK_MAIN.addWidget(self.page_3)
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_11 = QtWidgets.QLabel(self.page_5)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_5.addWidget(self.label_11)
        self.LBL_REVIEW = QtWidgets.QTextBrowser(self.page_5)
        self.LBL_REVIEW.setObjectName("LBL_REVIEW")
        self.verticalLayout_5.addWidget(self.LBL_REVIEW)
        self.STACK_MAIN.addWidget(self.page_5)
        self.gridLayout_2.addWidget(self.STACK_MAIN, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.STACK_MAIN.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.BTN_BACK.setText(_translate("Dialog", "Back"))
        self.BTN_NEXT.setText(_translate("Dialog", "Next"))
        self.BTN_OK.setText(_translate("Dialog", "OK"))
        self.label_19.setText(_translate("Dialog", "Destination"))
        self.label_19.setProperty("style", _translate("Dialog", "title"))
        self.label_20.setText(_translate("Dialog", "Specify where to send your data to.\n"
"For large datasets you are recommended to send your data to a Parcel first."))
        self.label_20.setProperty("style", _translate("Dialog", "helpbox"))
        self.CMB_DESTINATION.setToolTip(_translate("Dialog", "Specify the name of your parcel.\n"
"Click the button to create a new parcel."))
        self.BTN_DESTINATION.setToolTip(_translate("Dialog", "Click to create a new parcel."))
        self.BTN_DESTINATION.setText(_translate("Dialog", "New parcel"))
        self.BTN_REFRESH_DESTINATION.setToolTip(_translate("Dialog", "Click to create a new parcel."))
        self.BTN_REFRESH_DESTINATION.setText(_translate("Dialog", "Refresh"))
        self.label_13.setText(_translate("Dialog", "File"))
        self.label_13.setProperty("style", _translate("Dialog", "title"))
        self.label_16.setText(_translate("Dialog", "Specify the file you wish to import. This can be any CSV or TSV file, with or without headers and with or without Neo4j type information."))
        self.label_16.setProperty("style", _translate("Dialog", "helpbox"))
        self.label.setText(_translate("Dialog", "Name"))
        self.CMB_FILENAME.setToolTip(_translate("Dialog", "Specify the file from which you wish to import data."))
        self.BTN_FILENAME.setToolTip(_translate("Dialog", "Click to browse your disk."))
        self.BTN_FILENAME.setText(_translate("Dialog", "Browse"))
        self.label_8.setText(_translate("Dialog", "Type"))
        self.CMB_DELIMITER.setToolTip(_translate("Dialog", "<html><body>\n"
"Specify the file delimiter. Typically <tt>,</tt> or <tt>TAB</tt>.\n"
"</body></html>"))
        self.label_10.setText(_translate("Dialog", "Delimiter"))
        self.CMB_ARRAY_DELIMITER.setToolTip(_translate("Dialog", "<html><body>\n"
"If your file contains arrays, specify the delimiter here.\n"
"Typically <tt>;</tt>.\n"
"This is only used if you specify fields of type array (<tt>[]</tt>).\n"
"</body></html>"))
        self.label_21.setText(_translate("Dialog", "Array delimiter"))
        self.CHK_F_HEADERS.setToolTip(_translate("Dialog", "Select this option if your file contains headers.\n"
"\n"
"File headers can be any arbitrary information that you wish to use to specify the columns.\n"
"If your file contains headers, you must select this option or the first row will be treated as data."))
        self.CHK_F_HEADERS.setText(_translate("Dialog", "File contains headers"))
        self.CHK_F_TYPE_INFO.setToolTip(_translate("Dialog", "<html><body>\n"
"<p>\n"
"Select this option if your file\'s headers contain type information.\n"
"</p>\n"
"<p>\n"
"If they don\'t, you will be prompted to specify the datatypes manually.\n"
"</p>\n"
"\n"
"<p>\n"
"Type information should be of the form: <tt>entity.property:type</tt>\n"
"<ul>\n"
"<li><tt>entity</tt> - the entity, specify either a label, such as <tt>Sequence</tt> or <tt>LIKE</tt>, or the fully decorated name, such as <tt>(Sequence)</tt> or <tt>(Sequence)-[LIKE]->(Sequence)</tt></li>\n"
"<li><tt>property</tt> - the name of the property. You can also use the special values: <tt>UID</tt> <tt>START_ID(label)</tt> and <tt>END_ID(label)</tt>.\n"
"<li><tt>type</tt> - the type of the property, such as <tt>int</tt> or <tt>str[]</tt>.\n"
"</ul>\n"
"</p>\n"
"</body></html>"))
        self.CHK_F_TYPE_INFO.setText(_translate("Dialog", "Headers contain type information"))
        self.CHK_F_FILENAME_LABELS.setToolTip(_translate("Dialog", "<html><body>\n"
"<p>\n"
"Select this option if your filename contains entity labels.\n"
"</p><p>\n"
"If it doesn\'t, you will be prompted to specify the entities manually.\n"
"</p>\n"
"<p>\n"
"Valid filenames are of the form <tt>Node-label.extension</tt> or <tt>Edge-label-label-label.extension</tt>.\n"
"</p>\n"
"<p>\n"
"For example <tt>Node-Sequence.csv</tt> or <tt>Edge-Sequence-LIKE-Sequence.csv</tt>.\n"
"</p>\n"
"</body></html>"))
        self.CHK_F_FILENAME_LABELS.setText(_translate("Dialog", "File name contains labels"))
        self.label_2.setText(_translate("Dialog", "Entities"))
        self.label_2.setProperty("style", _translate("Dialog", "title"))
        self.label_17.setText(_translate("Dialog", "Specify the labels of the nodes and edges that you will be importing.\n"
"If your filename is formatted appropriately this section will have already been filled out. Please review before continuing."))
        self.label_17.setProperty("style", _translate("Dialog", "helpbox"))
        self.LBL_ADD_ENTITY_2.setText(_translate("Dialog", "Configure"))
        self.LBL_ADD_ENTITY_2.setProperty("style", _translate("Dialog", "heading"))
        self.LBL_ENT_DEST.setText(_translate("Dialog", "Destination"))
        self.RAD_EDGE.setText(_translate("Dialog", "Edge"))
        self.RAD_NODE.setText(_translate("Dialog", "Node"))
        self.BTN_ADD_EDGE.setText(_translate("Dialog", "Duplicate"))
        self.BTN_REMOVE_ENTITY.setText(_translate("Dialog", "Remove"))
        self.LBL_ENT_LABEL.setText(_translate("Dialog", "Label"))
        self.LBL_ENT_SOURCE.setText(_translate("Dialog", "Source"))
        self.label_7.setText(_translate("Dialog", "Columns"))
        self.label_7.setProperty("style", _translate("Dialog", "title"))
        self.label_18.setText(_translate("Dialog", "Specify the fields of your CSV file.\n"
"If your CSV file already contains Neo4j type information this section will have already been filled out. Please review before continuing."))
        self.label_18.setProperty("style", _translate("Dialog", "helpbox"))
        self.label_15.setText(_translate("Dialog", "Configure"))
        self.label_15.setProperty("style", _translate("Dialog", "heading"))
        self.LBL_E_TYPE.setText(_translate("Dialog", "Type"))
        self.LBL_E_NAME.setText(_translate("Dialog", "Name"))
        self.label_9.setText(_translate("Dialog", "Entity"))
        self.label_11.setText(_translate("Dialog", "Review"))
        self.label_11.setProperty("style", _translate("Dialog", "title"))


