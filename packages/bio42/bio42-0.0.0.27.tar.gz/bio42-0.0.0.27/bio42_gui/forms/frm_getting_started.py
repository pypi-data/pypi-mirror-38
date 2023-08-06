from PyQt5.QtWidgets import QWidget
from mhelper_qt import exqtSlot

from bio42_gui.forms.designer import frm_getting_started_designer as _my_form
from bio42_gui.forms.frm_b42_base import AbstractB42SubWindow


class FrmGettingStarted( AbstractB42SubWindow ):
    """
    Provides shortcuts to some basic commands to get the user started.
    
    The result of `request`ing this form is one of the `O_*` members, or `None`.
    """
    O_CREATE_PARCEL = object()
    O_PUT_DATA_IN = object()
    O_OPEN_CONNECTION = object()
    O_CREATE_DATABASE = object()
    O_EXPLORE_DATA = object()
    
    
    def __init__( self, parent: QWidget ):
        """
        CONSTRUCTOR
        """
        super().__init__( parent )
        self.ui = _my_form.Ui_Dialog( self )
        self.setWindowTitle( "Getting Started" )
        self.result = None
    
    
    def on_get_result( self ):
        return self.result
    
    
    @exqtSlot()
    def on_BTN_CREATE_PARCEL_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.result = self.O_CREATE_PARCEL
        self.accept()
    
    
    @exqtSlot()
    def on_BTN_PUT_DATA_IN_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.result = self.O_PUT_DATA_IN
        self.accept()
    
    
    @exqtSlot()
    def on_BTN_OPEN_CONNECTION_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.result = self.O_OPEN_CONNECTION
        self.accept()
    
    
    @exqtSlot()
    def on_BTN_CREATE_DATABASE_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.result = self.O_CREATE_DATABASE
        self.accept()
    
    
    @exqtSlot()
    def on_BTN_EXPLORE_DATA_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.result = self.O_EXPLORE_DATA
        self.accept()
