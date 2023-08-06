"""
Functions for applying annotations from the Uniprot online service.
"""
from typing import Optional
from mhelper import BatchList, SwitchError, MFlags
import neocommand
import intermake

from bio42.application import app
from bio42 import schema


@app.command( folder = "import" )
def download_accessions( endpoint: neocommand.Destination,
                         origin: neocommand.Origin,
                         input_type: str,
                         output_type: str = "ACC",
                         input_property: neocommand.isNodeProperty[schema.Sequence] = "uid",
                         input_column: Optional[int] = None,
                         output_property: neocommand.isNodeProperty[schema.Sequence] = "uniprot",
                         batch_size: int = 100 ) -> neocommand.Destination:
    """
    Uses UniProt to adds or replace accessions on gene Sequences.
    
    :param origin:              From where to retrieve the Sequences to update
    :param endpoint:            Where to send the new accessions to
    :param input_type:          Type of the input accession.
                                See http://www.uniprot.org/help/programmatic_access#id_mapping_examples
    :param output_type:         Type of the output accession.
    :param input_property:      Property to retrieve the input accession from.
                                For instance, `uid` or `accession`. 
    :param input_column:        Column of the input accession.
                                This only applies to pipe-delimited `input_property`s of the form `a|b|c`. 
    :param output_property:     Property to store the output accession into.
                                For instance, `uid` or `accession`.
    :param batch_size:          Number of requests to make to Uniprot at once. 
    :return:                    `endpoint` 
    """
    from urllib.parse import urlencode
    from urllib.request import Request
    from urllib.request import urlopen
    
    URL = "http://www.uniprot.org/uploadlists/"
    
    with origin.open_reader() as reader:
        to_do = reader.read_all_props( schema.Sequence.label, input_property )
        
    to_do = BatchList( to_do, batch_size )
    
    with endpoint.open_writer() as ep:
        with intermake.pr.pr_action( "Processing sequences", len( to_do ) ) as action:
            for next_portion in to_do:
                action.increment( len( next_portion ) )
                
                next_dict = { }
                
                for sequence_uid, property_value in next_portion:
                    if input_column is not None:
                        property_value = property_value.split( "|" )[input_column]
                    
                    next_dict[property_value] = sequence_uid
                
                data = urlencode( {
                    "from"  : input_type,
                    "to"    : output_type,
                    "format": "tab",
                    "query" : " ".join( next_dict.keys() )
                } )
                
                data = data.encode( 'ascii' )
                
                request = Request( URL, data )
                
                response = urlopen( request )
                tsv = response.read( 200000 ).decode( "utf-8" )
                
                lines = tsv.split( "\n" )[1:]  # first line just says "From-To"
                
                for line in lines:
                    accession_from, accession_to = line.split( "\t", 1 )
                    sequence_uid = next_dict[accession_from]  # type: str
                    
                    ep.create_node( label = schema.Sequence.label,
                                    uid = sequence_uid,
                                    properties = { output_property: accession_to } )
    
    return endpoint


class EAutoAnnotateMode( MFlags ):
    KEGG = 1
    GO = 2
    PFAM = 4


@app.command( folder = "import" )
def download_annotations( endpoint: neocommand.Destination,
                          origin: neocommand.Origin,
                          accession_property: str = "uniprot",
                          batch_size: int = 100,
                          create_edges: bool = True,
                          create_properties: bool = False,
                          create_nodes: bool = True,
                          property_prefix: str = "uniprot_",
                          modes: Optional[EAutoAnnotateMode] = None ):
    """
    Annotates sequences using Uniprot.
    Supports: PFAM, GO, KEGG.
    
    :param modes:                   What to apply. If not specified defaults to everything.
    :param create_properties:       Create properties for metadata. 
    :param create_edges:            Create edges for metadata.
    :param create_nodes:            Create nodes for metadata (requires `create_edges`).
    :param endpoint:                Where to send the results to
    :param origin:                  Where to get the sequences from
    :param accession_property:      Property to get the Uniprot accession from (on the `origin` sequences)
    :param batch_size:              Number of sequences to process at once. Note that Uniprot may also impose its own batching.
    :param property_prefix:         Prefix to add to the resultant properties (added to the `origin` sequences)
    :return:                        The `endpoint` argument.
    """
    import uniprot
    
    SEQUENCE_LABEL = schema.Sequence.label
    
    with origin.open_reader() as reader:
        to_do = reader.read_all_props( SEQUENCE_LABEL, accession_property )
    
    to_do = BatchList( to_do, batch_size )
    
    interesting = []
    
    if modes is None:
        modes = EAutoAnnotateMode.PFAM | EAutoAnnotateMode.GO | EAutoAnnotateMode.KEGG
    
    # noinspection PyTypeChecker
    for mode in modes:
        if mode.GO:
            interesting.append( ("go", schema.Go.label) )
        elif mode.PFAM:
            interesting.append( ("pfam", schema.Pfam.label) )
        elif mode.KEGG:
            interesting.append( ("kegg", schema.Kegg.label) )
        else:
            raise SwitchError( "modes[n]", mode )
    
    with endpoint.open_writer() as writer:
        with intermake.pr.pr_action( "Iterating sequences", len( to_do ) ) as action:
            for batch in to_do:
                action.increment( len( batch ) )
                accession_to_uid = dict( (v, k) for k, v in batch )
                
                sequence_id_string = " ".join( [x[1] for x in batch] )
                uniprot_data = uniprot.batch_uniprot_metadata( sequence_id_string, 'cache' )
                
                assert uniprot_data
                
                for sequence_accession, sequence_metadata in uniprot_data.items():
                    sequence_uid = accession_to_uid[sequence_accession]
                    
                    new_dict = { }
                    
                    for attribute, class_ in interesting:
                        if attribute in sequence_metadata:
                            value = sequence_metadata[attribute]
                            value = [x.split( ";", 1 )[0].strip() for x in value]
                            new_dict[property_prefix + attribute] = value
                            
                            if create_edges:
                                for mode in value:
                                    x_uid = mode
                                    
                                    if create_nodes:
                                        writer.create_node( label = class_, uid = x_uid, properties = { } )
                                    
                                    writer.create_edge( label = schema.GoClassContainsSequence,
                                                          start_uid = x_uid,
                                                          end_uid = sequence_uid,
                                                          properties = { } )
                    
                    if create_properties:
                        writer.create_node( label = SEQUENCE_LABEL, uid = sequence_uid, properties = new_dict )
    
    return endpoint
