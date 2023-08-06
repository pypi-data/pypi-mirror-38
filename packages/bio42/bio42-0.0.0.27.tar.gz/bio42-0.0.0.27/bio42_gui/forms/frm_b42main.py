from typing import List

import intermake_qt.utilities.interfaces
from mhelper import SwitchError
from mhelper_qt import exceptToGui, exqtSlot
from PyQt5.QtCore import QCoreApplication, Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QMessageBox

import intermake
import bio42
import neocommand
import intermake_qt

from bio42_gui.forms.designer import frm_b42main_designer
from bio42_gui.forms.frm_b42_base import AbstractB42SubWindow
from bio42_gui.forms.frm_neo4j_wizard import FrmNeo4jWizard


class FrmB42Main( QMainWindow, intermake_qt.utilities.interfaces.IGuiMainWindow ):
    """
    Main window
    """
    
    
    @exceptToGui()
    def __init__( self, controller ) -> None:
        """
        CONSTRUCTOR
        """
        from bio42_gui import B42GuiController
        
        # QT stuff
        QCoreApplication.setAttribute( Qt.AA_DontUseNativeMenuBar )
        QMainWindow.__init__( self )
        self.ui = frm_b42main_designer.Ui_MainWindow()
        self.ui.setupUi( self )
        self.setWindowTitle( "B42" )
        self.ui.PAGER_MAIN.setCurrentIndex( 0 )
        
        self.child_windows: List[AbstractB42SubWindow] = []
        self.ui.LBL_INTRO.linkActivated[str].connect( self.on_lbl_intro_link_activated )
        
        self.timer = QTimer( self )
        self.timer.timeout.connect( self.flash )
        self.flash_stage = 0
        self.flash_count = 0
        self.flash_button = ()
        self.flash_page = None
        
        self.controller: B42GuiController = controller
    
    
    def flash( self ):
        DELAY_1 = 5
        DELAY_2 = 5
        DELAY_3 = 10
        DELAY_4 = 10
        
        if self.flash_stage == 1:
            # Setup
            self.flash_count = DELAY_1
            self.flash_stage += 1
        elif self.flash_stage == 2:
            # Delay
            self.flash_count -= 1
            
            if self.flash_count == 0:
                self.ui.PAGER_MAIN.setCurrentWidget( self.flash_page )
                self.flash_count = DELAY_2
                self.flash_stage += 1
        elif self.flash_stage == 3:
            # Delay
            self.flash_count -= 1
            
            if self.flash_count == 0:
                self.flash_count = DELAY_3
                self.flash_stage += 1
        elif self.flash_stage == 4:
            # Flash button
            self.flash_count -= 1
            
            if self.flash_count == 0:
                self.flash_count = DELAY_4
                self.flash_stage += 1
                ss = ""
            elif self.flash_count % 2 == 0:
                ss = "border-bottom: 2px solid yellow;"
            else:
                ss = "border-bottom: 2px solid black;"
            
            for button in self.flash_button:
                button.setStyleSheet( ss )
        elif self.flash_stage == 5:
            self.flash_count -= 1
            
            if self.flash_count == 0:
                self.timer.stop()
                self.ui.PAGER_MAIN.setCurrentIndex( 0 )
                self.on_lbl_intro_link_activated( "" )
    
    
    def on_lbl_intro_link_activated( self, _ ):
        from bio42_gui.forms.frm_getting_started import FrmGettingStarted as f
        v = f.request( self )
        
        if v == f.O_CREATE_DATABASE:
            self.highlight( self.ui.PAG_ENDPOINTS, self.ui.BTN_ENDPOINT_TRANSFER )
        elif v == f.O_CREATE_PARCEL:
            self.highlight( self.ui.PAG_ENDPOINTS, self.ui.BTN_ENDPOINT_PACKAGE )
        elif v == f.O_EXPLORE_DATA:
            self.highlight( self.ui.PAG_QUERY, self.ui.BTN_QUERY_INBUILT )
        elif v == f.O_OPEN_CONNECTION:
            self.highlight( self.ui.PAG_ENDPOINTS, self.ui.BTN_WIZARD, self.ui.BTN_ENDPOINT_DATABASE )
        elif v == f.O_PUT_DATA_IN:
            self.highlight( self.ui.PAG_IMPORT, self.ui.BTN_IMPORT_TAXONOMY, self.ui.BTN_IMPORT_ANNOTATIONS, self.ui.BTN_IMPORT_CSV, self.ui.BTN_IMPORT_ONTOLOGY, self.ui.BTN_IMPORT_SEQUENCES, self.ui.BTN_IMPORT_SIMILARITIES )
        elif v is not None:
            raise SwitchError( "f.request", v )
    
    
    def highlight( self, page, *button ):
        self.flash_page = page
        self.flash_button = button
        self.flash_stage = 1
        self.timer.start( 100 )
    
    
    def command_completed( self, result: intermake.Result ) -> None:
        for window in self.child_windows:
            window.on_plugin_completed( result )
    
    
    def return_to_console( self ) -> bool:
        pass
    
    
    @exqtSlot()
    def on_BTN_ENDPOINT_DATABASE_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__request( neocommand.open_database )
    
    
    @exqtSlot()
    def on_BTN_ENDPOINT_PACKAGE_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__request( neocommand.open_parcel )
    
    
    @exqtSlot()
    def on_BTN_ENDPOINT_DISCONNECT_clicked( self ) -> None:
        """
        Signal handler:
        """
        from .frm_endpoint_list import FrmEndpointList
        FrmEndpointList.request( self )
    
    
    @exqtSlot()
    def on_BTN_IMPORT_SEQUENCES_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__request( bio42.import_sequences )
    
    
    @exqtSlot()
    def on_BTN_IMPORT_SIMILARITIES_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__request( bio42.import_blast )
    
    
    @exqtSlot()
    def on_BTN_IMPORT_ANNOTATIONS_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__request( bio42.import_annotations )
    
    
    @exqtSlot()
    def on_BTN_IMPORT_ONTOLOGY_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__request( bio42.import_go )
    
    
    @exqtSlot()
    def on_BTN_IMPORT_TAXONOMY_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__request( bio42.import_taxonomy )
    
    
    @exqtSlot()
    def on_BTN_IMPORT_CSV_clicked( self ) -> None:
        """
        Signal handler:
        """
        from bio42_gui.forms.frm_import_csv import FrmImportCsv
        FrmImportCsv.request( self )
    
    
    @exqtSlot()
    def on_BTN_QUERY_INBUILT_clicked( self ) -> None:
        """
        Signal handler:
        """
        from bio42_gui.forms.frm_query_browser import FrmQueryBrowser
        FrmQueryBrowser.request( self )
    
    
    @exqtSlot()
    def on_BTN_SETTINGS_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__request( intermake.commands.configure )
    
    
    @exqtSlot()
    def on_BTN_OPTIMISE_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__request( neocommand.apply_schema )
    
    
    @exqtSlot()
    def on_BTN_EXPORT_GEXF_clicked( self ) -> None:
        """
        Signal handler:
        """
        QMessageBox.information( self,
                                 "GEXF-Export",
                                 "GEXF currently can't be exported directly from the main screen. Please create a `file - gexf` endpoint and `transfer` to it for now." )
    
    
    @exqtSlot()
    def on_BTN_EXPORT_CSV_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__request( neocommand.export_edgelist )
    
    
    @exqtSlot()
    def on_BTN_EXPORT_HTML_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__request( neocommand.export_js )
    
    
    @exqtSlot()
    def on_BTN_QUERY_PICKLE_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__request( neocommand.export_binary )
    
    
    @exqtSlot()
    def on_BTN_WIZARD_clicked( self ) -> None:
        """
        Signal handler:
        """
        FrmNeo4jWizard.request( self )
    
    
    @exqtSlot()
    def on_BTN_DB_STATUS_clicked( self ) -> None:
        """
        Signal handler:
        """
        from bio42_gui.forms.frm_database import FrmDatabase
        FrmDatabase.request( self )
    
    
    @exqtSlot()
    def on_BTN_ENDPOINT_MGRAPH_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__request( neocommand.open_file )
    
    
    @exqtSlot()
    def on_BTN_ENDPOINT_TRANSFER_clicked( self ) -> None:
        """
        Signal handler:
        """
        from bio42_gui.forms.frm_transfer import FrmTransfer
        FrmTransfer.request( self )
    
    
    @exqtSlot()
    def on_BTN_INTERMAKE_clicked( self ) -> None:
        """
        Signal handler:
        """
        intermake_qt.show_basic_window( self )
    
    
    @exqtSlot()
    def on_BTN_HELP_clicked( self ) -> None:
        """
        Signal handler:
        """
        pass
    
    
    def __request( self, command ):
        return self.controller.acquire( command, window = self, confirm = True ).run()
