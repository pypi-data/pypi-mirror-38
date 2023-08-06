# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/martinrusilowicz/work/apps/bio42/bio42_gui/forms/designer/frm_query_browser_designer.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def __init__(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1281, 819)
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
"        WIDGET           | THEME             | APPEARANCE (GUIDE)            | USAGE (GUIDE)\n"
"        -----------------+-------------------+-------------------------------+-------------------------------\n"
"        QLabel           | heading           | border, big, bold             | section titles \n"
"        QLabel           | subheading        | border, big, bold             | section titles \n"
"        QTextEdit        | console           | monospaced, black background  | code, console output\n"
"        QPushButton      | completed         |                               |\n"
"        QPushButton      | cancel            | red                           | abort button\n"
"        QFrame           | header            | border                        | section titles\n"
"        QFrame           | contents          | white                         | with objects in\n"
"        QToolButton      | listbutton        | condensed                     | buttons in lists\n"
"        QToolButton      | help              | help icon                     | help buttons\n"
"        QLabel           | helpbox           | tooltip background            | help labels\n"
"        QLabel           | icon              | background suitable for image | label showing an icon\n"
"        QLabel           | warning           | yellow background, red text   | warning messages     \n"
"        QMdiArea         | empty             | darker                        | when MDI area has no windows\n"
"        QToolButton      | combo             | white                         | when button presents a selection menu\n"
"        QToolButton      | item              | white background, borderless  | button in a \"contents\" frame, like a list item\n"
"        QFrame           | helpbox           | yellow background             | frame contains help\n"
"        QFrame           | sidearea          | gray                          | behave like document-mode tab bar\n"
"        QAbstractButton  | expander          | double down / up arrow        | button expands current window frame           \n"
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
"\n"
"QFrame[style=\"sidearea\"]\n"
"{\n"
"    background: gray;\n"
"}\n"
"\n"
"QToolButton[style=\"sidearea\"]\n"
"{\n"
"    background: gray;\n"
"    border: 1px solid gray;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QToolButton[style=\"sidearea\"]:hover\n"
"{\n"
"    background: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(195, 195, 195, 255), stop:0.0985222 rgba(255, 255, 255, 255), stop:1 rgba(135, 135, 135, 255));\n"
"    border: 1px outset gray;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QToolButton[style=\"sidearea\"]:pressed\n"
"{\n"
"    background: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(195, 195, 195, 255), stop:0.0985222 rgba(99, 99, 99, 255), stop:1 rgba(135, 135, 135, 255));\n"
"    border: 1px inset gray;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QAbstractButton[style=\"expander\"]:checked\n"
"{\n"
"    qproperty-icon : url(:/intermake/expanddown.svg);\n"
"}\n"
"\n"
"QAbstractButton[style=\"expander\"]:!checked\n"
"{\n"
"    qproperty-icon : url(:/intermake/expandup.svg);\n"
"}\n"
"")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.SPLITTER_MAIN = QtWidgets.QSplitter(Dialog)
        self.SPLITTER_MAIN.setOrientation(QtCore.Qt.Horizontal)
        self.SPLITTER_MAIN.setHandleWidth(0)
        self.SPLITTER_MAIN.setChildrenCollapsible(False)
        self.SPLITTER_MAIN.setObjectName("SPLITTER_MAIN")
        self.PAN_MAIN_LEFT = QtWidgets.QWidget(self.SPLITTER_MAIN)
        self.PAN_MAIN_LEFT.setObjectName("PAN_MAIN_LEFT")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.PAN_MAIN_LEFT)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.PAGER_SET = QtWidgets.QStackedWidget(self.PAN_MAIN_LEFT)
        self.PAGER_SET.setObjectName("PAGER_SET")
        self.TWD_LEFTPage1 = QtWidgets.QWidget()
        self.TWD_LEFTPage1.setObjectName("TWD_LEFTPage1")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.TWD_LEFTPage1)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_3 = QtWidgets.QFrame(self.TWD_LEFTPage1)
        self.frame_3.setProperty("style", "sidearea")
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.BTN_SAVE = QtWidgets.QToolButton(self.frame_3)
        self.BTN_SAVE.setStyleSheet("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/bio42/save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_SAVE.setIcon(icon)
        self.BTN_SAVE.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.BTN_SAVE.setProperty("style", "sidearea")
        self.BTN_SAVE.setObjectName("BTN_SAVE")
        self.horizontalLayout_3.addWidget(self.BTN_SAVE)
        self.BTN_LOAD = QtWidgets.QToolButton(self.frame_3)
        self.BTN_LOAD.setStyleSheet("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/bio42/browse.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_LOAD.setIcon(icon1)
        self.BTN_LOAD.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.BTN_LOAD.setProperty("style", "sidearea")
        self.BTN_LOAD.setObjectName("BTN_LOAD")
        self.horizontalLayout_3.addWidget(self.BTN_LOAD)
        self.BTN_SHOW_ADVANCED = QtWidgets.QToolButton(self.frame_3)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/bio42/next.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_SHOW_ADVANCED.setIcon(icon2)
        self.BTN_SHOW_ADVANCED.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.BTN_SHOW_ADVANCED.setProperty("style", "sidearea")
        self.BTN_SHOW_ADVANCED.setObjectName("BTN_SHOW_ADVANCED")
        self.horizontalLayout_3.addWidget(self.BTN_SHOW_ADVANCED)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_6.addWidget(self.frame_3)
        self.splitter_2 = QtWidgets.QSplitter(self.TWD_LEFTPage1)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.PAN_CYPHER = QtWidgets.QWidget(self.splitter_2)
        self.PAN_CYPHER.setObjectName("PAN_CYPHER")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.PAN_CYPHER)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.PAN_CYPHER)
        self.label.setProperty("style", "heading")
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.CMB_QUERY = QtWidgets.QComboBox(self.PAN_CYPHER)
        self.CMB_QUERY.setObjectName("CMB_QUERY")
        self.verticalLayout_3.addWidget(self.CMB_QUERY)
        self.label_2 = QtWidgets.QLabel(self.PAN_CYPHER)
        self.label_2.setProperty("style", "heading")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.TXT_CYPHER = QtWidgets.QPlainTextEdit(self.PAN_CYPHER)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.TXT_CYPHER.setFont(font)
        self.TXT_CYPHER.setObjectName("TXT_CYPHER")
        self.verticalLayout_3.addWidget(self.TXT_CYPHER)
        self.FRA_PARAM_LOWER = QtWidgets.QWidget(self.splitter_2)
        self.FRA_PARAM_LOWER.setObjectName("FRA_PARAM_LOWER")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.FRA_PARAM_LOWER)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.FRA_PARAM_LOWER)
        self.label_3.setProperty("style", "heading")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.scrollArea = QtWidgets.QScrollArea(self.FRA_PARAM_LOWER)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.FRA_PARAMETERS = QtWidgets.QWidget()
        self.FRA_PARAMETERS.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.FRA_PARAMETERS.setObjectName("FRA_PARAMETERS")
        self.LAY_PARAMETERS = QtWidgets.QGridLayout(self.FRA_PARAMETERS)
        self.LAY_PARAMETERS.setContentsMargins(0, 0, 0, 0)
        self.LAY_PARAMETERS.setObjectName("LAY_PARAMETERS")
        self.scrollArea.setWidget(self.FRA_PARAMETERS)
        self.verticalLayout_4.addWidget(self.scrollArea)
        self.BTN_EXECUTE = QtWidgets.QPushButton(self.FRA_PARAM_LOWER)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/bio42/run_query.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_EXECUTE.setIcon(icon3)
        self.BTN_EXECUTE.setIconSize(QtCore.QSize(12, 12))
        self.BTN_EXECUTE.setObjectName("BTN_EXECUTE")
        self.verticalLayout_4.addWidget(self.BTN_EXECUTE, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_6.addWidget(self.splitter_2)
        self.PAGER_SET.addWidget(self.TWD_LEFTPage1)
        self.TWD_LEFTPage2 = QtWidgets.QWidget()
        self.TWD_LEFTPage2.setObjectName("TWD_LEFTPage2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.TWD_LEFTPage2)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.frame_4 = QtWidgets.QFrame(self.TWD_LEFTPage2)
        self.frame_4.setProperty("style", "sidearea")
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.BTN_BACK_TO_QUERY = QtWidgets.QToolButton(self.frame_4)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/bio42/verify.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_BACK_TO_QUERY.setIcon(icon4)
        self.BTN_BACK_TO_QUERY.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.BTN_BACK_TO_QUERY.setProperty("style", "sidearea")
        self.BTN_BACK_TO_QUERY.setObjectName("BTN_BACK_TO_QUERY")
        self.horizontalLayout_4.addWidget(self.BTN_BACK_TO_QUERY)
        spacerItem1 = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_7.addWidget(self.frame_4)
        self.widget_3 = QtWidgets.QWidget(self.TWD_LEFTPage2)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_9 = QtWidgets.QLabel(self.widget_3)
        self.label_9.setProperty("style", "heading")
        self.label_9.setObjectName("label_9")
        self.verticalLayout_9.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel(self.widget_3)
        self.label_10.setWordWrap(True)
        self.label_10.setProperty("style", "helpbox")
        self.label_10.setObjectName("label_10")
        self.verticalLayout_9.addWidget(self.label_10)
        self.CMB_SOURCE = QtWidgets.QComboBox(self.widget_3)
        self.CMB_SOURCE.setObjectName("CMB_SOURCE")
        self.verticalLayout_9.addWidget(self.CMB_SOURCE)
        self.label_5 = QtWidgets.QLabel(self.widget_3)
        self.label_5.setProperty("style", "heading")
        self.label_5.setObjectName("label_5")
        self.verticalLayout_9.addWidget(self.label_5)
        self.label_7 = QtWidgets.QLabel(self.widget_3)
        self.label_7.setWordWrap(True)
        self.label_7.setProperty("style", "helpbox")
        self.label_7.setObjectName("label_7")
        self.verticalLayout_9.addWidget(self.label_7)
        self.CHK_ENABLE_BROWSER = QtWidgets.QCheckBox(self.widget_3)
        self.CHK_ENABLE_BROWSER.setObjectName("CHK_ENABLE_BROWSER")
        self.verticalLayout_9.addWidget(self.CHK_ENABLE_BROWSER)
        self.label_11 = QtWidgets.QLabel(self.widget_3)
        self.label_11.setWordWrap(True)
        self.label_11.setProperty("style", "helpbox")
        self.label_11.setObjectName("label_11")
        self.verticalLayout_9.addWidget(self.label_11)
        self.CHK_B42_SCRIPTS = QtWidgets.QCheckBox(self.widget_3)
        self.CHK_B42_SCRIPTS.setObjectName("CHK_B42_SCRIPTS")
        self.verticalLayout_9.addWidget(self.CHK_B42_SCRIPTS)
        self.BTN_CUSTOM_LIBRARIES = QtWidgets.QPushButton(self.widget_3)
        self.BTN_CUSTOM_LIBRARIES.setObjectName("BTN_CUSTOM_LIBRARIES")
        self.verticalLayout_9.addWidget(self.BTN_CUSTOM_LIBRARIES, 0, QtCore.Qt.AlignLeft)
        self.label_6 = QtWidgets.QLabel(self.widget_3)
        self.label_6.setProperty("style", "heading")
        self.label_6.setObjectName("label_6")
        self.verticalLayout_9.addWidget(self.label_6)
        self.label_8 = QtWidgets.QLabel(self.widget_3)
        self.label_8.setWordWrap(True)
        self.label_8.setProperty("style", "helpbox")
        self.label_8.setObjectName("label_8")
        self.verticalLayout_9.addWidget(self.label_8)
        self.CMB_DESTINATION = QtWidgets.QComboBox(self.widget_3)
        self.CMB_DESTINATION.setObjectName("CMB_DESTINATION")
        self.verticalLayout_9.addWidget(self.CMB_DESTINATION)
        spacerItem2 = QtWidgets.QSpacerItem(20, 569, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem2)
        self.verticalLayout_7.addWidget(self.widget_3)
        self.PAGER_SET.addWidget(self.TWD_LEFTPage2)
        self.verticalLayout.addWidget(self.PAGER_SET)
        self.PAN_MAIN_RIGHT = QtWidgets.QWidget(self.SPLITTER_MAIN)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PAN_MAIN_RIGHT.sizePolicy().hasHeightForWidth())
        self.PAN_MAIN_RIGHT.setSizePolicy(sizePolicy)
        self.PAN_MAIN_RIGHT.setObjectName("PAN_MAIN_RIGHT")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.PAN_MAIN_RIGHT)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.SPL_BROWSER_TREE = QtWidgets.QSplitter(self.PAN_MAIN_RIGHT)
        self.SPL_BROWSER_TREE.setOrientation(QtCore.Qt.Horizontal)
        self.SPL_BROWSER_TREE.setHandleWidth(0)
        self.SPL_BROWSER_TREE.setChildrenCollapsible(False)
        self.SPL_BROWSER_TREE.setObjectName("SPL_BROWSER_TREE")
        self.FRA_BROWSER_HOLDER_BASE = QtWidgets.QWidget(self.SPL_BROWSER_TREE)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FRA_BROWSER_HOLDER_BASE.sizePolicy().hasHeightForWidth())
        self.FRA_BROWSER_HOLDER_BASE.setSizePolicy(sizePolicy)
        self.FRA_BROWSER_HOLDER_BASE.setStyleSheet("")
        self.FRA_BROWSER_HOLDER_BASE.setObjectName("FRA_BROWSER_HOLDER_BASE")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.FRA_BROWSER_HOLDER_BASE)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.frame = QtWidgets.QFrame(self.FRA_BROWSER_HOLDER_BASE)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setProperty("style", "sidearea")
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.BTN_TREE = QtWidgets.QToolButton(self.frame)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/intermake/expandup.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_TREE.setIcon(icon5)
        self.BTN_TREE.setCheckable(True)
        self.BTN_TREE.setProperty("style", "sidearea")
        self.BTN_TREE.setObjectName("BTN_TREE")
        self.horizontalLayout.addWidget(self.BTN_TREE)
        self.BTN_SEND_TO = QtWidgets.QToolButton(self.frame)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/bio42/send.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_SEND_TO.setIcon(icon6)
        self.BTN_SEND_TO.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.BTN_SEND_TO.setProperty("style", "sidearea")
        self.BTN_SEND_TO.setObjectName("BTN_SEND_TO")
        self.horizontalLayout.addWidget(self.BTN_SEND_TO)
        self.BTN_EXPORT_AS = QtWidgets.QToolButton(self.frame)
        self.BTN_EXPORT_AS.setStyleSheet("")
        self.BTN_EXPORT_AS.setIcon(icon)
        self.BTN_EXPORT_AS.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.BTN_EXPORT_AS.setProperty("style", "sidearea")
        self.BTN_EXPORT_AS.setObjectName("BTN_EXPORT_AS")
        self.horizontalLayout.addWidget(self.BTN_EXPORT_AS)
        self.BTN_SYSTEM_BROWSER = QtWidgets.QToolButton(self.frame)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/bio42/browser.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_SYSTEM_BROWSER.setIcon(icon7)
        self.BTN_SYSTEM_BROWSER.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.BTN_SYSTEM_BROWSER.setProperty("style", "sidearea")
        self.BTN_SYSTEM_BROWSER.setObjectName("BTN_SYSTEM_BROWSER")
        self.horizontalLayout.addWidget(self.BTN_SYSTEM_BROWSER)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_8.addWidget(self.frame)
        self.FRA_BROWSER_HOLDER = QtWidgets.QWidget(self.FRA_BROWSER_HOLDER_BASE)
        self.FRA_BROWSER_HOLDER.setStyleSheet("background: cornflowerblue;")
        self.FRA_BROWSER_HOLDER.setObjectName("FRA_BROWSER_HOLDER")
        self.GRID_BROWSER_HOLDER = QtWidgets.QGridLayout(self.FRA_BROWSER_HOLDER)
        self.GRID_BROWSER_HOLDER.setContentsMargins(0, 0, 0, 0)
        self.GRID_BROWSER_HOLDER.setSpacing(0)
        self.GRID_BROWSER_HOLDER.setObjectName("GRID_BROWSER_HOLDER")
        self.verticalLayout_8.addWidget(self.FRA_BROWSER_HOLDER)
        self.FRA_TREE_HOLDER_BASE = QtWidgets.QWidget(self.SPL_BROWSER_TREE)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FRA_TREE_HOLDER_BASE.sizePolicy().hasHeightForWidth())
        self.FRA_TREE_HOLDER_BASE.setSizePolicy(sizePolicy)
        self.FRA_TREE_HOLDER_BASE.setStyleSheet("")
        self.FRA_TREE_HOLDER_BASE.setObjectName("FRA_TREE_HOLDER_BASE")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.FRA_TREE_HOLDER_BASE)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.FRA_TREE_BAR = QtWidgets.QFrame(self.FRA_TREE_HOLDER_BASE)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FRA_TREE_BAR.sizePolicy().hasHeightForWidth())
        self.FRA_TREE_BAR.setSizePolicy(sizePolicy)
        self.FRA_TREE_BAR.setProperty("style", "sidearea")
        self.FRA_TREE_BAR.setObjectName("FRA_TREE_BAR")
        self.LAY_TREE_BAR = QtWidgets.QHBoxLayout(self.FRA_TREE_BAR)
        self.LAY_TREE_BAR.setContentsMargins(0, 0, 0, 0)
        self.LAY_TREE_BAR.setSpacing(0)
        self.LAY_TREE_BAR.setObjectName("LAY_TREE_BAR")
        self.BTN_LOCAL_BROWSER = QtWidgets.QToolButton(self.FRA_TREE_BAR)
        self.BTN_LOCAL_BROWSER.setIcon(icon5)
        self.BTN_LOCAL_BROWSER.setCheckable(True)
        self.BTN_LOCAL_BROWSER.setProperty("style", "sidearea")
        self.BTN_LOCAL_BROWSER.setObjectName("BTN_LOCAL_BROWSER")
        self.LAY_TREE_BAR.addWidget(self.BTN_LOCAL_BROWSER)
        self.verticalLayout_5.addWidget(self.FRA_TREE_BAR)
        self.FRA_TREE_HOLDER = QtWidgets.QWidget(self.FRA_TREE_HOLDER_BASE)
        self.FRA_TREE_HOLDER.setStyleSheet("background: violet;")
        self.FRA_TREE_HOLDER.setObjectName("FRA_TREE_HOLDER")
        self.verticalLayout_5.addWidget(self.FRA_TREE_HOLDER)
        self.verticalLayout_2.addWidget(self.SPL_BROWSER_TREE)
        self.gridLayout.addWidget(self.SPLITTER_MAIN, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.PAGER_SET.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.BTN_SAVE.setText(_translate("Dialog", "Save"))
        self.BTN_LOAD.setText(_translate("Dialog", "Load"))
        self.BTN_SHOW_ADVANCED.setText(_translate("Dialog", "Advanced"))
        self.label.setText(_translate("Dialog", "Query"))
        self.label_2.setText(_translate("Dialog", "Cypher"))
        self.label_3.setText(_translate("Dialog", "Parameters"))
        self.BTN_EXECUTE.setText(_translate("Dialog", "Execute"))
        self.BTN_BACK_TO_QUERY.setText(_translate("Dialog", "Accept"))
        self.label_9.setText(_translate("Dialog", "Data source"))
        self.label_10.setText(_translate("Dialog", "The data has to come from somewhere!"))
        self.label_5.setText(_translate("Dialog", "Enable"))
        self.label_7.setText(_translate("Dialog", "Turn the inbuilt browser off if it\'s causing problems or you\'d like to use your own browser."))
        self.CHK_ENABLE_BROWSER.setText(_translate("Dialog", "Enable browser (requires restart)"))
        self.label_11.setText(_translate("Dialog", "Add or remove script libraries. Note that loading extra libraries can take time."))
        self.CHK_B42_SCRIPTS.setText(_translate("Dialog", "Enable bio42_scripts"))
        self.BTN_CUSTOM_LIBRARIES.setText(_translate("Dialog", "Manage custom libraries"))
        self.label_6.setText(_translate("Dialog", "Send output to"))
        self.label_8.setText(_translate("Dialog", "This interface directs the output at the GUI by default, but you can send it somewhere else instead."))
        self.BTN_SEND_TO.setText(_translate("Dialog", "Send"))
        self.BTN_EXPORT_AS.setText(_translate("Dialog", "Export"))
        self.BTN_SYSTEM_BROWSER.setText(_translate("Dialog", "System"))


