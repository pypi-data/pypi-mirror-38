from bio42_gui.forms.frm_b42main import FrmB42Main

import intermake
import intermake_qt


class B42GuiSettings:
    """
    :ivar auto_load_bio42_scripts: Load `bio42_scripts` library scripts when showing the query window
    """
    KEY = "b42_gui_settings"
    
    
    def __init__( self ):
        self.auto_load_bio42_scripts = True


class B42GuiController( intermake_qt.GuiControllerWithBrowser ):
    def __init__( self ):
        super().__init__()
        self.b42_gui_settings = intermake.Controller.ACTIVE.app.local_data.bind( B42GuiSettings.KEY, B42GuiSettings() )
        
        import bio42_gui.controller.editorium
        bio42_gui.controller.editorium.register_with( self.editorium )
    
    
    def on_create_window( self, args ):
        # Initialise resources
        # noinspection PyUnresolvedReferences
        from bio42_gui.forms.designer.resources import resources_rc
        
        # Get main window
        return FrmB42Main( self )
