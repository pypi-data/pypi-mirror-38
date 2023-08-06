import csv
from typing import Dict, List, Optional
import intermake
from mhelper import EFileMode, isFilename
import neocommand

from bio42.application import app
from bio42 import schema as b42schema


_EXT_CSV = ".csv"
_EXT_TSV = ".tsv"


@app.command( folder = "import" )
def import_annotations( destination: neocommand.Destination,
                        file_name: isFilename[EFileMode.READ, _EXT_CSV, _EXT_TSV],
                        create_classes: bool = False,
                        viable_columns: Optional[List[str]] = None,
                        name_delimiter: str = "|",
                        uid_delimiter: str = "|",
                        pad: bool = False
                        ) -> None:
    """
    Imports gene annotations from a CSV or TSV file.
    
    The following columns of the source file are used.

    =============== ===========================================================
    Column          Meaning    
    =============== ===========================================================
    uid             the accession of the gene sequence
    xxx             a column containing accession(s) of the annotation terms.
                    The column must be named after a valid annotation label.
                    
                    * A node schema must exist defining nodes with this label
                    * An edge schema must exist defining edges from nodes with
                      this label to nodes with the 'Sequence' label. The label
                      of the edges themselves are ignored.
                    
                    Valid inbuilt values include `Go`, `Pfam`, `Ipr` and `Kegg`.
    xxx.name        a column containing the name(s) of the annotation terms
                    These columns are optional, and are only used if the
                    `create_classes` argument is passed.  
    =============== ===========================================================
    
    All columns must be valid, though columns can be ignored by passing the
    `viable_columns` argument.
    
    :param destination:        Where to send the parsed data to. 
    :param file_name:       File to read in.
    :param create_classes:  Whether to create the annotation classes.
    :param viable_columns:  Which columns to accept.
                            If not specified then all columns are assumed.
                            The `uid` column is implicit and need not be specified.
    :param name_delimiter:  Delimiter for multiple annotation UIDs in the same column.
    :param uid_delimiter:   Delimiter for multiple annotation names in the same column.
                            This is only used if `create_classes` is set.
    :param pad:             When set, missing columns are treated as empty.
                            This allows jagged input to be imported without error.
    """
    NAME_KEY_SUFFIX = ".name"
    schema = neocommand.get_core().schema
    gene_node_schema = b42schema.Sequence
    
    #
    # Determine the input delimiter
    #
    if file_name.endswith( ".csv" ):
        delimiter = ","
    elif file_name.endswith( ".tsv" ):
        delimiter = "\t"
    else:
        raise ValueError( "File must end with <.csv> or <.tsv> but «{0}» does not.".format( file_name ) )
    
    #
    # Open the destination for writing
    #
    with destination.open_writer() as writer:
        #
        # Open the source for reading
        #
        with open( file_name, "r" ) as file_in:
            reader = csv.reader( file_in, delimiter = delimiter )
            
            #
            # Map out the column headers
            #
            col_names = next( reader )
            
            col_anno_indices: Dict[str, int] = { }  # ------------------------- Maps normal column names to their indices
            col_anno_edge_schema: Dict[str, neocommand.EdgeSchema] = { }  # --- Maps normal column names to their edge schema 
            col_anno_node_schema: Dict[str, neocommand.NodeSchema] = { }  # --- Maps normal column names to their node schema
            col_gene_id: int = None  # ---------------------------------------- Maps the special UID column to its index
            col_anno_names: Dict[str, int] = { }  # --------------------------- Maps normal column names to indices of their counterpart name columns (these have the same name but ending ".name")
            
            for i, col_name in enumerate( col_names ):
                if col_name == "uid":
                    col_gene_id = i
                else:
                    if viable_columns is not None and col_name not in viable_columns:
                        continue
                    
                    if col_name.endswith( NAME_KEY_SUFFIX ):
                        col_anno_names[col_name[:len( NAME_KEY_SUFFIX )]] = i
                    else:
                        col_anno_indices[col_name] = i
                        
                        for anno_node_schema in schema.node_schema:
                            if col_name == anno_node_schema.label:
                                col_anno_node_schema[col_name] = anno_node_schema
                                
                                for edge_schema in schema.edge_schema:
                                    if edge_schema.start_label == anno_node_schema and edge_schema.end_label == gene_node_schema:
                                        col_anno_edge_schema[col_name] = edge_schema
                                        break
                                else:
                                    raise ValueError( "Cannot read the file «{}» because the «{}» "
                                                      "column is not named after a valid schema: "
                                                      "there is no defined schema for edges from «{}» to «{}».".format( file_name, col_name, anno_node_schema, gene_node_schema ) )
                        
                        else:
                            raise ValueError( "Cannot read the file «{}» because the «{}» "
                                              "column is not named after a valid schema: "
                                              "there is no defined schema for nodes named «{}».".format( file_name, col_name, col_name ) )
            
            #
            # Check the headers are valid
            #
            
            # each `col_class_name` should have an associated `col_index`
            for key in col_anno_names:
                if key not in col_anno_indices:
                    raise ValueError( "Cannot read the file «{0}» because whilst there is a <.name> column for «{1}» (<{1}.name>), there is no UID column («{1}»). The columns present are «{2}».".format( file_name, key, col_names ) )
            
            # There must be a UID column
            if col_gene_id is None:
                raise ValueError( "Cannot read the file «{0}» because none of the mandatory <uid> column does not exist. The columns present are «{1}».".format( file_name, col_names ) )
            
            # There must be at least one annotation column
            if not col_anno_indices:
                raise ValueError( "Cannot read the file «{0}» because it doesn't contain any other accepted columns. The columns present are «{1}».".format( file_name, col_names ) )
            
            #
            # Display the mapping to the user
            #
            anno_names: Dict[str, Dict[str, str]] = { }  # Maps column names to dictionaries mapping annotation UIDs to names
            
            for col_name, col_index in col_anno_indices.items():
                name = col_anno_names.get( col_name )
                anno_names[col_name] = { }
                
                if name is not None:
                    print( "«{}» in column «{}» with name in column «{}».".format( col_name, col_index, name ) )
                else:
                    print( "«{}» in column «{}».".format( col_name, col_index ) )
            
            #
            # Create the actual edges
            #
            for i, row in intermake.pr.pr_enumerate( reader, "Creating edges" ):
                gene_uid = row[col_gene_id]
                
                for col_name, col_index in col_anno_indices.items():
                    annotation_class_name = col_anno_names.get( col_name )
                    col_edge = col_anno_edge_schema.get( col_name )
                    
                    __apply_annotation( writer = writer,
                                        gene_uid = gene_uid,
                                        row = row,
                                        anno_names = anno_names[col_name],
                                        col_anno_uid = col_index,
                                        col_anno_name = annotation_class_name,
                                        anno_edge_label = col_edge,
                                        anno_name_delimiter = name_delimiter,
                                        anno_uid_delimiter = uid_delimiter,
                                        pad = pad )
            
            #
            # Create the classes
            #
            if create_classes:
                for col_name, name_dict in anno_names.items():
                    with intermake.pr.pr_action( "Creating «{}» nodes".format( col_name ), len( name_dict ) ) as action:
                        for anno_uid, anno_name in name_dict.items():
                            if name:
                                data = { "name": name }
                            else:
                                data = { }
                            
                            action.increment()
                            writer.create_node( label = col_name,
                                                uid = anno_uid,
                                                properties = data )


def __apply_annotation( writer: neocommand.Writer,
                        gene_uid: str,
                        row: List[str],
                        anno_names: Dict[str, Optional[str]],
                        col_anno_uid: int,
                        col_anno_name: Optional[int],
                        anno_edge_label: neocommand.EdgeSchema,
                        anno_name_delimiter,
                        anno_uid_delimiter,
                        pad ) -> None:
    """
    Adds an edge from a column.
    
    :param writer:                      Where to send edges to.
    :param gene_uid:                    UID of the gene.
    :param row:                         Contents of the CSV row.
    :param anno_names:                  Receives annotation UIDs and names.
    :param col_anno_uid:                Index of column containing the annotation UID(s).
    :param col_anno_name:               Index of column containing the annotation name(s)
    :param anno_edge_label:             Label to give the created edges. 
    :param anno_name_delimiter:         Used to split `col_annotation_name`.
    :param anno_uid_delimiter:          Used to split `col_annotation_uid`
    :param pad:                         Whether to ignore the case when columns are missing.
    """
    if col_anno_uid < 0 or col_anno_uid >= len( row ):
        if pad:
            return
        raise KeyError( "Row does not have column «{}», which is specified as the UID, and the <pad> argument is <False>: «{}».".format( col_anno_uid, row ) )
    
    uid_text = row[col_anno_uid]
    
    if col_anno_name is None:
        name_texts = None
    else:
        name_text = row[col_anno_name]
        name_texts = name_text.split( anno_name_delimiter )
    
    for i, row_text in enumerate( uid_text.split( anno_uid_delimiter ) ):
        if row_text:
            uid = row_text
            
            if name_texts is not None:
                name = name_texts[i]
            else:
                name = None
            
            anno_names[uid] = name
            
            writer.create_edge( label = anno_edge_label,
                                start_uid = uid,
                                end_uid = gene_uid,
                                properties = { } )
