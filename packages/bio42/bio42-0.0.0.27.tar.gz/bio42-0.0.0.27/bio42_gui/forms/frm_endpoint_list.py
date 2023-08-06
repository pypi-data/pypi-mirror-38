from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from mhelper_qt import exceptToGui, exqtSlot, menu_helper, tree_helper
from typing import Optional

import intermake
import neocommand

from bio42_gui.forms.designer.resources import resources
from bio42_gui.forms.designer import frm_endpoint_list_designer
from bio42_gui.forms.frm_b42_base import AbstractB42SubWindow


class FrmEndpointList( AbstractB42SubWindow ):
    """
    Displays the list of endpoints.
    """
    TAG_ENDPOINT = "_FrmEndpointList__tag_endpoint"
    
    
    @exceptToGui()
    def __init__( self, parent: QWidget ):
        """
        CONSTRUCTOR
        """
        super().__init__( parent )
        self.ui = frm_endpoint_list_designer.Ui_Dialog( self )
        self.setWindowTitle( "Endpoint list" )
        self.update_view()
        tree_helper.set_as_list( self.ui.TVW_MAIN )
    
    
    def update_view( self ):
        self.ui.TVW_MAIN.clear()
        
        headers = QTreeWidgetItem()
        headers.setText( 0, "Name" )
        headers.setText( 1, "Value" )
        self.ui.TVW_MAIN.setHeaderItem( headers )
        
        for endpoint in neocommand.get_core().endpoint_manager:
            endpoint: neocommand.Endpoint = endpoint
            item = QTreeWidgetItem()
            item.setText( 0, endpoint.name )
            item.setText( 1, str( endpoint ) )
            item.setIcon( 0, resources.endpoint.icon() )
            setattr( item, self.TAG_ENDPOINT, endpoint )
            self.ui.TVW_MAIN.addTopLevelItem( item )
        
        tree_helper.resize_all( self.ui.TVW_MAIN )
    
    
    def __command_complete( self, _: intermake.Result ) -> None:
        self.update_view()
    
    
    def get_selected( self ) -> Optional[neocommand.Endpoint]:
        items = self.ui.TVW_MAIN.selectedItems()
        
        if len( items ) != 1:
            return None
        
        item = items[0]
        return getattr( item, self.TAG_ENDPOINT )
    
    
    def has_selected( self ) -> bool:
        return self.get_selected() is not None
    
    
    @exqtSlot()
    def on_BTN_ADD_clicked( self ) -> None:
        """
        Signal handler:
        """
        opts = ["Database", "Parcel", "File"]
        
        m = menu_helper.show_menu( self, opts )
        
        if m == "Database":
            self.show_command( neocommand.endpoints.open_database ).listen( self.__command_complete )
        elif m == "File":
            self.show_command( neocommand.endpoints.open_file ).listen( self.__command_complete )
        elif m == "Parcel":
            self.show_command( neocommand.endpoints.open_parcel ).listen( self.__command_complete )
    
    
    @exqtSlot()
    def on_BTN_REMOVE_clicked( self ) -> None:
        """
        Signal handler:
        """
        if self.has_selected():
            self.show_command( neocommand.endpoints.close, endpoint = self.get_selected(), delete = False ).listen( self.__command_complete )
    
    
    @exqtSlot()
    def on_BTN_DELETE_clicked( self ) -> None:
        """
        Signal handler:
        """
        if self.has_selected():
            self.show_command( neocommand.endpoints.close, endpoint = self.get_selected(), delete = True ).listen( self.__command_complete )
    
    
    @exqtSlot()
    def on_BTN_REFRESH_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.update_view()
    
    
    @exqtSlot()
    def on_BTN_OK_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.close()
