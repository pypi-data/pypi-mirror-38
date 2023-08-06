from mhelper import io_helper
from mhelper_qt import exqtSlot, qt_gui_helper
from PyQt5.QtWidgets import QMessageBox, QWidget
from bio42 import Application

import os.path
import webbrowser
import intermake
import neocommand

from bio42_gui.forms.designer import frm_neo4j_wizard_designer
from bio42_gui.forms.frm_b42_base import AbstractB42SubWindow


class FrmNeo4jWizard( AbstractB42SubWindow ):
    """
    This wizard-style dialogue guides the user through installing and connecting to Neo4j.
    
    Uses the `open_database` command.
    """
    
    def __init__( self, parent: QWidget ):
        """
        CONSTRUCTOR
        """
        super().__init__( parent )
        self.ui = frm_neo4j_wizard_designer.Ui_Dialog( self )
        self.setWindowTitle( "Wizard" )
        self.ui.LBL_FINISHED.setVisible( False )
        self.locked_index = 0
        self.ui.TAB_MAIN.setCurrentIndex( 0 )
        self.ui.TAB_MAIN.currentChanged[int].connect( self.__on_TAB_MAIN_currentChanged )
        self.ep = None
    
    
    def __on_TAB_MAIN_currentChanged( self, index ):
        if index != self.locked_index:
            self.ui.TAB_MAIN.setCurrentIndex( self.locked_index )
    
    
    def next_page( self ):
        self.locked_index += 1
        self.ui.TAB_MAIN.setCurrentIndex( self.locked_index )
    
    
    def alert( self, text, det = None ):
        msg = QMessageBox( self )
        msg.setText( "Cannot continue" )
        msg.setInformativeText( text )
        msg.setDetailedText( det )
        msg.setIcon( QMessageBox.Critical )
        msg.exec_()
    
    
    @exqtSlot()
    def on_BTN_BEGIN_clicked( self ) -> None:
        """
        Signal handler:
        """
        for ep in neocommand.get_core().endpoint_manager.user_endpoints:
            if ep.name == "neo4j":
                self.alert( "You already have an endpoint named 'neo4j'. Please close the wizard and «disconnect» that before continuing." )
                return
        
        self.next_page()
    
    
    @exqtSlot()
    def on_BTN_OPEN_DOWNLOAD_clicked( self ) -> None:
        """
        Signal handler:
        """
        webbrowser.open( self.ui.BTN_OPEN_DOWNLOAD.text() )
    
    
    @exqtSlot()
    def on_BTN_BROWSE_DOWNLOAD_clicked( self ) -> None:
        """
        Signal handler:
        """
        qt_gui_helper.browse_dir_on_textbox( self.ui.TXT_DOWNLOAD )
    
    
    @exqtSlot()
    def on_BTN_VERIFY_DOWNLOAD_clicked( self ) -> None:
        """
        Signal handler: Stage 1 - verify
        """
        txt = self.ui.TXT_DOWNLOAD.text()
        
        if not os.path.isdir( txt ):
            self.alert( "'{}' is not a directory.".format( txt ) )
            return
        
        txt = os.path.join( txt, "bin", "neo4j" )
        
        if io_helper.get_system() == io_helper.ESystem.WINDOWS:
            txt += ".exe"
        
        if not os.path.isfile( txt ):
            self.alert( "'{}' does not exist.".format( txt ) )
            return
        
        self.next_page()
    
    
    @exqtSlot()
    def on_BTN_START_clicked( self ) -> None:
        """
        Signal handler: Stage 2 - start
        """
        ep = self.mk_endpoint( directory = self.ui.TXT_DOWNLOAD.text() )
        intermake.acquire( _start_neo4j,
                           window = self,
                           auto_close = True,
                           ).run( ep ).listen( self.__start_neo4j_completed )
    
    
    def __start_neo4j_completed( self, result: intermake.Result ):
        assert result.command == _start_neo4j
        
        if result.is_error:
            self.alert( "Couldn't start Neo4j.", str( result.exception ) )
        else:
            self.next_page()
    
    
    def __finish_wizard( self ):
        self.ui.BTN_OPTIMISE.setEnabled( False )
        self.ui.BTN_DONT_OPTIMISE.setEnabled( False )
        self.ui.LBL_FINISHED.setVisible( True )
    
    
    @exqtSlot()
    def on_BTN_OPEN_LOGON_clicked( self ) -> None:
        """
        Signal handler:
        """
        webbrowser.open( self.ui.BTN_OPEN_LOGON.text() )
    
    
    @exqtSlot()
    def on_BTN_VERIFY_LOGON_clicked( self ) -> None:
        """
        Signal handler:
        """
        ep = self.mk_endpoint( directory = self.ui.TXT_DOWNLOAD.text(),
                               user_name = self.ui.TXT_USERNAME.text(),
                               password = self.ui.TXT_PASSWORD.text() )
        
        intermake.acquire( neocommand.test_connection,
                           window = self,
                           auto_close = True,
                           ).run( ep ).listen( self.__test_connection_completed )
    
    
    def __test_connection_completed( self, result: intermake.Result ):
        if result.is_error:
            self.alert( "Couldn't logon to Neo4j due to a runtime exception.", str( result.exception ) )
        else:
            r: neocommand.Neo4jStatus = result.result
            
            if not r.is_running:
                self.alert( "Neo4j is not running.", r.error )
            elif not r.is_connected:
                self.alert( "Couldn't logon to Neo4j due to an error.", r.error )
            else:
                self.next_page()
    
    
    def mk_endpoint( self, *, name = "neo4j", user_name = "neo4j", password = "neo4j", directory = None, keyring = False ):
        return neocommand.DatabaseEndpoint( name = name,
                                            driver = "neo4jv1",
                                            remote_address = "127.0.0.1",
                                            user_name = user_name,
                                            password = password,
                                            directory = directory,
                                            is_unix = io_helper.get_system() != io_helper.ESystem.WINDOWS,
                                            port = "7474",
                                            keyring = keyring )
    
    
    @exqtSlot()
    def on_BTN_SAVE_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.ep = self.mk_endpoint( directory = self.ui.TXT_DOWNLOAD.text(),
                                    user_name = self.ui.TXT_USERNAME.text(),
                                    password = self.ui.TXT_PASSWORD.text(),
                                    keyring = True )
        
        neocommand.get_core().endpoint_manager.add_user_endpoint( self.ep )
        self.next_page()
    
    
    @exqtSlot()
    def on_BTN_OPTIMISE_clicked( self ) -> None:
        """
        Signal handler:
        """
        intermake.acquire( command = neocommand.apply_schema,
                           window = self
                           ).run( self.ep ).listen( self.__applied_schema )
    
    
    def __applied_schema( self, result: intermake.Result ):
        if result.is_error:
            self.alert( "Failed to apply schema due to a runtime exception.", str( result.exception ) )
        else:
            self.__finish_wizard()
    
    
    @exqtSlot()
    def on_BTN_DONT_OPTIMISE_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__finish_wizard()


@Application.INSTANCE.command( visibility = intermake.visibilities.INTERNAL )
def _start_neo4j( endpoint: neocommand.DatabaseEndpoint ) -> None:
    """
    Starts the Neo4j server.
    This is a private Command.
    
    :param endpoint:   Endpoint 
    """
    neocommand.control_server( endpoint, neocommand.ENeo4jCommand.START )
    out = neocommand.control_server( endpoint, neocommand.ENeo4jCommand.STATUS )
    if not "Neo4j is running" in out:
        raise ValueError( "Failed to start Neo4j. Neo4j reported the following: {}".format( out ) )
