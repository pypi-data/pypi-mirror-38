"""
Imports taxa

Normally the taxa are downloaded as a set of DMP files, these will need to be renamed so we can tell the difference between them
Specifically we want NODES.DMP and NAMES.DMP
"""
import os.path
import intermake
import neocommand
from typing import Dict, List
from mhelper import file_helper, isFilename, EFileMode, isOptional

from bio42 import schema
from bio42.application import app

UID_TAXON_UNKNOWN = "unknown"
_EXT_DMP = ".dmp"


@app.command( folder = "import" )
def import_taxonomy( endpoint: neocommand.Destination,
                     file_name: isOptional[isFilename[EFileMode.READ, _EXT_DMP]],
                     names_file_name: isOptional[isFilename[EFileMode.READ, _EXT_DMP]] ) -> None:
    """
    Imports the taxonomy database.
    
    :param endpoint:            Where to send the parsed data to. 
    :param file_name:           Where to get the data from.
                                This should be an NCBI taxonomy database, e.g. `taxa.dmp` 
    :param names_file_name:     Names file.
                                This should be an NCBI taxonomy database, e.g. `names.dmp`
                                If left blank this parameter assumes a file called `names.dmp` in the same directory as `file_name`. 
    :return: 
    """
    #
    # Try and find the names file
    #
    if not names_file_name:
        tax_file_names = [file_helper.replace_filename( file_name, "names.dmp" ), file_helper.replace_extension( file_name, ".names" )]
        for possibility in tax_file_names:
            if os.path.isfile( possibility ):
                names_file_name = possibility
                break
    
    print( "Reading taxonomy from «{}» and «{}».".format( file_name, names_file_name ) )
    
    tax_names = _read_names( names_file_name )
    
    # Always create an unknown
    with endpoint.open_writer() as writer:
        _create_unknown_taxon_node( writer )
        
        with intermake.pr.pr_action( "Iterating nodes" ) as action:
            with open( file_name, "r" ) as file:
                for line in file:
                    action.increment()
                    __yield_line( writer, line, tax_names )


def __yield_line( writer: neocommand.Writer, line: str, tax_names: Dict[int, Dict[str, List[str]]] ) -> None:
    # 00 tax_id                            -- node id in GenBank taxonomy database
    # 01 parent tax_id                     -- parent node id in GenBank taxonomy database
    # 02 rank                              -- rank of this node (superkingdom, kingdom, ...)
    # 03 embl code#                        -- locus-name prefix; not unique
    # 04 division id                       -- see division.dmp file
    # 05 inherited div flag  (1 or 0)      -- 1 if node inherits division from parent
    # 06 genetic code id                   -- see gencode.dmp file
    # 07 inherited GC  flag  (1 or 0)      -- 1 if node inherits genetic code from parent
    # 08 mitochondrial genetic code id     -- see gencode.dmp file
    # 09 inherited MGC flag  (1 or 0)      -- 1 if node inherits mitochondrial gencode from parent
    # 10 GenBank hidden flag (1 or 0)      -- 1 if  name is suppressed in GenBank entry lineage
    # 11 hidden subtree root flag (1 or 0) -- 1 if this subtree has no sequence data yet
    # 12 comments                          -- free-text comments and citations
    
    fields = [x.strip( " \t|\n" ) for x in line.split( "\t|\t" )]
    
    if len( fields ) != 13:
        raise ValueError( "This is not a taxonomy node database." )
    
    # super( ).__init__( fields[ 0 ] )
    
    name = fields[0]
    my_id = int( fields[0] )
    applicable_names = tax_names[my_id]
    
    # Each value of applicable_names is
    # 00 id
    # 01 name
    # 02 unique name
    # 03 class
    if "scientific_name" in applicable_names:
        scientific_name = applicable_names["scientific_name"][0]
    else:
        scientific_name = None
    
    parent_id = int( fields[1] )
    
    props = {
        "parent_id"                    : parent_id,
        "rank"                         : fields[2],  # don't short-code this any more since its reasonably useful
        "embl_code"                    : fields[3],  # letters
        "division_id"                  : int( fields[4] ),
        "inherited_div_flag"           : _str_to_bool( fields[5] ),
        "genetic_code_id"              : int( fields[6] ),
        "inherited_gc_flag"            : _str_to_bool( fields[7] ),
        "mitochondrial_genetic_code_id": int( fields[8] ),
        "inherited_mgc_flag"           : _str_to_bool( fields[9] ),
        "genbank_hidden_flag"          : _str_to_bool( fields[10] ),
        "hidden_subtree_root_flag"     : _str_to_bool( fields[11] ),
        "comments"                     : fields[12],
        "acronym"                      : read_name( applicable_names, "acronym" ),
        "anamorph"                     : read_name( applicable_names, "anamorph" ),
        "authority"                    : read_name( applicable_names, "authority" ),
        "blast_name"                   : read_name( applicable_names, "blast_name" ),
        "common_name"                  : read_name( applicable_names, "common_name" ),
        "equivalent_name"              : read_name( applicable_names, "equivalent_name" ),
        "genbank_acronym"              : read_name( applicable_names, "genbank_acronym" ),
        "genbank_anamorph"             : read_name( applicable_names, "genbank_anamorph" ),
        "genbank_common_name"          : read_name( applicable_names, "genbank_common_name" ),
        "genbank_synonym"              : read_name( applicable_names, "genbank_synonym" ),
        "in_part"                      : read_name( applicable_names, "in_part" ),
        "includes"                     : read_name( applicable_names, "includes" ),
        "misnomer"                     : read_name( applicable_names, "misnomer" ),
        "misspelling"                  : read_name( applicable_names, "misspelling" ),
        "scientific_name"              : scientific_name,
        "scientific_names"             : read_name( applicable_names, "scientific_name" ),
        "synonym"                      : read_name( applicable_names, "synonym" ),
        "teleomorph"                   : read_name( applicable_names, "teleomorph" ),
        "type_material"                : read_name( applicable_names, "type_material" ) }
    
    writer.create_node( label = schema.Taxon,
                        uid = name,
                        properties = props )
    
    writer.create_edge( label = schema.TaxonContainsTaxon,
                        start_uid = str( parent_id ),
                        end_uid = name, properties = { } )


def read_name( dictionary, type_ ):
    if type_ not in dictionary:
        return ""
    
    names = dictionary[type_]
    
    return ", ".join( names )


def _create_unknown_taxon_node( writer: neocommand.Writer ) -> None:
    props = {
        "parent_id"                    : -1,
        "rank"                         : "",
        "embl_code"                    : "",
        "division_id"                  : -1,
        "inherited_div_flag"           : False,
        "genetic_code_id"              : -1,
        "inherited_gc_flag"            : False,
        "mitochondrial_genetic_code_id": -1,
        "inherited_mgc_flag"           : False,
        "genbank_hidden_flag"          : False,
        "hidden_subtree_root_flag"     : False,
        "comments"                     : "Unknown signifier automatically generated by " + intermake.Controller.ACTIVE.app.name + " " + intermake.Controller.ACTIVE.app.version,
        "acronym"                      : "",
        "anamorph"                     : "",
        "authority"                    : "",
        "blast_name"                   : "",
        "common_name"                  : "unknown",
        "equivalent_name"              : "",
        "genbank_acronym"              : "",
        "genbank_anamorph"             : "",
        "genbank_common_name"          : "",
        "genbank_synonym"              : "",
        "in_part"                      : "",
        "includes"                     : "",
        "misnomer"                     : "",
        "misspelling"                  : "",
        "scientific_name"              : "unknown",
        "synonym"                      : "",
        "teleomorph"                   : "",
        "type_material"                : "" }
    
    writer.create_node( label = schema.Taxon,
                        uid = UID_TAXON_UNKNOWN,
                        properties = props )


def _read_names( file_name ) -> Dict[str, Dict[int, List[str]]]:
    """
    Reads a taxonomy names file.
    :param file_name: File to read 
    :return: Dictionary:
                K: Taxon ID
                V: Dictionary:
                    K: Name type (e.g. "scientific_name")
                    V: LIST:
                        V: Name
    """
    assert file_name, "A taxonomy names file must be specified."
    
    result_names: Dict[str, Dict[int, List[str]]] = { }
    
    with intermake.pr.pr_action( "Reading names" ) as action:
        with open( file_name, "r" ) as file:
            for line in file:
                action.increment()
                fields = [x.strip( " \t|\n" ) for x in line.split( "\t|\t" )]
                id = int( fields[0] )
                
                name = fields[1]
                name_type = fields[3].replace( " ", "_" ).replace( "-", "_" )
                
                if id in result_names:
                    dict_for_id = result_names[id]
                else:
                    dict_for_id = { }
                    result_names[id] = dict_for_id
                
                if name_type in dict_for_id:
                    names_for_class = dict_for_id[name_type]
                else:
                    names_for_class = []
                    dict_for_id[name_type] = names_for_class
                
                names_for_class.append( name )
    
    return result_names


def _read_scientific_names( file_name ) -> Dict[int, str]:
    names = _read_names( file_name )
    result: Dict[int, str] = { }
    
    for k, v in names.items():
        scientific_names = v.get( "scientific_name" )
        
        if scientific_names:
            scientific_name = scientific_names[0]
            result[k] = scientific_name
    
    return result


def _str_to_bool( text: str ) -> bool:
    """
    Converts the text to a boolean value.
    """
    if text == "0":
        return False
    elif text == "1":
        return True
    else:
        raise ValueError( "Cannot convert text \"" + text + "\" to bool." )
