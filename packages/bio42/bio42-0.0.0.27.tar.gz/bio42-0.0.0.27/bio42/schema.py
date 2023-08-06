"""
Neo4j doesn't have a well defined 'schema', this class just tells the underlying
library (neocommand) what our Bio42 database is supposed to look like so we
can check it against this and we have somewhere to formally define the names of
everything.
"""

from neocommand import NodeSchema as _node, EdgeSchema as _edge, PropertySchema as _data, DatabaseSchema
from typing import TypeVar


_T = TypeVar( "_T" )
available = []


def register( schema: DatabaseSchema ):
    for x in available:
        schema.register( x )


def _add( x: _T ) -> _T:
    available.append( x )
    return x


# noinspection SpellCheckingInspection
Blast = _add( _node( label = "Blast",
                     is_complete = True,
                     properties = (_data( "query_accession", str, doc = "Query Seq-id, blast name = qseqid, qacc" ),
                                   _data( "query_gi", str, doc = "Query GI, blast name = 'qgi'" ),
                                   _data( "all_subject_accessions", str, doc = "All subject Seq-id(s), blast name = 'sallseqid, sallacc'" ),
                                   _data( "subject_gi", str, doc = "Subject GI, blast name = 'sgi'" ),
                                   _data( "all_subject_gis", str, doc = "All subject GIs, blast name = 'sallgi'" ),
                                   _data( "subject_accession", str, doc = "Subject accession, blast name = 'sseqid, sacc'" ),
                                   _data( "query_start", int, doc = "Start of alignment in query, blast name = 'qstart'" ),
                                   _data( "query_end", int, doc = "End of alignment in query, blast name = 'qend'" ),
                                   _data( "subject_start", int, doc = "Start of alignment in subject, blast name = 'sstart'" ),
                                   _data( "subject_end", int, doc = "End of alignment in subject, blast name = 'send'" ),
                                   _data( "aligned_query_sequence", str, doc = "Aligned part of query sequence, blast name = 'qseq'" ),
                                   _data( "aligned_subject_sequence", str, doc = "Aligned part of subject sequence, blast name = 'sseq'" ),
                                   _data( "e_value", float, doc = "Expect value, blast name = 'evalue'" ),
                                   _data( "bit_score", float, doc = "Bit score, blast name = 'bitscore'" ),
                                   _data( "raw_score", str, doc = "Raw score, blast name = 'score'" ),
                                   _data( "alignment_length", int, doc = "Alignment length, blast name = 'length'" ),
                                   _data( "percent_identity", float, doc = "Percentage of identical matches, blast name = 'pident'" ),
                                   _data( "num_identical", int, doc = "Number of identical matches, blast name = 'nident'" ),
                                   _data( "mismatches", int, doc = "Number of mismatches, blast name = 'mismatch'" ),
                                   _data( "num_positive", int, doc = "Number of positive-scoring matches, blast name = 'positive'" ),
                                   _data( "gap_opens", int, doc = "Number of gap openings, blast name = 'gapopen'" ),
                                   _data( "num_gaps", int, doc = "Total number of gap, blast name = 'gaps'" ),
                                   _data( "subject_length", int, doc = "Subject length (?), blast name = 'slen'" ),
                                   _data( "query_length", int, doc = "Query length (?), blast name = 'qlen'" ),
                                   _data( "percent_positive", float, doc = "Percentage of positive-scoring matches, blast name = 'ppos'" ),
                                   _data( "frames", str, doc = "Query and subject frames, blast name = 'frames'" ),
                                   _data( "query_frame", str, doc = "Query frame, blast name = 'qframe'" ),
                                   _data( "subject_frame", str, doc = "Subject frame, blast name = 'sframe'" ),
                                   _data( "traceback", str, doc = "Blast traceback operations, blast name = 'btop'" ),
                                   _data( "subject_taxonomy", str, doc = "unique Subject Taxonomy ID(s), blast name = 'staxids'" ),
                                   _data( "subject_scientific_name", str, doc = "unique Subject Scientific Name(s), blast name = 'sscinames'" ),
                                   _data( "subject_common_name", str, doc = "unique Subject Common Name(s), blast name = 'scomnames'" ),
                                   _data( "subject_blast_name", str, doc = "unique Subject Blast Name(s), blast name = 'sblastnames'" ),
                                   _data( "subject_super_kingdom", str, doc = "unique Subject Super Kingdom(s), blast name = 'sskingdoms'" ),
                                   _data( "subject_title", str, doc = "Subject Title, blast name = 'stitle'" ),
                                   _data( "all_subject_titles", str, doc = "All Subject Title(s), blast name = 'salltitles'" ),
                                   _data( "subject_strand", str, doc = "Subject Strand, blast name = 'sstrand'" ),
                                   _data( "query_coverage_per_subject", str, doc = "Query Coverage Per Subject, blast name = 'qcovs'" ),
                                   _data( "query_coverage_per_hsp", str, doc = "Query Coverage Per HSP, blast name = 'qcovhsp'" ),
                                   _data( "query_coverage", str, doc = "Measure of Query Coverage, blast name = 'qcovus'" )) ) )

Family = _add( _node( "Family" ) )

Feature = _add( _node( "Feature" ) )

Reference = _add( _node( "Reference" ) )

Source = _add( _node( "Source" ) )

Plasmid = _add( _node( "Plasmid" ) )

Taxon = _add( _node( label = "Taxon",
                     is_complete = True,
                     properties = (_data( "parent_id", str, key = "Taxon" ),
                                   _data( "rank", str ),
                                   _data( "embl_code", str ),
                                   _data( "division_id", int ),
                                   _data( "inherited_div_flag", bool ),
                                   _data( "genetic_code_id", int ),
                                   _data( "inherited_gc_flag", bool ),
                                   _data( "mitochondrial_genetic_code_id", int ),
                                   _data( "inherited_mgc_flag", bool ),
                                   _data( "genbank_hidden_flag", bool ),
                                   _data( "hidden_subtree_root_flag", bool ),
                                   _data( "comments", str ),
                                   _data( "acronym", str ),
                                   _data( "anamorph", str ),
                                   _data( "authority", str ),
                                   _data( "blast_name", str ),
                                   _data( "common_name", str ),
                                   _data( "equivalent_name", str ),
                                   _data( "genbank_acronym", str ),
                                   _data( "genbank_anamorph", str ),
                                   _data( "genbank_common_name", str ),
                                   _data( "genbank_synonym", str ),
                                   _data( "in_part", str ),
                                   _data( "includes", str ),
                                   _data( "misnomer", str ),
                                   _data( "misspelling", str ),
                                   _data( "scientific_name", str ),
                                   _data( "scientific_names", str ),  # array?
                                   _data( "synonym", str ),
                                   _data( "teleomorph", str ),
                                   _data( "type_material", str )) ) )

Sequence = _add( _node( label = "Sequence",
                        is_complete = False,
                        properties = [_data( "description", str, is_default = True )] ) )

Subsequence = _add( _node( "Subsequence" ) )

Go = _add( _node( "Go" ) )

Ipr = _add( _node( "Ipr" ) )

Kegg = _add( _node( "Kegg" ) )

Pfam = _add( _node( "Pfam" ) )

BlastQueriesSequence = _add( _edge( Blast, "Queries", Sequence ) )

BlastUsesSubsequence = _add( _edge( Blast, "Queries", Subsequence ) )

FamilyAccompaniesFamily = _add( _edge( Family, "Accompanies", Family ) )

FamilyAvoidsFamily = _add( _edge( Family, "Avoids", Family ) )

FamilyContainsSequence = _add( _edge( Family, "Contains", Sequence ) )

FamilyReachesTaxon = _add( _edge( Family, "Reaches", Taxon ) )

FeatureOverlapsFeature = _add( _edge( Feature, "Overlaps", Feature ) )

SourceContainsSequence = _add( _edge( Source, "Contains", Sequence ) )

GoClassContainsGoClass = _add( _edge( Go, "Contains", Go ) )

GoClassContainsSequence = _add( _edge( Go, "Contains", Sequence ) )

IprClassContainsSequence = _add( _edge( Ipr, "Contains", Sequence ) )

KeggClassContainsSequence = _add( _edge( Kegg, "Contains", Sequence ) )

PfamClassContainsSequence = _add( _edge( Pfam, "Contains", Sequence ) )

PlasmidContainsSequence = _add( _edge( Plasmid, "Contains", Sequence ) )

SequenceBlastqueriedSequence = _add( _edge( Sequence, "Like", Sequence ) )

SequenceContainsFeature = _add( _edge( Sequence, "Contains", Feature ) )

SequenceContainsSubsequence = _add( _edge( Sequence, "Contains", Subsequence ) )

SequenceReferencesReference = _add( _edge( Sequence, "References", Reference ) )

SourceContainsFamily = _add( _edge( Source, "Contains", Family ) )

SourceTouchesFamily = _add( _edge( Source, "Touches", Family ) )

SubsequenceBlastqueriedSubsequence = _add( _edge( Subsequence, "Like", Subsequence ) )

SubsequenceOverlapsSubsequence = _add( _edge( Subsequence, "Overlaps", Subsequence ) )

TaxonContainsSequence = _add( _edge( Taxon, "Contains", Sequence ) )

TaxonContainsTaxon = _add( _edge( Taxon, "Contains", Taxon ) )
