from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QDialog, QWidget, QMessageBox
from mhelper import NOT_PROVIDED

import intermake


class AbstractB42SubWindow( QDialog ):
    __sig_shown = pyqtSignal()
    
    
    def __init__( self, parent: QWidget ):
        """
        CONSTRUCTOR
        """
        from bio42_gui.forms.frm_b42main import FrmB42Main
        self.main_window: FrmB42Main = parent
        super().__init__( parent )
        
        self.__sig_shown_emitted = False
        self.__sig_shown.connect( self.on_shown, Qt.QueuedConnection )
    
    
    def show_command( self, command, **kwargs ) -> intermake.Result:
        return self.main_window.controller.acquire( command, window = self, confirm = True ).run( **kwargs )
    
    
    def information( self, message ):
        QMessageBox.information( self,
                                 self.windowTitle(),
                                 message )
    
    
    def on_plugin_completed( self, result: intermake.Result ):
        pass
    
    
    def on_shown( self ):
        """
        This is called to allow the derived class to process any response after
        the dialogue is first shown and is visible to the user.
        """
        pass
    
    
    def on_get_result( self ):
        """
        This is called to allow the derived class to return any response to
        `request` having been called. If this is not implemented the result
        of `exec_` is returned.
        """
        return NOT_PROVIDED
    
    
    @classmethod
    def request( cls, parent: QWidget, *args, **kwargs ):
        from bio42_gui.forms.frm_b42main import FrmB42Main
        parent: FrmB42Main = parent
        # noinspection PyArgumentList
        frm = cls( parent, *args, **kwargs )
        parent.child_windows.append( frm )
        r = frm.exec_()
        parent.child_windows.remove( frm )
        x = frm.on_get_result()
        if x is not NOT_PROVIDED:
            r = x
        return r
    
    
    def showEvent( self, e: QShowEvent ):
        super().showEvent( e )
        
        if self.__sig_shown_emitted:
            return
        
        self.__sig_shown_emitted = True
        self.__sig_shown.emit()  # callback to be received AFTER the window is fully displayed
