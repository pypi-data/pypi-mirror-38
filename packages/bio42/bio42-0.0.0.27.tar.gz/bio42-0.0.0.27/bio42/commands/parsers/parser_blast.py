"""
Contains the BLAST to $(APP_DISPLAY_NAME) importer/parser.
"""
from typing import Dict, List, Optional, Tuple
from uuid import uuid4

from bio42.application import app
from bio42 import schema

import intermake
from mhelper import EFileMode, isFilename, isOptional
import neocommand


__author__ = "Martin Rusilowicz"

_SPC_NONE_ = -1
_SPC_QUERY_UID = 0
_SPC_SUBJECT_UID = 1
_SPC_QUERY_START = 2
_SPC_QUERY_END = 3
_SPC_SUBJECT_START = 4
_SPC_SUBJECT_END = 5
_SPC_COUNT_ = 6

_EXT_DICTIONARY = ".dict"
_EXT_BLAST = ".blast"
_EXT_TSV = ".tsv"


@app.command(folder="import")
def import_blast( file_name: isFilename[EFileMode.READ, _EXT_BLAST, _EXT_TSV],
                  destination: neocommand.Destination,
                  column_names: Optional[List[str]] = None,
                  dictionary_file_name: isOptional[isFilename[EFileMode.READ, _EXT_DICTIONARY, _EXT_TSV]] = None,
                  dictionary_uid_column: int = -1,
                  deep_query: bool = False
                  ) -> None:
    """
    Imports BLAST data as edges and/or nodes in the graph.
    
    :param destination: Where to send the parsed data to.
    :param file_name: File to read from.
    :param column_names: Mapping of the columns in the TSV file. See the BLAST+ documentation, or see the `BLAST Columns` help topic for quick reference.
    :param dictionary_file_name: Dictionary of names (TSV file giving Original_name and BLAST_name for each line).
    :param dictionary_uid_column: When using the dictionary, if not '-1' this specifies that the original names are '|' delimited FASTA accessions and this column should be taken as the UID.
    :param deep_query: When `True`, additional nodes and edges will be created: Subsequence, Query
    """
    with destination.open_writer() as writer:
        if dictionary_uid_column != -1:
            print( "Taking the nth element where n = {} as the UID column.".format( dictionary_uid_column ) )
        
        if deep_query:
            print( "Deep query is {},".format( "ON" if deep_query else "OFF" ) )
        
        if dictionary_file_name:
            uid_dictionary = { }
            
            with intermake.pr.pr_action( "Iterating dictionary file" ) as action:
                with open( dictionary_file_name, "r" ) as dictionary_file:
                    for line in dictionary_file:
                        action.increment()
                        if line:
                            elements = line.split( "\t" )
                            
                            original_name = elements[0].strip()
                            blast_name = elements[1].strip()
                            
                            if dictionary_uid_column != -1:
                                original_name = original_name.split( "|" )[dictionary_uid_column]
                            
                            uid_dictionary[blast_name] = original_name
        else:
            uid_dictionary = None
        
        if not column_names:
            column_names = ["std"]
        
        if len( column_names ) == 1:
            column_names = BLASTAUTOMAP[column_names[0]][1]
        
        column_mapping = []
        db_names = set()
        
        for i, column_name in enumerate( column_names ):
            mapping = BLASTMAP[column_name]
            db_name = mapping[0]
            
            if db_name in db_names:
                raise ValueError( "Column mapping specifies «{}» twice.".format( db_name ) )
            
            db_names.add( db_name )
            
            column_mapping.append( mapping )
        
        print( "Column names are:\n* {}".format( "\n* ".join( x[1] for x in column_mapping ) ) )
        
        with intermake.pr.pr_action( "Iterating BLAST file" ) as action:
            with open( file_name, "r" ) as file:
                for line in file:
                    action.increment()
                    __yield_line( writer, line, file_name, column_mapping, uid_dictionary, deep_query )


# noinspection PyUnusedLocal
def __yield_line( endpoint: neocommand.Writer, tsv_line: str, file_name: str, column_mapping: List[Tuple[str, str, type]], uid_dictionary: Dict[str, str], deep_query: bool ) -> None:
    e = tsv_line.split( "\t" )
    
    properties = { }
    specials = [None] * _SPC_COUNT_  # type: List[str]
    
    for i, element in enumerate( e ):
        mapping = column_mapping[i]
        
        name = mapping[1]
        
        try:
            value = mapping[2]( element )
        except Exception as ex:
            raise ValueError( "Failed to convert «{}» («{}») to «{}»".format( element, name, mapping[2].__name__ ) ) from ex
        
        special = mapping[3]
        
        properties[name] = value
        
        if special != _SPC_NONE_:
            specials[special] = value
    
    if any( x is None for x in specials ):
        raise ValueError( "Missing a mandatory column." )
    
    query_uid = specials[_SPC_QUERY_UID]  # TODO: Used to have truncate_id here, still need
    subject_uid = specials[_SPC_SUBJECT_UID]
    
    if uid_dictionary is not None:
        query_uid = uid_dictionary[query_uid]
        subject_uid = uid_dictionary[subject_uid]
    
    # Fields: query acc., subject acc., % identity, alignment length, mismatches, gap opens, q. start, q. end, s. start, s. end, e-value, bit score
    query_start = specials[_SPC_QUERY_START]
    query_end = specials[_SPC_QUERY_END]
    subject_start = specials[_SPC_SUBJECT_START]
    subject_end = specials[_SPC_SUBJECT_END]
    
    endpoint.create_edge( label = schema.SequenceBlastqueriedSequence,
                          start_uid = query_uid,
                          end_uid = subject_uid,
                          properties = dict( properties ) )
    
    if deep_query:
        # Expand BLAST edge to BLAST node
        blast_uid = str( uuid4() )
        endpoint.create_node( label = schema.Blast,
                              uid = blast_uid,
                              properties = dict( properties ) )
        
        endpoint.create_edge( label = schema.BlastQueriesSequence,
                              start_uid = blast_uid,
                              end_uid = query_uid,
                              properties = { "subject": False, "start": query_start, "end": query_end } )
        
        endpoint.create_edge( label = schema.BlastQueriesSequence,
                              start_uid = blast_uid,
                              end_uid = subject_uid,
                              properties = { "subject": True, "start": subject_start, "end": subject_end } )
        
        # Expand TARGET edge to TARGET node
        query_ss_name = "{0}({1},{2})".format( query_uid, query_start, query_end )
        
        endpoint.create_node( label = schema.Subsequence,
                              uid = query_ss_name,
                              properties = { "start": query_start, "end": query_end } )
        
        endpoint.create_edge( label = schema.BlastUsesSubsequence,
                              start_uid = blast_uid,
                              end_uid = query_ss_name,
                              properties = { "is_subject": False } )
        
        endpoint.create_edge( label = schema.SequenceContainsSubsequence,
                              start_uid = query_uid,
                              end_uid = query_ss_name,
                              properties = { } )
        
        subject_ss_name = "{0}({1},{2})".format( subject_uid, subject_start, subject_end )
        
        endpoint.create_node( label = schema.Subsequence,
                              uid = subject_ss_name,
                              properties = { "start": subject_start, "end": subject_end } )
        
        endpoint.create_edge( label = schema.BlastUsesSubsequence,
                              start_uid = blast_uid,
                              end_uid = subject_ss_name,
                              properties = { "is_subject": True } )
        
        endpoint.create_edge( label = schema.SequenceContainsSubsequence,
                              start_uid = subject_uid,
                              end_uid = subject_ss_name,
                              properties = { } )
        
        endpoint.create_edge( label = schema.SubsequenceBlastqueriedSubsequence,
                              start_uid = query_ss_name,
                              end_uid = subject_ss_name,
                              properties = properties )


unknown = str

# noinspection SpellCheckingInspection
BLASTMAP = {
    # BLAST-name    Description                                 DB name                       Type      Special
    "qseqid"     : ("Query Seq-id", "query_accession", str, _SPC_QUERY_UID),
    "qgi"        : ("Query GI", "query_gi", unknown, _SPC_NONE_),
    "qacc"       : ("Query accesion", "query_accession", unknown, _SPC_NONE_),
    "sseqid"     : ("Subject Seq-id", "subject_accession", str, _SPC_SUBJECT_UID),
    "sallseqid"  : ("All subject Seq-id(s)", "all_subject_accessions", unknown, _SPC_NONE_),
    "sgi"        : ("Subject GI", "subject_gi", unknown, _SPC_NONE_),
    "sallgi"     : ("All subject GIs", "all_subject_gis", unknown, _SPC_NONE_),
    "sacc"       : ("Subject accession", "subject_accession", unknown, _SPC_NONE_),
    "sallacc"    : ("All subject accessions", "all_subject_accessions", unknown, _SPC_NONE_),
    "qstart"     : ("Start of alignment in query", "query_start", int, _SPC_QUERY_START),
    "qend"       : ("End of alignment in query", "query_end", int, _SPC_QUERY_END),
    "sstart"     : ("Start of alignment in subject", "subject_start", int, _SPC_SUBJECT_START),
    "send"       : ("End of alignment in subject", "subject_end", int, _SPC_SUBJECT_END),
    "qseq"       : ("Aligned part of query sequence", "aligned_query_sequence", unknown, _SPC_NONE_),
    "sseq"       : ("Aligned part of subject sequence", "aligned_subject_sequence", unknown, _SPC_NONE_),
    "evalue"     : ("Expect value", "e_value", float, _SPC_NONE_),
    "bitscore"   : ("Bit score", "bit_score", float, _SPC_NONE_),
    "score"      : ("Raw score", "raw_score", unknown, _SPC_NONE_),
    "length"     : ("Alignment length", "alignment_length", int, _SPC_NONE_),
    "pident"     : ("Percentage of identical matches", "percent_identity", float, _SPC_NONE_),
    "nident"     : ("Number of identical matches", "num_identical", int, _SPC_NONE_),
    "mismatch"   : ("Number of mismatches", "mismatches", int, _SPC_NONE_),
    "positive"   : ("Number of positive-scoring matches", "num_positive", int, _SPC_NONE_),
    "gapopen"    : ("Number of gap openings", "gap_opens", int, _SPC_NONE_),
    "gaps"       : ("Total number of gap", "num_gaps", int, _SPC_NONE_),
    "slen"       : ("Subject length (?)", "subject_length", int, _SPC_NONE_),
    "qlen"       : ("Query length (?)", "query_length", int, _SPC_NONE_),
    "ppos"       : ("Percentage of positive-scoring matches", "percent_positive", float, _SPC_NONE_),
    "frames"     : ("Query and subject frames", "frames", unknown, _SPC_NONE_),
    "qframe"     : ("Query frame", "query_frame", unknown, _SPC_NONE_),
    "sframe"     : ("Subject frame", "subject_frame", unknown, _SPC_NONE_),
    "btop"       : ("Blast traceback operations", "traceback", unknown, _SPC_NONE_),
    "staxids"    : ("unique Subject Taxonomy ID(s)", "subject_taxonomy", unknown, _SPC_NONE_),
    "sscinames"  : ("unique Subject Scientific Name(s)", "subject_scientific_name", unknown, _SPC_NONE_),
    "scomnames"  : ("unique Subject Common Name(s)", "subject_common_name", unknown, _SPC_NONE_),
    "sblastnames": ("unique Subject Blast Name(s)", "subject_blast_name", unknown, _SPC_NONE_),
    "sskingdoms" : ("unique Subject Super Kingdom(s)", "subject_super_kingdom", unknown, _SPC_NONE_),
    "stitle"     : ("Subject Title", "subject_title", unknown, _SPC_NONE_),
    "salltitles" : ("All Subject Title(s)", "all_subject_titles", unknown, _SPC_NONE_),
    "sstrand"    : ("Subject Strand", "subject_strand", unknown, _SPC_NONE_),
    "qcovs"      : ("Query Coverage Per Subject", "query_coverage_per_subject", unknown, _SPC_NONE_),
    "qcovhsp"    : ("Query Coverage Per HSP", "query_coverage_per_hsp", unknown, _SPC_NONE_),
    "qcovus"     : ("Measure of Query Coverage", "query_coverage", unknown, _SPC_NONE_)
}

# noinspection SpellCheckingInspection
BLASTAUTOMAP = {
    # ID    Description                                                 Translation
    "std": ("BLAST standard", ("qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send", "evalue", "bitscore")),
    "pcn": ("J. Pathmanathan's clean network for Composite Searcher", ("qseqid", "sseqid", "evalue", "pident", "bitscore", "qstart", "qend", "qlen", "sstart", "send", "slen"))
}


def __blast_columns_help():
    """
    Lists the BLAST column mapping, taken from the BLAST+ documentation at https://www.ncbi.nlm.nih.gov/books/NBK279675/.
    """
    r = []
    
    r.append( "Details on BLAST columns" )
    r.append( "Columns" )
    r.append( "<table>" )
    r.append( intermake.pr.fmt_row( ["BLAST+ name", "Description", intermake.Controller.ACTIVE.app.name + " name (once in database)"] ) )
    
    for k, v in BLASTMAP.items():
        description = v[0]
        name = v[1]  # name
        
        if v[3] != _SPC_NONE_:  # special
            description += " **MANDATORY**"
        
        r.append( intermake.pr.fmt_row( [k, description, name] ) )
    
    r.append( "</table>" )
    
    r.append( "Special identifiers" )
    r.append( "<table>" )
    r.append( intermake.pr.fmt_row( ["ID", "Description", "Translation"] ) )
    
    for k, v in BLASTAUTOMAP.items():
        r.append( intermake.pr.fmt_row( [k, v[0], ", ".join( v[1] )] ) )
    
    r.append( "</table>" )
    
    return "\n".join( r )


intermake.Application.LAST.help.add( "blast_columns", "Quick reference sheet for the available columns in BLAST", __blast_columns_help )
