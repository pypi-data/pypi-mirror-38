from typing import Iterable, cast
from mhelper_qt import ComboBoxWrapper, exqtSlot
from PyQt5.QtWidgets import QWidget

import intermake
import mhelper
import neocommand

from bio42_gui.forms.designer import frm_transfer_designer
from bio42_gui.forms.frm_b42_base import AbstractB42SubWindow


class FrmTransfer( AbstractB42SubWindow ):
    """
    Friendly GUI for the `transfer` command.
    """
    
    
    def __init__( self,
                  parent: QWidget,
                  source: neocommand.Endpoint = None ):
        """
        CONSTRUCTOR
        """
        super().__init__( parent )
        self.ui = frm_transfer_designer.Ui_Dialog( self )
        self.setWindowTitle( "Transfer" )
        
        self.protocols = ComboBoxWrapper( self.ui.CBM_PROTO, cast( Iterable, neocommand.EParcelMethod ), lambda x: x.name )
        self.destinations = ComboBoxWrapper( self.ui.CMB_DEST, (x for x in neocommand.get_core().endpoint_manager if isinstance( x, neocommand.Destination )), lambda x: x.name )
        self.sources = ComboBoxWrapper( self.ui.CMB_SOURCE, (x for x in neocommand.get_core().endpoint_manager if isinstance( x, neocommand.Origin )), lambda x: x.name )
        
        if source is not None:
            if source in self.sources:
                self.sources.selected = source
            else:
                self.sources.append( source, True )
        
        self.ui.CMB_DEST.currentIndexChanged.connect( self.update_info )
        self.ui.CMB_SOURCE.currentIndexChanged.connect( self.update_info )
        self.ui.CBM_PROTO.currentIndexChanged.connect( self.update_info )
        
        self.update_info()
        self.result = None
    
    
    def get_selected( self ):
        return self.sources.selected, self.destinations.selected, self.protocols.selected
    
    
    def get_doc( self, x: neocommand.Endpoint ):
        if x is None:
            return "No endpoint selected"
        else:
            return str( x ) + "\n\n" + mhelper.documentation_helper.get_basic_documentation( x )
    
    
    def update_info( self ):
        s, d, p = self.get_selected()
        
        if p is None:
            tp = "No protocol selected"
        else:
            tp = mhelper.documentation_helper.get_enum_documentation( p )
        
        self.ui.LBL_SRC_INFO.setText( self.get_doc( s ) )
        self.ui.LBL_DEST_INFO.setText( self.get_doc( d ) )
        self.ui.LBL_PROTO_INFO.setText( tp )
    
    
    @exqtSlot()
    def on_BTNBOX_MAIN_accepted( self ) -> None:
        """
        Signal handler:
        """
        s, d, p = self.get_selected()
        
        asr = intermake.Controller.ACTIVE \
            .acquire( neocommand.transfer,
                      window = self ) \
            .run( s, d, p )
        
        asr.listen( self.on_completed )
    
    
    def on_completed( self, result: intermake.Result ):
        if result.is_success:
            self.close()
    
    
    @exqtSlot()
    def on_BTNBOX_MAIN_rejected( self ) -> None:
        """
        Signal handler:
        """
        self.reject()
