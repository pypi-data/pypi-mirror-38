from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox, QWidget
from bio42_gui.forms.designer import frm_import_csv_designer
from bio42_gui.forms.frm_b42_base import AbstractB42SubWindow
from mhelper import string_helper, file_helper
from mhelper_qt import exceptToGui, exqtSlot, qt_gui_helper, tree_helper
from typing import List, Optional

import os.path
import csv
import bio42
import intermake
import neocommand as nc





class FrmImportCsv( AbstractB42SubWindow ):
    """
    Guides the user through importing a CSV using the `import_csv` command.
    """
    
    
    class Settings:
        """
        :ivar history: List of CSV files previously imported.
        """
        
        def __init__( self ):
            self.history: List[str] = []
    
    
    def __init__( self, parent: QWidget ):
        """
        CONSTRUCTOR
        """
        super().__init__( parent )
        self.ui = frm_import_csv_designer.Ui_Dialog( self )
        self.setWindowTitle( "Import CSV" )
        self.settings = intermake.Controller.ACTIVE.app.local_data.store.bind( type( self ).__name__, self.Settings() )
        
        # Delimiters
        for x in (self.ui.CMB_DELIMITER, self.ui.CMB_ARRAY_DELIMITER):
            x.addItem( "," )
            x.addItem( "TAB" )
            x.addItem( ";" )
            x.addItem( "|" )
        
        self.ui.CMB_DELIMITER.setCurrentText( "," )
        self.ui.CMB_ARRAY_DELIMITER.setCurrentText( ";" )
        self.ui.CHK_F_HEADERS.setChecked( True )
        
        # Inputs
        self.ui.CMB_FILENAME.addItems( self.settings.history )
        self.handle_update_filename()
        
        # Destinations
        self.__update_destinations()
        
        s: nc.DatabaseSchema = nc.get_core().schema
        
        # Properties
        self.ui.CMB_E_NAME.addItems( sorted( s.get_distinct_property_names() ) )
        
        # Types
        self.ui.CMB_E_TYPE.addItems( ["*{}".format( x.name ) for x in nc.ENcvSpecial if x is not nc.ENcvSpecial.NONE] )
        self.ui.CMB_E_TYPE.addItems( sorted( x.neo4j_name for x in nc.NeoType.ALLA ) )
        
        # Fields
        self.ui.CMB_EDGE_DEST.addItems( sorted( x.label for x in s.node_schema ) )
        self.ui.CMB_EDGE_SOURCE.addItems( sorted( x.label for x in s.node_schema ) )
        self.ui.CMB_EDGE_LABEL.addItems( sorted( set( x.label for x in s.iter_entity_types() ) ) )
        
        # Fields
        self.prev_index = -1
        self.ignore_field_changes = False
        self.ignore_entity_changes = False
        
        # Display
        self.ui.STACK_MAIN.setCurrentIndex( 0 )
        
        # Signals
        # Stack widget 
        self.ui.STACK_MAIN.currentChanged[int].connect( self._on_current_changed )
        
        # Entity editor
        self.ui.LST_ENTITIES.itemSelectionChanged.connect( self.entity_to_ui )
        self.ui.CMB_EDGE_DEST.currentTextChanged.connect( self.entity_from_ui )
        self.ui.CMB_EDGE_LABEL.currentTextChanged.connect( self.entity_from_ui )
        self.ui.CMB_EDGE_SOURCE.currentTextChanged.connect( self.entity_from_ui )
        self.ui.RAD_EDGE.toggled[bool].connect( self.entity_from_ui )
        self.ui.RAD_NODE.toggled[bool].connect( self.entity_from_ui )
        
        # Field editor
        self.ui.TVW_FIELDS.itemSelectionChanged.connect( self.field_to_ui )
        self.ui.CMB_ENTITY.currentTextChanged.connect( self.field_from_ui )
        self.ui.CMB_E_NAME.currentTextChanged.connect( self.field_from_ui )
        self.ui.CMB_E_TYPE.currentTextChanged.connect( self.field_from_ui )
    
    
    def on_plugin_completed( self, result: intermake.Result ):
        self.__update_destinations()
    
    
    def __update_destinations( self ):
        self.ui.CMB_DESTINATION.clear()
        self.ui.CMB_DESTINATION.addItems( [x.name for x in nc.get_core().endpoint_manager] )
    
    
    def entity_to_ui( self ):
        if self.ignore_entity_changes:
            return
        
        ent: _Entity = self.get_selected_entity()
        
        if ent is None:
            return
        
        self.ignore_entity_changes = True
        self.ui.RAD_EDGE.setChecked( ent.is_edge )
        self.ui.RAD_NODE.setChecked( not ent.is_edge )
        self.ui.CMB_EDGE_SOURCE.setCurrentText( ent.start_label )
        self.ui.CMB_EDGE_DEST.setCurrentText( ent.end_label )
        self.ui.CMB_EDGE_LABEL.setCurrentText( ent.label )
        
        self.ignore_entity_changes = False
        self.entity_update_buttons()
    
    
    def entity_from_ui( self, *_, **__ ):
        ent: _Entity = self.get_selected_entity()
        
        if ent is None:
            return
        
        ent.is_edge = self.ui.RAD_EDGE.isChecked()
        ent.start_label = self.ui.CMB_EDGE_SOURCE.currentText()
        ent.label = self.ui.CMB_EDGE_LABEL.currentText()
        ent.end_label = self.ui.CMB_EDGE_DEST.currentText()
        
        self.ent_to_list( ent )
        self.entity_update_buttons()
    
    
    def entity_update_buttons( self ):
        ent = self.get_selected_entity()
        
        if ent is None:
            return
        
        self.ui.LBL_ENT_DEST.setEnabled( ent.is_edge )
        self.ui.CMB_EDGE_DEST.setEnabled( ent.is_edge )
        self.ui.LBL_ENT_SOURCE.setEnabled( ent.is_edge )
        self.ui.CMB_EDGE_SOURCE.setEnabled( ent.is_edge )
    
    
    def field_from_ui( self ):
        if self.ignore_field_changes:
            return
        
        field = self.get_selected_field()
        
        if field is None:
            return
        
        entity_str = self.ui.CMB_ENTITY.currentText()
        
        if entity_str == "*NONE":
            field.entity = None
        else:
            for entity in tree_helper.iter_data( self.ui.LST_ENTITIES ):
                if str( entity ) == entity_str:
                    field.entity = entity
                    break
        
        name = self.ui.CMB_E_NAME.currentText()
        type_str = self.ui.CMB_E_TYPE.currentText()
        
        if type_str.startswith( "*" ):
            try:
                special = nc.ENcvSpecial[type_str[1:]]
            except KeyError:
                special = nc.ENcvSpecial.UID
            
            field.field = nc.NcvHeader( None, None, special, None )
        else:
            try:
                type_ = nc.NeoType.from_name( type_str )
            except KeyError:
                type_ = nc.NeoType.STR
            
            field.field = nc.NcvHeader( name, type_, nc.ENcvSpecial.NONE, None )
        
        self.field_to_list( field )
        self.field_update_buttons()
    
    
    @exceptToGui()
    def field_to_ui( self ):
        field = self.get_selected_field()
        
        if field is None:
            return
        
        self.ignore_field_changes = True
        
        self.ui.label_15.setText( "Configure: {}".format( field.column ) )
        self.ui.CMB_ENTITY.setCurrentText( str( field.entity ) if field.entity is not None else "*NONE" )
        self.ui.CMB_E_NAME.setCurrentText( field.field.name )
        
        if field.field.special == nc.ENcvSpecial.NONE:
            self.ui.CMB_E_TYPE.setCurrentText( field.field.type.neo4j_name )
        else:
            self.ui.CMB_E_TYPE.setCurrentText( "*{}".format( field.field.special.name ) )
        
        self.ignore_field_changes = False
        self.field_update_buttons()
    
    
    def field_update_buttons( self ):
        field = self.get_selected_field()
        
        if field is None:
            return
        
        self.ui.CMB_E_TYPE.setEnabled( field.entity is not None )
        self.ui.LBL_E_TYPE.setEnabled( field.entity is not None )
        self.ui.CMB_E_NAME.setEnabled( field.entity is not None and field.field.special == nc.ENcvSpecial.NONE )
        self.ui.LBL_E_NAME.setEnabled( field.entity is not None and field.field.special == nc.ENcvSpecial.NONE )
    
    
    def field_to_list( self, field: "_Field" ):
        item = tree_helper.get_or_create_item( self.ui.TVW_FIELDS, field )
        item.setText( tree_helper.get_or_create_column( self.ui.TVW_FIELDS, "Index" ), str( field.index ) )
        item.setText( tree_helper.get_or_create_column( self.ui.TVW_FIELDS, "Header" ), str( field.column ) )
        item.setText( tree_helper.get_or_create_column( self.ui.TVW_FIELDS, "Example" ), field.sample )
        
        if field.entity is not None:
            item.setText( tree_helper.get_or_create_column( self.ui.TVW_FIELDS, "Entity" ), str( field.entity ) )
            
            if field.field.special != nc.ENcvSpecial.NONE:
                item.setText( tree_helper.get_or_create_column( self.ui.TVW_FIELDS, "Type" ), "*{}".format( field.field.special ) )
                item.setText( tree_helper.get_or_create_column( self.ui.TVW_FIELDS, "Name" ), "--" )
            else:
                item.setText( tree_helper.get_or_create_column( self.ui.TVW_FIELDS, "Type" ), str( field.field.type.neo4j_name ) )
                item.setText( tree_helper.get_or_create_column( self.ui.TVW_FIELDS, "Name" ), str( field.field.name ) )
        else:
            item.setText( tree_helper.get_or_create_column( self.ui.TVW_FIELDS, "Entity" ), "--" )
            item.setText( tree_helper.get_or_create_column( self.ui.TVW_FIELDS, "Type" ), "--" )
            item.setText( tree_helper.get_or_create_column( self.ui.TVW_FIELDS, "Name" ), "--" )
    
    
    def ent_to_list( self, ent: "_Entity" ):
        item = tree_helper.get_or_create_item( self.ui.LST_ENTITIES, ent )
        item.setText( tree_helper.get_or_create_column( self.ui.LST_ENTITIES, "Type" ), "Edge" if ent.is_edge else "Node" )
        item.setText( tree_helper.get_or_create_column( self.ui.LST_ENTITIES, "Start" ), ent.start_label if ent.is_edge else "" )
        item.setText( tree_helper.get_or_create_column( self.ui.LST_ENTITIES, "Label" ), ent.label )
        item.setText( tree_helper.get_or_create_column( self.ui.LST_ENTITIES, "End" ), ent.end_label if ent.is_edge else "" )
        
        item.setForeground( 0, QColor( 0, 0, 0 ) if ent.is_valid else QColor( 255, 0, 0 ) )
    
    
    def get_selected_field( self ) -> Optional["_Field"]:
        return tree_helper.get_selected_data( self.ui.TVW_FIELDS )
    
    
    def get_selected_entity( self ) -> Optional["_Entity"]:
        return tree_helper.get_selected_data( self.ui.LST_ENTITIES )
    
    
    @exceptToGui()
    def _on_current_changed( self, index: int ):
        is_advance = self.prev_index < index
        self.prev_index = index
        self.ui.BTN_BACK.setEnabled( self.ui.STACK_MAIN.currentIndex() != 0 )
        self.ui.BTN_NEXT.setEnabled( self.ui.STACK_MAIN.currentIndex() != self.ui.STACK_MAIN.count() - 1 )
        self.ui.BTN_OK.setEnabled( self.ui.STACK_MAIN.currentIndex() == self.ui.STACK_MAIN.count() - 1 )
        
        if is_advance:
            if index == 2:
                # Entities
                
                if not os.path.isfile( self.ui.CMB_FILENAME.currentText() ):
                    self.ui.STACK_MAIN.setCurrentIndex( 1 )
                    QMessageBox.warning( self, "Oops", "Select a valid file before continuing." )
                    return
                
                # Save filename 
                fn = self.ui.CMB_FILENAME.currentText()
                if os.path.isfile( fn ):
                    if fn in self.settings.history:
                        self.settings.history.remove( fn )
                    
                    self.settings.history.insert( 0, fn )
                    intermake.Controller.ACTIVE.app.local_data.store.commit( self.settings )
                
                # Populate defaults
                self.ui.LST_ENTITIES.clear()
                
                if self.ui.CHK_F_FILENAME_LABELS.isChecked():
                    nf = nc.NcvFilename.construct_from_file( self.ui.CMB_FILENAME.currentText() )
                    
                    if nf.is_edge:
                        self.ent_to_list( _Entity( False, nf.start_label, "", "" ) )
                        self.ent_to_list( _Entity( False, nf.end_label, "", "" ) )
                        self.ent_to_list( _Entity( True, nf.label, nf.start_label, nf.end_label ) )
                    else:
                        self.ent_to_list( _Entity( False, nf.label, "", "" ) )
                
                if self.ui.LST_ENTITIES.topLevelItemCount() == 0:
                    self.ent_to_list( _Entity( False, "", "", "" ) )
                
                # Select first
                self.ui.LST_ENTITIES.setCurrentItem( self.ui.LST_ENTITIES.topLevelItem( 0 ) )
            elif index == 3:
                # Fields
                # Entity list
                self.ui.CMB_ENTITY.clear()
                self.ui.CMB_ENTITY.addItem( "*NONE" )
                for entity in tree_helper.iter_data( self.ui.LST_ENTITIES ):
                    self.ui.CMB_ENTITY.addItem( str( entity ) )
                
                # Default fields
                self.ui.TVW_FIELDS.clear()
                
                with open( self.ui.CMB_FILENAME.currentText(), "r" ) as file:
                    headers = None
                    
                    for row in csv.reader( file, delimiter = self.get_delimiter() ):
                        if headers is None:
                            headers = row
                        else:
                            row0 = row
                            break
                    else:
                        headers = ()
                        row0 = ()
                
                if self.ui.CHK_F_HEADERS.isChecked():
                    for index, (header_, row0_) in enumerate( zip( headers, row0 ) ):
                        header_: str = header_.strip()
                        row0_: str = row0_.strip()
                        
                        if "." in header_:
                            entity_str, header = header_.split( ".", 1 )
                        else:
                            header = header_
                            entity_str = None
                        
                        for e in tree_helper.iter_data( self.ui.LST_ENTITIES ):
                            assert isinstance( e, _Entity )
                            
                            if str( e ) == entity_str:
                                entity = e
                                break
                            elif e.label == entity_str:
                                entity = e
                                break
                        
                        if self.ui.CHK_F_TYPE_INFO.isChecked():
                            hd = nc.NcvHeader.from_decorated_name( None, header )
                            self.field_to_list( _Field( index, header_, entity, nc.NcvHeader( hd.name, hd.type, hd.special ), row0_ ) )
                        else:
                            hd = header.lower().replace( " ", "_" )
                            self.field_to_list( _Field( index, header_, entity, nc.NcvHeader( hd, nc.NeoType.STR, nc.ENcvSpecial.NONE ), row0_ ) )
                else:
                    for index, header_ in enumerate( headers ):
                        header_: str = header_.strip()
                        self.field_to_list( _Field( index, "#{}".format( index ), None, nc.NcvHeader( "untitled_{}".format( index ), nc.NeoType.STR, nc.ENcvSpecial.NONE ), header_ ) )
                
                # Select first
                self.ui.TVW_FIELDS.setCurrentItem( self.ui.TVW_FIELDS.topLevelItem( 0 ) )
            elif index == 4:
                # Review
                r = []
                r.append( "<html><body>" )
                r.append( "<h2>Summary</h2>" )
                r.append( "<table border=1>" )
                r.append( "<tr><td><b>{}</b></td><td><b>{}</b></td><td><b>{}</b></td></tr>".format( "Column", "Entity", "Field" ) )
                invalid = []
                
                for field in tree_helper.iter_data( self.ui.TVW_FIELDS ):
                    assert isinstance( field, _Field )
                    try:
                        r.append( "<tr><td>{}. \"<i>{}</i>\"</td><td>{}</td><td>{}</td></tr>".format( field.index, field.column, field.entity, field.field.decorated_name( field.entity ) if field.entity else "-" ) )
                        field.validate()
                    except Exception as ex:
                        invalid.append( (field, repr( ex )) )
                
                r.append( "</table>" )
                
                for entity in tree_helper.iter_data( self.ui.LST_ENTITIES ):
                    assert isinstance( entity, _Entity )
                    try:
                        entity.validate()
                    except Exception as ex:
                        invalid.append( (entity, repr( ex )) )
                
                r.append( "<h2>Issues</h2>" )
                if invalid:
                    r.append( "<p>Cannot continue: At least one entity or field is not configured: {}</p>".format( string_helper.format_array( invalid, format = "“{}”".format ) ) )
                    self.ui.BTN_OK.setEnabled( False )
                else:
                    r.append( "<p>No issues.</p>" )
                
                r.append( "<h2>Fields data</h2>" )
                r.append( "<ul>" )
                r.append( "".join( "<li>“{}”</li>".format( x ) for x in self.get_field_text() ) )
                r.append( "</ul>" )
                r.append( "</body></html>" )
                
                self.ui.LBL_REVIEW.setText( "\n".join( r ) )
    
    
    def get_delimiter( self ):
        return self.process_delimiter( self.ui.CMB_DELIMITER.currentText() )
    
    
    def process_delimiter( self, d ):
        if d in ("TAB", "\\t"):
            d = "\t"
        elif d in ("SPACE", "\\s"):
            d = " "
        elif d in ("CR", "\\r"):
            d = "\r"
        
        if len( d ) != 1:
            raise ValueError( "«{}» is not an acceptable delimiter.".format( d ) )
        
        return d
    
    
    def get_array_delimiter( self ):
        return self.process_delimiter( self.ui.CMB_ARRAY_DELIMITER.currentText() )
    
    
    @exqtSlot()
    def on_BTN_BACK_clicked( self ) -> None:
        """
        Signal handler:
        """
        if QMessageBox.question( self,
                                 self.windowTitle(),
                                 "If you go back you will lose any changes on the current page?",
                                 QMessageBox.Ok | QMessageBox.Cancel
                                 ) != QMessageBox.Ok:
            return
        
        if self.ui.STACK_MAIN.currentIndex() > 0:
            self.ui.STACK_MAIN.setCurrentIndex( self.ui.STACK_MAIN.currentIndex() - 1 )
    
    
    @exqtSlot()
    def on_BTN_NEXT_clicked( self ) -> None:
        """
        Signal handler:
        """
        if self.ui.STACK_MAIN.currentIndex() < self.ui.STACK_MAIN.count() - 1:
            self.ui.STACK_MAIN.setCurrentIndex( self.ui.STACK_MAIN.currentIndex() + 1 )
    
    
    @exqtSlot()
    def on_BTN_OK_clicked( self ) -> None:
        """
        Signal handler:
        """
        file = self.ui.CMB_FILENAME.currentText()
        endpoint = nc.get_core().endpoint_manager.find_endpoint( self.ui.CMB_DESTINATION.currentText() )
        delimiter = self.get_delimiter()
        array_delimiter = self.get_array_delimiter()
        fields = self.get_field_text()
        
        intermake.acquire( bio42.import_csv, window = self ) \
            .run( file = file,
                  endpoint = endpoint,
                  fields = fields,
                  delimiter = delimiter,
                  array_delimiter = array_delimiter )
    
    
    def get_field_text( self ):
        fields = []
        
        for field in tree_helper.iter_data( self.ui.TVW_FIELDS ):
            assert isinstance( field, _Field )
            assert field.index == len( fields )
            fields.append( field.to_import_csv() )
        
        return fields
    
    
    @exqtSlot()
    def on_BTN_DESTINATION_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.show_command( nc.open_parcel )
    
    
    @exqtSlot()
    def on_BTN_FILENAME_clicked( self ) -> None:
        """
        Signal handler:
        """
        if qt_gui_helper.browse_open_on_textbox( self.ui.CMB_FILENAME ):
            self.handle_update_filename()
    
    
    def handle_update_filename( self ):
        cfn = self.ui.CMB_FILENAME.currentText()
        
        if file_helper.get_extension( cfn ) == ".tsv":
            self.ui.CMB_DELIMITER.setCurrentText( "TAB" )
        elif file_helper.get_extension( cfn ) == ".csv":
            self.ui.CMB_DELIMITER.setCurrentText( "," )
    
    
    @exqtSlot()
    def on_BTN_REMOVE_ENTITY_clicked( self ) -> None:
        """
        Signal handler:
        """
        if self.ui.LST_ENTITIES.topLevelItemCount() == 1:
            return
        
        tree_helper.remove_selected( self.ui.LST_ENTITIES )
    
    
    @exqtSlot()
    def on_BTN_REFRESH_DESTINATION_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.__update_destinations()
    
    
    @exqtSlot()
    def on_BTN_ADD_EDGE_clicked( self ) -> None:
        """
        Signal handler:
        """
        ent = self.get_selected_entity()
        
        if ent is None:
            return
        
        self.ent_to_list( _Entity( ent.is_edge, ent.label, ent.start_label, ent.end_label ) )


class _Entity( nc.NcvEntitySpec ):
    """
    Entity definition on the import CSV form.
    """
    
    
    @property
    def is_valid( self ):
        try:
            self.validate()
        except:
            return False
        else:
            return True
    
    
    def validate( self ):
        if not self.label:
            raise ValueError( "Missing label" )
        
        if self.is_edge:
            if not self.start_label:
                raise ValueError( "Missing start label" )
            
            if not self.end_label:
                raise ValueError( "Missing end label" )


class _Field:
    """
    Field definition on the import CSV form.
    """
    
    
    def __init__( self, index, column, entity: Optional[_Entity], field: nc.NcvHeader, sample: str ):
        self.index = index
        self.column = column
        self.entity = entity
        self.field = field
        self.sample = sample
    
    
    def validate( self ):
        if not self.entity:
            return
        
        if self.field.special != nc.ENcvSpecial.NONE:
            return
        
        if not self.field.name:
            raise ValueError( "Missing field name" )
        
        if not self.field.type:
            raise ValueError( "Missing field type" )
    
    
    def to_import_csv( self ):
        if self.entity is None:
            return ""
        else:
            return "{}.{}".format( self.entity.label, self.field.decorated_name( self.entity ) )