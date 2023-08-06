# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/martinrusilowicz/work/apps/bio42/bio42_gui/forms/designer/frm_neo4j_wizard_designer.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def __init__(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(973, 603)
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
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TAB_MAIN = QtWidgets.QTabWidget(Dialog)
        self.TAB_MAIN.setDocumentMode(True)
        self.TAB_MAIN.setObjectName("TAB_MAIN")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_16 = QtWidgets.QLabel(self.tab)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_2.addWidget(self.label_16)
        self.label_15 = QtWidgets.QLabel(self.tab)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_2.addWidget(self.label_15)
        self.BTN_BEGIN = QtWidgets.QCommandLinkButton(self.tab)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/bio42/next.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_BEGIN.setIcon(icon)
        self.BTN_BEGIN.setIconSize(QtCore.QSize(32, 32))
        self.BTN_BEGIN.setAutoDefault(False)
        self.BTN_BEGIN.setObjectName("BTN_BEGIN")
        self.verticalLayout_2.addWidget(self.BTN_BEGIN)
        spacerItem = QtWidgets.QSpacerItem(20, 942, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.TAB_MAIN.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_3.addWidget(self.label_9)
        self.BTN_OPEN_DOWNLOAD = QtWidgets.QPushButton(self.tab_2)
        self.BTN_OPEN_DOWNLOAD.setStyleSheet("margin-left:32px;")
        self.BTN_OPEN_DOWNLOAD.setObjectName("BTN_OPEN_DOWNLOAD")
        self.verticalLayout_3.addWidget(self.BTN_OPEN_DOWNLOAD, 0, QtCore.Qt.AlignLeft)
        self.label_17 = QtWidgets.QLabel(self.tab_2)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_3.addWidget(self.label_17)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TXT_DOWNLOAD = QtWidgets.QLineEdit(self.tab_2)
        self.TXT_DOWNLOAD.setObjectName("TXT_DOWNLOAD")
        self.horizontalLayout.addWidget(self.TXT_DOWNLOAD)
        self.BTN_BROWSE_DOWNLOAD = QtWidgets.QPushButton(self.tab_2)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/bio42/browse.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_BROWSE_DOWNLOAD.setIcon(icon1)
        self.BTN_BROWSE_DOWNLOAD.setAutoDefault(False)
        self.BTN_BROWSE_DOWNLOAD.setObjectName("BTN_BROWSE_DOWNLOAD")
        self.horizontalLayout.addWidget(self.BTN_BROWSE_DOWNLOAD)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.BTN_VERIFY_DOWNLOAD = QtWidgets.QCommandLinkButton(self.tab_2)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/bio42/verify.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_VERIFY_DOWNLOAD.setIcon(icon2)
        self.BTN_VERIFY_DOWNLOAD.setIconSize(QtCore.QSize(32, 32))
        self.BTN_VERIFY_DOWNLOAD.setAutoDefault(False)
        self.BTN_VERIFY_DOWNLOAD.setObjectName("BTN_VERIFY_DOWNLOAD")
        self.verticalLayout_3.addWidget(self.BTN_VERIFY_DOWNLOAD)
        spacerItem1 = QtWidgets.QSpacerItem(20, 890, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.TAB_MAIN.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.tab_3)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.tab_3)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_4.addWidget(self.label_8)
        self.BTN_START = QtWidgets.QCommandLinkButton(self.tab_3)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/bio42/start.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_START.setIcon(icon3)
        self.BTN_START.setIconSize(QtCore.QSize(32, 32))
        self.BTN_START.setAutoDefault(False)
        self.BTN_START.setObjectName("BTN_START")
        self.verticalLayout_4.addWidget(self.BTN_START)
        spacerItem2 = QtWidgets.QSpacerItem(20, 419, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.TAB_MAIN.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_10 = QtWidgets.QLabel(self.tab_4)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_5.addWidget(self.label_10)
        self.label_11 = QtWidgets.QLabel(self.tab_4)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_5.addWidget(self.label_11)
        self.BTN_OPEN_LOGON = QtWidgets.QPushButton(self.tab_4)
        self.BTN_OPEN_LOGON.setObjectName("BTN_OPEN_LOGON")
        self.verticalLayout_5.addWidget(self.BTN_OPEN_LOGON, 0, QtCore.Qt.AlignLeft)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(8, 8, 8, 8)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.tab_4)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab_4)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.TXT_USERNAME = QtWidgets.QLineEdit(self.tab_4)
        self.TXT_USERNAME.setObjectName("TXT_USERNAME")
        self.gridLayout.addWidget(self.TXT_USERNAME, 0, 1, 1, 1)
        self.TXT_PASSWORD = QtWidgets.QLineEdit(self.tab_4)
        self.TXT_PASSWORD.setEchoMode(QtWidgets.QLineEdit.Password)
        self.TXT_PASSWORD.setObjectName("TXT_PASSWORD")
        self.gridLayout.addWidget(self.TXT_PASSWORD, 1, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout)
        self.label_18 = QtWidgets.QLabel(self.tab_4)
        self.label_18.setObjectName("label_18")
        self.verticalLayout_5.addWidget(self.label_18)
        self.BTN_VERIFY_LOGON = QtWidgets.QCommandLinkButton(self.tab_4)
        self.BTN_VERIFY_LOGON.setIcon(icon2)
        self.BTN_VERIFY_LOGON.setIconSize(QtCore.QSize(32, 32))
        self.BTN_VERIFY_LOGON.setAutoDefault(False)
        self.BTN_VERIFY_LOGON.setObjectName("BTN_VERIFY_LOGON")
        self.verticalLayout_5.addWidget(self.BTN_VERIFY_LOGON)
        spacerItem3 = QtWidgets.QSpacerItem(20, 191, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.TAB_MAIN.addTab(self.tab_4, "")
        self.TAB_COMPLETED = QtWidgets.QWidget()
        self.TAB_COMPLETED.setObjectName("TAB_COMPLETED")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.TAB_COMPLETED)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_12 = QtWidgets.QLabel(self.TAB_COMPLETED)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_6.addWidget(self.label_12)
        self.LBL_SAVE = QtWidgets.QLabel(self.TAB_COMPLETED)
        self.LBL_SAVE.setObjectName("LBL_SAVE")
        self.verticalLayout_6.addWidget(self.LBL_SAVE)
        self.BTN_SAVE = QtWidgets.QCommandLinkButton(self.TAB_COMPLETED)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/bio42/save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_SAVE.setIcon(icon4)
        self.BTN_SAVE.setIconSize(QtCore.QSize(32, 32))
        self.BTN_SAVE.setAutoDefault(False)
        self.BTN_SAVE.setObjectName("BTN_SAVE")
        self.verticalLayout_6.addWidget(self.BTN_SAVE)
        spacerItem4 = QtWidgets.QSpacerItem(20, 435, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem4)
        self.TAB_MAIN.addTab(self.TAB_COMPLETED, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_5)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_13 = QtWidgets.QLabel(self.tab_5)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_7.addWidget(self.label_13)
        self.LBL_SAVE_2 = QtWidgets.QLabel(self.tab_5)
        self.LBL_SAVE_2.setObjectName("LBL_SAVE_2")
        self.verticalLayout_7.addWidget(self.LBL_SAVE_2)
        self.BTN_OPTIMISE = QtWidgets.QCommandLinkButton(self.tab_5)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/bio42/optimise.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_OPTIMISE.setIcon(icon5)
        self.BTN_OPTIMISE.setIconSize(QtCore.QSize(32, 32))
        self.BTN_OPTIMISE.setAutoDefault(False)
        self.BTN_OPTIMISE.setObjectName("BTN_OPTIMISE")
        self.verticalLayout_7.addWidget(self.BTN_OPTIMISE)
        self.BTN_DONT_OPTIMISE = QtWidgets.QCommandLinkButton(self.tab_5)
        self.BTN_DONT_OPTIMISE.setIcon(icon)
        self.BTN_DONT_OPTIMISE.setIconSize(QtCore.QSize(32, 32))
        self.BTN_DONT_OPTIMISE.setAutoDefault(False)
        self.BTN_DONT_OPTIMISE.setObjectName("BTN_DONT_OPTIMISE")
        self.verticalLayout_7.addWidget(self.BTN_DONT_OPTIMISE)
        self.LBL_FINISHED = QtWidgets.QLabel(self.tab_5)
        self.LBL_FINISHED.setObjectName("LBL_FINISHED")
        self.verticalLayout_7.addWidget(self.LBL_FINISHED)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem5)
        self.TAB_MAIN.addTab(self.tab_5, "")
        self.verticalLayout.addWidget(self.TAB_MAIN)

        self.retranslateUi(Dialog)
        self.TAB_MAIN.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_16.setText(_translate("Dialog", "Introduction"))
        self.label_16.setProperty("style", _translate("Dialog", "heading"))
        self.label_15.setText(_translate("Dialog", "<html><head/><body><p>This wizard will guide you through configuring a Neo4j server.</p><p>If you prefer, you can close this dialogue and configure your control_server manually.</p><p>Click <span style=\" font-weight:600;\">begin</span> to begin.</p></body></html>"))
        self.label_15.setProperty("style", _translate("Dialog", "helpbox"))
        self.BTN_BEGIN.setText(_translate("Dialog", "Begin"))
        self.TAB_MAIN.setTabText(self.TAB_MAIN.indexOf(self.tab), _translate("Dialog", "Introduction"))
        self.label_6.setText(_translate("Dialog", "Step 1: Download Neo4j"))
        self.label_6.setProperty("style", _translate("Dialog", "heading"))
        self.label_9.setText(_translate("Dialog", "<html>\n"
"<body>\n"
"<p>Download the <b>Neo4j server</b> (<i>.zip</i>) from the link below.</p>\n"
"<p>Make sure to:\n"
"<ul>\n"
"<li>download the <b>server</b> version - <b>not</b> the desktop version</li>\n"
"<li><b>unzip</b> the downloaded package!</li>\n"
"</p></body></html>"))
        self.label_9.setProperty("style", _translate("Dialog", "helpbox"))
        self.BTN_OPEN_DOWNLOAD.setText(_translate("Dialog", "https://neo4j.com/download/"))
        self.BTN_OPEN_DOWNLOAD.setProperty("style", _translate("Dialog", "link"))
        self.label_17.setText(_translate("Dialog", "<html><head/><body><p>When you are done, tell me where you unzipped Neo4j to and click <span style=\" font-weight:600;\">verify </span>to continue the wizard.</p></body></html>"))
        self.label_17.setProperty("style", _translate("Dialog", "helpbox"))
        self.BTN_BROWSE_DOWNLOAD.setText(_translate("Dialog", "Browse"))
        self.BTN_VERIFY_DOWNLOAD.setText(_translate("Dialog", "Verify"))
        self.TAB_MAIN.setTabText(self.TAB_MAIN.indexOf(self.tab_2), _translate("Dialog", "Download"))
        self.label_7.setText(_translate("Dialog", "Step 2: Start Neo4j"))
        self.label_7.setProperty("style", _translate("Dialog", "heading"))
        self.label_8.setText(_translate("Dialog", "<html><head/><body><p>Click the <span style=\" font-weight:600;\">start</span> button to start the server and continue the wizard.</p><p>If you have already started the server yourself, clicking <span style=\" font-weight:600;\">start </span>will verify your server is running instead.</p></body></html>"))
        self.label_8.setProperty("style", _translate("Dialog", "helpbox"))
        self.BTN_START.setText(_translate("Dialog", "Start"))
        self.TAB_MAIN.setTabText(self.TAB_MAIN.indexOf(self.tab_3), _translate("Dialog", "Start"))
        self.label_10.setText(_translate("Dialog", "Step 3: Configure logon"))
        self.label_10.setProperty("style", _translate("Dialog", "heading"))
        self.label_11.setText(_translate("Dialog", "<html><head/><body><p>We should change the default password.<br/>The default credentials are:</p><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">user name</span>: <span style=\" font-family:\'Monaco\';\">neo4j</span></li><li style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">password</span>: <span style=\" font-family:\'Monaco\';\">neo4j</span></li></ul><p>Click the link and change your password.<br/>When you are done, come back here and let me know the details, if possible they\'ll be secured using your operating system\'s secure keyring.</p></body></html>"))
        self.label_11.setProperty("style", _translate("Dialog", "helpbox"))
        self.BTN_OPEN_LOGON.setText(_translate("Dialog", "http://127.0.0.1:7474"))
        self.BTN_OPEN_LOGON.setProperty("style", _translate("Dialog", "link"))
        self.label_4.setText(_translate("Dialog", "Password"))
        self.label_3.setText(_translate("Dialog", "Username"))
        self.TXT_USERNAME.setText(_translate("Dialog", "neo4j"))
        self.label_18.setText(_translate("Dialog", "<html><head/><body><p>When you are done, click <span style=\" font-weight:600;\">verify</span> to continue.</p></body></html>"))
        self.label_18.setProperty("style", _translate("Dialog", "helpbox"))
        self.BTN_VERIFY_LOGON.setText(_translate("Dialog", "Verify"))
        self.TAB_MAIN.setTabText(self.TAB_MAIN.indexOf(self.tab_4), _translate("Dialog", "Logon"))
        self.label_12.setText(_translate("Dialog", "Almost there..."))
        self.label_12.setProperty("style", _translate("Dialog", "heading"))
        self.LBL_SAVE.setText(_translate("Dialog", "<html><head/><body><p>Click <span style=\" font-weight:600;\">save</span> to save your connection information and continue.</p></body></html>"))
        self.LBL_SAVE.setProperty("style", _translate("Dialog", "helpbox"))
        self.BTN_SAVE.setText(_translate("Dialog", "Save"))
        self.TAB_MAIN.setTabText(self.TAB_MAIN.indexOf(self.TAB_COMPLETED), _translate("Dialog", "Save"))
        self.label_13.setText(_translate("Dialog", "Step 4: Optimise"))
        self.label_13.setProperty("style", _translate("Dialog", "heading"))
        self.LBL_SAVE_2.setText(_translate("Dialog", "<html><head/><body><p>Click <span style=\" font-weight:600;\">create indexes</span> to optimise your database and create the Bio42 schema.</p><p>This step is optional, an unoptimised database will still work and you can always perform this step later.</p></body></html>"))
        self.LBL_SAVE_2.setProperty("style", _translate("Dialog", "helpbox"))
        self.BTN_OPTIMISE.setText(_translate("Dialog", "Optimize"))
        self.BTN_DONT_OPTIMISE.setText(_translate("Dialog", "Don\'t optimise"))
        self.LBL_FINISHED.setText(_translate("Dialog", "<html><head/><body><p>All done, you may now close the wizard.</p></body></html>"))
        self.LBL_FINISHED.setProperty("style", _translate("Dialog", "helpbox"))
        self.TAB_MAIN.setTabText(self.TAB_MAIN.indexOf(self.tab_5), _translate("Dialog", "Optimize"))


