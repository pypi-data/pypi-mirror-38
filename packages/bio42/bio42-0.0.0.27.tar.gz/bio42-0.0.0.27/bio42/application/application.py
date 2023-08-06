"""
Defines and instantiates the application.
"""

import intermake
import neocommand
from bio42 import __version__
from bio42.application import help


class Application( neocommand.Application ):
    INSTANCE: "Application" = None
    
    
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        
        from bio42 import schema
        schema.register( self.core.schema )
    
    
    def on_create_controller( self, mode: str ) -> intermake.Controller:
        if intermake.EImRunMode.is_gui( mode ):
            import bio42_gui
            return bio42_gui.B42GuiController()
        
        return super().on_create_controller( mode )


Application.INSTANCE = Application( inherit = neocommand.Application.INSTANCE,
                                    name = "bio42",
                                    version = __version__ )
app = Application.INSTANCE
help.init( Application.INSTANCE )
