import intermake
from mhelper import EFileMode, isFilename, array_helper
import neocommand
import csv
from typing import Dict, List, Optional, Union

from bio42.application import app

TReadCsvFilename = isFilename[EFileMode.READ, ".csv"]
TColId = Union[str, int]


class _HMap:
    def __init__( self, index, text ):
        """
        :param index:   Header index 
        :param text:    Text of the form `'entity.header'` OR `''` to ignore the column. 
        """
        self.index: int = index
        
        if text:
            a, b = text.split( ".", 1 )
            self.entity_str = a
            self.header: neocommand.NcvHeader = neocommand.NcvHeader.from_decorated_name( None, b )
        else:
            self.entity_str = None
            self.header: neocommand.NcvHeader = None
        
        self.entity: _HEnt = None


class _HEnt:
    def __init__( self, label ):
        self.label = label
        self.is_edge: bool = None
        self.uid_col: _HMap = None
        self.start_col: _HMap = None
        self.end_col: _HMap = None
        self.start_label = None
        self.end_label = None
        self.schema = None
        
        self.cur_props: Dict[str, object] = { }
        self.cur_uid: str = None
        self.cur_start: str = None
        self.cur_end: str = None


@app.command( folder = "import" )
def import_csv( file_name: TReadCsvFilename,
                destination: neocommand.Destination,
                headers: bool = True,
                fields: Optional[List[str]] = None,
                mapping: Optional[Dict[Union[int, str], str]] = None,
                delimiter = ",",
                array_delimiter = "¶",
                preview: bool = False ):
    """
    Imports specified data from a CSV file.
        
    :param preview:                 Previews the import headers but doesn't do anything.
    :param file_name:               File to import. 
    :param destination:             Where to send the data to.
    :param headers:                 File has headers?
                                    Headers should be of the form:
                                        `label.property`
                                    Where `property` is a valid Neo4j identifier such as `spam:int` `uid:ID` (see 
                                    `from_decorated_name`).
                                    Empty headers are permitted and indicate that that column is ignored.
                                    Whether `label` denotes a node or edge label is inferred from the properties.
    :param fields:                  Overrides the file headers.
                                    Mandatory if the file has no headers OR if the headers are not in the correct format. 
    :param mapping:                     Alternative to `fields` that specifies headers as key-value pairs.
                                    `key` = the name of the old header, or `#` followed by the zero based index of the header.
                                    `value` = the new header 
    :param delimiter:               CSV delimiter 
    :param array_delimiter:         Array delimiter 
    :return:                        The `endpoint` 
    """
    with open( file_name, "r" ) as i:
        csv_reader = csv.reader( i, delimiter = delimiter )
        maps_in: List[_HMap] = []
        
        # Read the headers, if available
        if headers:
            header_row: List[str] = [cell.strip() for cell in next( csv_reader )]
        else:
            header_row = None
        
        # Convert `fields` to `map`
        if fields is not None:
            mapping = { i: v for i, v in enumerate( fields ) }
        
        # Convert `map` or `header_row` to an `_HMap` array.
        # The `_HMap` constructor parses the actual text.
        if mapping is not None:
            for key, value in mapping.items():
                if isinstance( key, int ):
                    index = key
                elif key.startswith( "#" ):
                    index = int( key[1:] )
                elif header_row is not None:
                    index = header_row.index( key )
                else:
                    raise ValueError( "Cannot specify headers by name when `headers` is `False`." )
                
                maps_in.append( _HMap( index, value ) )
        elif header_row is not None:
            for index, header in enumerate( header_row ):
                maps_in.append( _HMap( index, header ) )
        else:
            raise ValueError( "Must provide `headers`, `fields` or `map`." )
        
        # Sort our `_HMap` array by index and make a note of the entities
        maps: List[_HMap] = []
        entities: Dict[str, _HEnt] = { }
        
        for mapping in maps_in:
            # Discard empty mappings
            if mapping.entity_str is None:
                continue
            
            array_helper.ensure_capacity( maps, index = mapping.index )
            maps[mapping.index] = mapping
            
            ent = entities.get( mapping.entity_str )
            
            if ent is None:
                ent = _HEnt( mapping.entity_str )
                entities[mapping.entity_str] = ent
            
            mapping.entity = ent
            
            if mapping.header.special == neocommand.ENcvSpecial.UID:
                ent.is_edge = False
                ent.uid_col = mapping
            
            if mapping.header.special == neocommand.ENcvSpecial.START:
                ent.is_edge = True
                ent.start_col = mapping
                ent.start_label = mapping.header.type_label
            
            if mapping.header.special == neocommand.ENcvSpecial.END:
                ent.is_edge = True
                ent.end_col = mapping
                ent.end_label = mapping.header.type_label
        
        for ent in entities.values():
            if ent.is_edge:
                assert ent.start_label
                assert ent.label
                assert ent.end_label
                ent.schema = neocommand.get_core().schema.edge_schema.create( ent.start_label, ent.label, ent.end_label )
            else:
                assert not ent.start_label
                assert ent.label
                assert not ent.end_label
                ent.schema = neocommand.get_core().schema.node_schema.create( ent.label )
        
        if preview:
            for index, mapping in enumerate( maps ):
                if mapping is None:
                    print( "COLUMN {} = -".format( index ) )
                else:
                    print( "COLUMN {} = {}".format( index, mapping.entity, mapping.header ) )
            
            for ent in entities:
                if ent.is_edge:
                    print( "EDGE: {}--{}->{} ({}->{})".format( ent.start_col.header.type_label, ent.label, ent.end_col.header.type_label, ent.start_col.index, ent.end_col.index ) )
                else:
                    print( "NODE: {} ({})".format( ent.label, ent.uid_col ) )
            
            return destination
        
        # Iterate our rows
        with destination.open_writer() as dst:
            for row in intermake.pr.pr_iterate( csv_reader, "Iterating rows" ):
                for ent in entities.values():
                    ent.cur_props.clear()
                    ent.cur_start = None
                    ent.cur_end = None
                    ent.cur_uid = None
                
                for index, cell in enumerate( row ):
                    cell = cell.strip()
                    mapping: _HMap = maps[index]
                    
                    if mapping is None:
                        continue
                    
                    ent: _HEnt = mapping.entity
                    
                    if mapping.header.special == neocommand.ENcvSpecial.UID:
                        ent.cur_uid = cell
                    elif mapping.header.special == neocommand.ENcvSpecial.START:
                        ent.cur_start = cell
                    elif mapping.header.special == neocommand.ENcvSpecial.END:
                        ent.cur_end = cell
                    elif mapping.header.type.is_array:
                        ent.cur_props[mapping.header.name] = (mapping.header.type.element_type( x ) for x in cell.split( array_delimiter ))
                    else:
                        ent.cur_props[mapping.header.name] = mapping.header.type.element_type( cell )
                
                for ent in entities.values():
                    if ent.is_edge:
                        dst.create_edge( label = ent.schema,
                                         start_uid = ent.cur_start,
                                         end_uid = ent.cur_end,
                                         properties = ent.cur_props )
                    else:
                        dst.create_node( label = ent.schema,
                                         uid = ent.cur_uid,
                                         properties = ent.cur_props )
    
    return destination


def __read_properties( row: List[str], indices: List[int], names: Optional[List[str]], headers: Optional[List[str]] ):
    r = { }
    
    for order, index in enumerate( indices ):
        if names is not None:
            name = names[order]
        elif headers is not None:
            name = headers[index]
        else:
            raise ValueError( "To get the column name I need either a `name` or `header`, but I have neither." )
        
        r[name] = row[index]
    
    return r
