from typing import Iterable
import editorium
import neocommand


class DatabaseDriverEditor( editorium.AbstractEnumEditor ):
    def on_get_options( self, info: editorium.EditorInfo ) -> Iterable[object]:
        return neocommand.DbManager.DRIVER_CLASSES.keys()
    
    
    @classmethod
    def on_can_handle( cls, info: editorium.EditorInfo ) -> bool:
        return info.annotation.is_mannotation_of( neocommand.isDriverName )


def register_with( x: editorium.Editorium ):
    x.register( DatabaseDriverEditor )
