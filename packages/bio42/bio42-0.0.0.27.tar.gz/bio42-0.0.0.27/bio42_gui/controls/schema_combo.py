from PyQt5.QtWidgets import QComboBox
from typing import Optional, Sequence, Union
from mhelper import MEnum
import neocommand


class ESchema( MEnum ):
    NODE = 1
    EDGE = 2
    NODE_PROPERTY = 4
    EDGE_PROPERTY = 8


def add_schema( target: QComboBox, mode: ESchema, left: Optional[Sequence[neocommand.EntitySchema]], right: Optional[Union[Sequence[type], Sequence[neocommand.EntitySchema]]] ):
    SchemaComboBox( target, mode, left, right )


class SchemaComboBox:
    def __init__( self, target: QComboBox, mode: ESchema, left: Optional[Sequence[neocommand.EntitySchema]], right: Optional[Union[Sequence[type], Sequence[neocommand.EntitySchema]]] ):
        """
        
        :param target:      Target. 
        :param mode:        Mode of display.
        :param left:        If `NODE`:          Filter: *      - [left]    -> [options]
                               `EDGE`:          Filter: [left] - [options] -> *
                               `NODE_PROPERTY`: Filter: [left].[options] : *
                               `EDGE_PROPERTY`: Filter: [left].[options] : *
        :param right:       If `NODE`:          Filter: [options] - [right]    -> *
                               `EDGE`:          Filter: *         - [options]  -> [right]
                               `NODE_PROPERTY`: Filter: *.[options] : [right]
                               `EDGE_PROPERTY`: Filter: *.[options] : [right]
        """
        self.target: QComboBox = target
        self.mode: ESchema = mode
        self.left: Optional[Sequence[neocommand.EntitySchema]] = left
        self.right: Optional[Union[Sequence[type], Sequence[neocommand.EntitySchema]]] = right
        self.update()
    
    
    def update( self ):
        self.target.clear()
        
        if self.mode == ESchema.NODE:
            for node in neocommand.get_core().schema.node.find( self.left, self.right ):
                self.target.addItem( node.label )
        
        if self.mode == ESchema.EDGE_PROPERTY:
            for node in neocommand.get_core().schema.edges.find( self.left, self.right ):
                self.target.addItem( node.label )
        
        if self.mode in (ESchema.NODE_PROPERTY, ESchema.EDGE_PROPERTY):
            if self.left is not None:
                lst = self.left
            elif self.mode == ESchema.NODE_PROPERTY:
                lst = neocommand.get_core().schema.nodes
            else:
                lst = neocommand.get_core().schema.edges
            
            for entity in lst:
                for prop in entity.properties:
                    if self.right is not None:
                        if not any( prop.type is x for x in self.right ):
                            continue
                    
                    self.target.addItem( prop.name )
