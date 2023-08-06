from os import path
from PyQt5.QtWidgets import QInputDialog, QWidget, QMessageBox
from mhelper import file_helper, io_helper, safe_cast
from mhelper_qt import exceptToGui, exqtSlot

import os
import webbrowser
import intermake
import neocommand

from bio42_gui.forms.designer import frm_database_designer
from bio42_gui.forms.frm_b42_base import AbstractB42SubWindow


_SS_WAIT = "busy"
_SS_ON = "online"
_SS_OFF = "offline"
_SS_ERROR = "error"


class FrmDatabase( AbstractB42SubWindow ):
    """
    Friendly GUI for the `transfer` command.
    """
    
    
    @exceptToGui()
    def __init__( self, parent: QWidget ):
        """
        CONSTRUCTOR
        """
        super().__init__( parent )
        self.ui = frm_database_designer.Ui_Dialog( self )
        self.ui.GRP_ENDPOINT.setVisible( False )
        self.ui.GRP_DATABASE.setVisible( False )
        self.setWindowTitle( "Database" )
        self.endpoint_list = []
        self.known_status = None
        self.status: neocommand.Neo4jStatus = None
        self.shown = False
    
    
    def on_shown( self ):
        self.update_status( None )
    
    
    @property
    def s_endpoint( self ):
        return self.status.endpoint if self.status is not None else None
    
    
    @property
    def s_database( self ):
        return self.status.database if self.status is not None else None
    
    
    def update_endpoints_list( self ):
        self.ui.CMB_ENDPOINT.clear()
        self.endpoint_list.clear()
        
        for endpoint in neocommand.get_core().endpoint_manager:
            if isinstance( endpoint, neocommand.DatabaseEndpoint ):
                self.ui.CMB_ENDPOINT.addItem( endpoint.name )
                self.endpoint_list.append( endpoint )
        
        if not self.endpoint_list:
            QMessageBox.warning( self, "Oops", "You haven't defined any database endpoints. You won't be able to query the database until you do so." )
        
        if self.s_endpoint is not None:
            try:
                index = self.endpoint_list.index( self.s_endpoint )
            except ValueError:
                index = -1
            
            self.ui.CMB_ENDPOINT.setCurrentIndex( index )
    
    
    def update_database_list( self, selection: str = None ):
        self.ui.CMB_DATABASE.clear()
        
        if self.s_endpoint is None:
            return
        
        src_dir = path.join( self.s_endpoint.directory, "data/databases" )
        items = []
        
        for dir in file_helper.list_dir( src_dir ):
            if not path.isdir( dir ):
                continue
            
            if not path.isfile( path.join( dir, "neostore" ) ):
                if len( os.listdir( dir ) ) != 0:
                    continue
            
            name = file_helper.get_filename( dir )
            
            self.ui.CMB_DATABASE.addItem( name )
            items.append( name )
        
        selection = selection or self.s_database
        
        if selection:
            try:
                index = items.index( selection )
            except ValueError:
                index = -1
            
            self.ui.CMB_DATABASE.setCurrentIndex( index )
    
    
    def update_status( self, target ):
        #
        # Select the first database if no `target` is specified
        #
        if target is None:
            for endpoint in neocommand.get_core().endpoint_manager:
                if isinstance( endpoint, neocommand.DatabaseEndpoint ):
                    target = endpoint
                    break
        
        #
        # Reset our information
        #
        self.status = None
        
        #
        # Clear the text if there is no suitable target
        #
        if target is None:
            self.ui.TXT_SERVER.setText( "(none)" )
            self.ui.TXT_DATABASE.setText( "N/A" )
            self.ui.TXT_STATUS.setText( "N/A" )
            self.set_label( "error", "no database selected" )
            return
        
        #
        # If there is a suitable target, display "please wait"
        #
        self.ui.TXT_SERVER.setText( "(please wait)" )
        self.ui.TXT_DATABASE.setText( "(please wait)" )
        self.ui.TXT_STATUS.setText( "(please wait)" )
        self.set_label( _SS_WAIT, "(please wait)" )
        
        #
        # Send the command asking for information
        #
        intermake \
            .acquire( neocommand.test_connection,
                      window = self,
                      auto_close = True,
                      callback = self.__test_connection_callback ) \
            .run( target )
    
    
    def __test_connection_callback( self, result: intermake.Result ):
        if result.is_error:
            return
        
        if result.command in (neocommand.set_database, neocommand.control_server):
            assert self.s_endpoint, "Didn't expect endpoint to change whilst database was being controlled."
            self.update_status( self.s_endpoint )
            return
        
        self.handle_status( safe_cast( neocommand.Neo4jStatus, result.result ) )
    
    
    def handle_status( self, status: neocommand.Neo4jStatus ):
        self.status = status
        self.ui.TXT_DATABASE.setText( status.database or "Unknown" )
        self.ui.TXT_SERVER.setText( status.endpoint.name )
        
        if status.error:
            self.set_label( _SS_ERROR, status.error )
        elif status.is_connected:
            self.set_label( _SS_ON, status.version )
        elif status.is_running:
            self.set_label( _SS_ERROR, "running but not connected (?) should have received an error code from neocommand but didn't." )
        else:
            self.set_label( _SS_OFF, status.version )
    
    
    def set_label( self, i, x ):
        self.known_status = i
        self.ui.TXT_STATUS.setText( i + ((" - " + x) if x else "") )
        self.ui.BTN_START.setEnabled( i is _SS_OFF )
        self.ui.BTN_STOP.setEnabled( i is _SS_ON )
        self.ui.BTN_REFRESH.setEnabled( i is not _SS_WAIT )
        self.ui.BTN_DATABASE.setEnabled( i is _SS_OFF )
        self.ui.BTN_ENDPOINT.setEnabled( i is not _SS_WAIT )
        self.ui.BTN_OPEN_BROWSER.setEnabled( i is _SS_ON )
        self.ui.BTN_SHOW_CONFIG.setEnabled( i is _SS_OFF or i is _SS_ERROR )
        
        if i is _SS_ON:
            self.ui.LBL_STATUS_COLOUR.setStyleSheet( "background: green;" )
        elif i is _SS_OFF:
            self.ui.LBL_STATUS_COLOUR.setStyleSheet( "background: darkred;" )
        else:
            self.ui.LBL_STATUS_COLOUR.setStyleSheet( "background: #C0C000;" )
    
    
    def set_display_page( self, i ):
        self.ui.GRP_ENDPOINT.setVisible( i == 1 and not self.ui.GRP_ENDPOINT.isVisible() )
        self.ui.GRP_DATABASE.setVisible( i == 2 and not self.ui.GRP_DATABASE.isVisible() )
    
    
    @exqtSlot()
    def on_BTN_START_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.set_display_page( 0 )
        
        if self.known_status is not _SS_OFF:
            return
        
        if self.s_endpoint is None:
            return
        
        neocommand.control_server( self.s_endpoint, neocommand.ENeo4jCommand.START )
    
    
    @exqtSlot()
    def on_BTN_STOP_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.set_display_page( 0 )
        
        if self.known_status is not _SS_ON:
            return
        
        if self.s_endpoint is None:
            return
        
        neocommand.control_server( self.s_endpoint, neocommand.ENeo4jCommand.STOP )
    
    
    @exqtSlot()
    def on_BTN_APPLYDB_clicked( self ) -> None:
        """
        Signal handler:
        """
        if self.known_status is not _SS_OFF:
            return
        
        if self.s_endpoint is None:
            return
        
        neocommand.set_database( self.s_endpoint, self.ui.CMB_DATABASE.currentText() )
    
    
    @exqtSlot()
    def on_BTN_OPEN_BROWSER_clicked( self ) -> None:
        """
        Signal handler:
        """
        if self.s_endpoint is None:
            return
        
        url = "http://{}:{}".format( self.s_endpoint.remote_address, self.s_endpoint.port )
        webbrowser.open( url )
    
    
    @exqtSlot()
    def on_BTN_SHOW_CONFIG_clicked( self ) -> None:
        """
        Signal handler:
        """
        if self.s_endpoint is None:
            return
        
        url = path.join( self.s_endpoint.directory, "conf", "neo4j.conf" )
        io_helper.system_select( url )
    
    
    @exqtSlot()
    def on_BTN_NEWDB_clicked( self ) -> None:
        """
        Signal handler:
        """
        if self.s_endpoint is None:
            return
        
        name, ok = QInputDialog.getText( self, "New database", "Please name your database" )
        
        if not name or not ok:
            return
        
        dir = path.join( self.s_endpoint.directory, "data", "databases", name )
        file_helper.create_directory( dir )
        
        self.update_database_list( name )
    
    
    @exqtSlot()
    def on_BTN_UPDATE_ENDPOINT_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.set_display_page( 0 )
        
        i = self.ui.CMB_ENDPOINT.currentIndex()
        
        if i == -1:
            return None
        
        self.update_status( self.endpoint_list[i] )
    
    
    @exqtSlot()
    def on_BTN_ENDPOINT_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.set_display_page( 1 )
        
        if self.ui.GRP_ENDPOINT.isVisible():
            self.update_endpoints_list()
    
    
    @exqtSlot()
    def on_BTN_DATABASE_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.set_display_page( 2 )
        
        if self.ui.GRP_DATABASE.isVisible():
            self.update_database_list()
    
    
    @exqtSlot()
    def on_BTN_REFRESH_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.set_display_page( 0 )
        
        if self.known_status is _SS_WAIT:
            return
        
        self.update_status( self.s_endpoint )
