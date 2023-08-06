import datetime
import re
import intermake
import neocommand
import uuid

from collections import defaultdict
from typing import Dict, Iterator, List, Optional, Tuple, Union, cast
from mhelper import EFileMode, isFilename, SwitchError, array_helper, file_helper, string_helper, MFlags, isOptional
from Bio import SeqIO
from Bio.Alphabet import Alphabet
from Bio.SeqFeature import CompoundLocation, FeatureLocation, Reference, SeqFeature
from Bio.SeqRecord import SeqRecord

from bio42 import schema
from bio42.application import app
from bio42.commands.parsers import parser_taxonomy


class ESequenceFlags( MFlags ):
    """
    :cvar SOURCES:           Source edges.
                                `True`  - an edge to the 'Source' node is included, denoting the origin of the data (i.e. the file path).
                                          This may be useful in limited circumstances when combining multiple datasets into the same
                                          database, but incurs an additional memory overhead of one additional edge per sequence.
                                `False` - `Source` nodes are not included.
    :cvar FASTAS:   Record sequences.
                              * `True` - full sequence data is added to the created Record nodes.
    :cvar FEATURE_FASTAS:  Feature sequences.
                              * `True` - full sequence data is added to the created Feature nodes.
    :cvar FEATURES:          Create nodes for features.
    :cvar REFERENCES:        Create nodes for references.
    :cvar ANNOTATIONS:       Create properties for record annotations. 
    :cvar QUALIFIERS:        Create properties for feature annotations ("qualifiers").

    """
    SOURCES = 1
    FASTAS = 2
    FEATURE_FASTAS = 4
    REFERENCES = 8
    FEATURES = 16
    QUALIFIERS = 32
    ANNOTATIONS = 64


@app.command( folder = "import" )
def import_sequences( file: isFilename[EFileMode.READ],
                      destination: neocommand.Destination,
                      create: ESequenceFlags = ESequenceFlags.NONE,
                      code: str = "",
                      id_parts: Optional[List[str]] = None,
                      user_edges: Optional[List[str]] = None,
                      taxonomy_file: isOptional[isFilename[EFileMode.READ]] = None,
                      taxonomy_source: Optional[neocommand.Origin] = None,
                      biopython_extraction: bool = False,
                      no_count: bool = False, ):
    # noinspection SpellCheckingInspection
    """
        Imports genes and sequences from a variety of formats.
        
        .. note::
        
            Requires BioPython.
    
        .. note::
        
            Labels, entities and properties are dynamic and dependent on the arguments passed and information found in 
            the source file.
        
        :param no_count:                  Disables counting.
                                          When set, skips the record counting step (this step is only used to estimate
                                          the processing time and show the progress bar).
                                          
        :param destination:                  Endpoint.
                                          Where to send the data to.
                                          
        :param file:                      The file to read.
                                          This can be in any of the formats accepted by the version of BioPython you
                                          have installed. At the time of writing this includes the following types:
                                              ABIF, ACE, EMBL, FASTA, FASTQ, FASTQ, FASTQ, FASTQ, Genbank,
                                              IntelliGenetics, IMGT, Protein, Bio, PHRED, NBRF, XML, SFF, SFF, XML,
                                              TSV, Quality, TXT.
                                              
        :param code:                      The type of file.
                                          This should designate the format of the `file`.
                                          This may be left blank, in which case the type is automatically determined
                                          from the file extension. 
                                          * `Empty`  = "default" 
                                           
        :param biopython_extraction:      Extraction method.
                                          * `True`  = "biopython" - Uses BioPython's extract feature, which is great
                                                                    but can be a bit slow.
                                          * `False` = "custom"    - uses a custom quick method (faster but less reliable).
                                          
        :param user_edges:                Edges to create.
                                          ¡Please see the help topic: `user_edges` for details!
                                          
        :param taxonomy_file:             Taxonomy-names file.
                                          Required if taxonomy nodes are specified in the `user_edges` argument,
                                          otherwise, this parameter is unused.
                                          Mutually exclusive with `taxonomy_database`.
                                          
        :param taxonomy_source:         Taxonomy-names source.
                                          Required if taxonomy nodes are specified in the `user_edges` argument,
                                          otherwise, this parameter is unused.
                                          Mutually exclusive with `taxonomy_file`.
                                          
        :param id_parts:                  How to determine the gene accession from the names in the file.
                                          See the help topic: `id_parts`.
                                          If no argument is specified, the entirety of the name as the accession.
                                          
        :param create:                    A set of flags which specifies the elements to create.
        """
    with destination.open_writer() as writer:
        __Process( file = file,
                   code = code,
                   writer = writer,
                   create = create,
                   id_parts = id_parts,
                   user_edges = user_edges,
                   taxonomy_file = taxonomy_file,
                   taxonomy_database = taxonomy_source,
                   biopython_extraction = biopython_extraction,
                   no_count = no_count )


# noinspection SpellCheckingInspection
class __Process:
    # noinspection SpellCheckingInspection
    def __init__( self,
                  *,
                  file: isFilename[EFileMode.READ],
                  code: str,
                  writer: neocommand.Writer,
                  create: ESequenceFlags,
                  id_parts: Optional[List[str]],
                  user_edges: Optional[List[str]],
                  taxonomy_file: isOptional[isFilename[EFileMode.READ]],
                  taxonomy_database: Optional[neocommand.Origin],
                  biopython_extraction: bool,
                  no_count: bool = False ):
        self.include_record_sequence = create.FASTAS
        self.include_feature_sequence = create.FEATURE_FASTAS
        self.include_references = create.REFERENCES
        self.include_features = create.FEATURES
        self.include_annotations = create.ANNOTATIONS
        self.include_qualifiers = create.QUALIFIERS
        
        if taxonomy_file:
            self.taxonomy_names_list = parser_taxonomy._read_scientific_names( taxonomy_file )
        elif taxonomy_database:
            self.taxonomy_names_list = _read_scientific_names_db( taxonomy_database )
        else:
            self.taxonomy_names_list = None
        self.id_parts = id_parts
        self.id_part_has_uid = neocommand.PRIMARY_KEY in id_parts if id_parts else False
        self.endpoint = neocommand.CounterWriter( writer )
        self.create_edges = self.__parse_user_edges_argument( user_edges )
        
        # Determine file type
        handler: IsParserFilter = None
        ext = file_helper.get_extension( file ).lower()
        
        if code:
            handler = IsParserFilter( code, code, "." + code, code, None )
        else:
            for x in _SEQUENCE_EXT:
                if x.extension == ext:
                    handler = x
                    break
            
            if handler is None:
                raise ValueError( "Did not understand extension. Please rename the file or provide a `code` parameter." )
        
        # Create "Source" node
        if create.SOURCES:
            self.source_uid = str( uuid.uuid4() )
            writer.create_node( label = schema.Source,
                                uid = self.source_uid,
                                properties = { "file_name"  : str( file ),
                                               "name"       : file_helper.get_filename( file ),
                                               "import_date": str( datetime.datetime.now() ) } )
        else:
            self.source_uid = None
        
        if handler.detect_records and not no_count:
            rx = re.compile( handler.detect_records )
            num_records = 0
            
            with intermake.pr.pr_action( "Counting records" ) as action:
                with open( file, "r" ) as file_in:
                    for line in file_in:
                        if rx.match( line ):
                            num_records += 1
                            action.increment()
        else:
            num_records = -1
        
        title = "Iterating {}".format( file_helper.get_filename( file ) )
        
        with intermake.pr.pr_action( title,
                                     count = num_records,
                                     text = lambda _: "{} nodes, {} edges".format( self.endpoint.num_nodes, self.endpoint.num_edges ) ) as action:
            self.action = action
            with open( file, "r" ) as file_in:
                for record in SeqIO.parse( file_in, handler.code ):
                    self.__process_line( record, biopython_extraction )
                    action.increment()
    
    
    @staticmethod
    def __parse_user_edges_argument( create_edges ):
        create_edges_list = []
        if create_edges:
            for x in create_edges:
                xx = x.split( "=" )
                if len( xx ) != 2:
                    raise ValueError( "The `create_edges` parameter expects key=value pairs: «{}» is invalid.".format( x ) )
                
                create_edges_list.append( xx )
        
        return create_edges_list
    
    
    def __read_id( self, id: str, props ) -> None:
        """
        FASTA contains other garbage that isn't in the GB, so to stay compatible we remove it
        This only works for GB fasta files and similar (i.e. where the true ID is the last element of the provided ID)
        """
        elements = id.split( "|" )
        
        if self.id_parts:
            if len( elements ) != len( self.id_parts ):
                raise ValueError( "The ID «{}» is not compatible with the ID format specified: «{}». Maybe you meant to specify a different format?".format( id, "|".join( self.id_parts ) ) )
            
            for index, property in enumerate( self.id_parts ):
                if property:
                    props[self._make_property_name( property, "" )] = elements[index]
        
        if not self.id_part_has_uid:
            assert neocommand.PRIMARY_KEY not in props
            props[neocommand.PRIMARY_KEY] = id.strip()
        
        assert neocommand.PRIMARY_KEY in props, "Internal error. ID parsed: «{}». No «{}» in properties: {}".format( id, neocommand.PRIMARY_KEY, props )
        assert props[neocommand.PRIMARY_KEY], "Internal error. ID parsed: «{}». Invalid «{}» in properties: {}".format( id, neocommand.PRIMARY_KEY, props )
    
    
    def __process_line( self, record: SeqRecord, true_extract: bool ) -> None:
        #
        # Record node
        #
        annotation_references, props, uid = self.__mk_record_node( record )
        
        #
        # Features
        #
        if self.include_features:
            for f in record.features:  # type:SeqFeature
                self.__mk_feature( f, record, uid, true_extract )
                self.action.still_alive()
        
        #
        # References
        #
        if self.include_references:
            for key, value in annotation_references.items():
                self.__mk_reference_node( key, uid, value )
                self.action.still_alive()
        
        #
        # Source edge
        if self.source_uid is not None:
            self.__mk_source_edge( uid )
        
        # 
        # User edges
        #
        if self.create_edges:
            for property, label in self.create_edges:
                self.__mk_user_edge( label, property, props, uid )
                self.action.still_alive()
    
    
    def __mk_record_node( self, record: SeqRecord ):
        """
        Creates a `NcNode` from a `SeqRecord`.
        """
        #
        # Truncate superfluous information
        #
        
        # - ignore record name if it is the same as the ID
        record_name = record.name
        
        if record_name == record.id:
            record_name = None
        
        # - truncate the part of the description that is the same as the ID
        description = record.description
        if description.startswith( record.id ):
            description = description[len( cast( str, record.id ) ):].lstrip()
        
        # - simplify the alphabet name
        alphabet_name = self._alphabet_shortcode( record.seq.alphabet )
        
        #
        # Create the property dictionary
        #
        props = { }
        props["source_id"] = record.id
        props["sequence_alphabet"] = alphabet_name
        if self.include_record_sequence:
            props["sequence"] = str( record.seq )
        if record_name:
            props["name"] = record_name
        if len( record.letter_annotations ):
            props["letter_annotations_count"] = len( record.letter_annotations )
        if len( record.dbxrefs ):
            # noinspection SpellCheckingInspection
            props["dbxrefs"] = record.dbxrefs
        if len( record.seq ):
            props["sequence_length"] = len( record.seq )
        if len( record.features ):
            props["features_count"] = len( record.features )
        if len( record.annotations ):
            props["annotations_count"] = len( record.annotations )
        if description:
            props["description"] = description
        self.__read_id( cast( str, record.id ), props )
        annotation_references = { }
        
        #
        # Dictionary annotations get expanded
        #
        annotations = { }
        
        if self.include_annotations:
            for key, value in record.annotations.items():
                def recursive_add( target_1, key_1, value_1 ):
                    if type( value_1 ) in [dict, defaultdict]:
                        for key_2, value_2 in value_1.items():
                            recursive_add( target_1, key_1 + "_" + key_2, value_2 )
                    else:
                        target_1[key_1] = value_1
                
                
                recursive_add( annotations, key, value )
            
            #
            # Convert annotations to properties with a leading "_"
            #
            for key, value in annotations.items():
                if not value:
                    # Don't add empty annotations
                    continue
                if type( value ) in neocommand.NeoType._BY_TYPE:
                    # Add all standard typed annotations
                    props[self._make_property_name( key )] = value  # if this is the wrong type it will get caught later
                elif (type( value ) == list) and (array_helper.list_type( value ) in neocommand.NeoType._BY_TYPE):
                    # Add lists of standard typed annotations
                    props[self._make_property_name( key )] = value
                elif type( value ) == Reference:
                    # Add references in their own special set
                    annotation_references[key] = value
                elif (type( value ) == list) and (array_helper.list_type( value ) == Reference):
                    # Add lists of references
                    for i, vv in enumerate( value ):
                        if type( vv ) == Reference:
                            annotation_references[key + "_" + str( i )] = vv
                else:
                    raise NotImplementedError( "InstanceHandler not implemented for annotation type. Regarding annotation «{0}» of value «{1}» and type «{2}» within sequence «{3}»".format( key, value, type( value ).__name__, record.id ) )
        
        #
        # Write
        #
        uid = props[neocommand.PRIMARY_KEY]
        del props[neocommand.PRIMARY_KEY]
        self.endpoint.create_node( label = schema.Sequence,
                                   uid = uid,
                                   properties = props )
        
        return annotation_references, props, uid
    
    
    def __mk_user_edge( self, label: str, property: str, record_props: Dict[str, Optional[object]], uid: str ):
        value = record_props.get( property )
        
        if value:
            if label == "Taxon" and self.taxonomy_names_list is not None:
                taxon_uid = self.taxonomy_names_list.get( value )
                
                if taxon_uid is None:
                    raise ValueError( "Cannot get the UID of the taxon named «{}» in the sequence with UID = «{}».".format( value, uid ) )
                
                value = taxon_uid
            
            self.endpoint.create_edge( label = schema.TaxonContainsSequence,
                                       start_uid = value,
                                       end_uid = uid,
                                       properties = { } )
    
    
    def __mk_source_edge( self, record_uid: str ):
        self.endpoint.create_edge( label = schema.SourceContainsSequence,
                                   start_uid = self.source_uid,
                                   end_uid = record_uid,
                                   properties = { } )
    
    
    def __mk_reference_node( self, reason: str, record_uid: str, reference: Reference ):
        reference_name = self._get_unique_id( reference )
        location = _LocationExtract( reference.location )
        self.endpoint.create_node( label = schema.Reference,
                                   uid = reference_name,
                                   properties = {
                                       "authors"            : reference.authors,
                                       "comment"            : reference.comment,
                                       "consrtm"            : reference.consrtm,  # I presume this is "consortium", but I haven't translated it because I cannot find any documentation to that effect
                                       "journal"            : reference.journal,
                                       "location_start"     : location.start,
                                       "location_end"       : location.end,
                                       "location_start_type": location.start_type,
                                       "location_end_type"  : location.end_type,
                                       "title"              : reference.title,
                                       "medline_id"         : reference.medline_id,
                                       "pubmed_id"          : reference.pubmed_id
                                   } )
        
        self.endpoint.create_edge( label = schema.SequenceReferencesReference,
                                   start_uid = record_uid,
                                   end_uid = reference_name,
                                   properties = { "reason": reason } )
    
    
    class MSubset:
        def __init__( self, record: SeqRecord, location: "_LocationExtract" ):
            self.record = record
            self.location = location
        
        
        @property
        def seq( self ) -> str:
            return self.record.seq[self.location.start:self.location.end]  # TODO: Check this, should it be inclusive?
        
        
        @property
        def features( self ) -> Iterator[SeqFeature]:
            for feature in self.record.features:
                location = _LocationExtract( feature.location )
                
                if self.location.start <= location.end and location.start <= self.location.end:
                    yield feature
    
    
    def __mk_feature( self, feature: SeqFeature, record: SeqRecord, record_uid: str, true_extract: bool ):
        """
        Converts a `SeqFeature` to a `NcNode`.
        """
        location = _LocationExtract( feature.location )
        
        if true_extract:
            record_subset = feature.extract( record )  # type: SeqRecord
        else:
            record_subset = self.MSubset( record, location )
        
        props = { }
        
        for key, value in feature.qualifiers.items():
            if key == "db_xref":
                for db_xref in value:
                    db, _ = db_xref.split( ":", 1 )
                    props["db_xref" + self._make_property_name( db )] = db_xref
            else:
                if self.include_qualifiers:
                    props[self._make_property_name( key )] = array_helper.decomplex( value )
        
        props["type"] = feature.type
        props["location_start"] = location.start
        props["location_end"] = location.end
        props["location_start_type"] = location.start_type
        props["location_end_type"] = location.end_type
        
        # Include sequence data
        if self.include_feature_sequence:
            props["sequence"] = record_subset.seq
        
        # The `translation` is annoying, get rid
        if "_translation" in props:
            del props["_translation"]
        
        feature_label, feature_uid = self.__get_feature_label_and_uid( feature, record_uid, location )
        
        props["feature_type"] = feature_label
        
        self.endpoint.create_node( label = schema.Feature,
                                   uid = feature_uid,
                                   properties = props )
        
        self.endpoint.create_edge( label = schema.SequenceContainsFeature,
                                   start_uid = record_uid,
                                   end_uid = feature_uid,
                                   properties = { } )
        
        for f2 in record_subset.features:
            f2_label, f2_uid = self.__get_feature_label_and_uid( f2, record_uid )
            
            f_key = feature_label + "|" + feature_uid
            f2_key = f2_label + "|" + f2_uid
            
            if f2_key >= f_key:
                continue  # Only create 1 edge
            
            self.endpoint.create_edge( label = schema.FeatureOverlapsFeature,
                                       start_uid = feature_uid,
                                       end_uid = f2_uid,
                                       properties = { } )
    
    
    def __get_feature_label_and_uid( self, feature: SeqFeature, record_uid: str, location = None ):
        uid = feature.id
        label = str( feature.type )
        
        if uid:
            uid = "{}_{}_{}".format( label, record_uid, uid )
        else:
            if location is None:
                location = _LocationExtract( feature.location )
            
            uid = "{}_{}[{}:{}]".format( label, record_uid, location.start, location.end )
        
        return label, uid
    
    
    def _make_property_name( self, key, prefix = "_" ):
        return prefix + string_helper.make_name( key )
    
    
    __ALPHABET = None
    
    
    @classmethod
    def __alphabet( cls ):
        from Bio import Alphabet
        from Bio.Alphabet import IUPAC
        
        
        if cls.__ALPHABET:
            return cls.__ALPHABET
        else:
            cls.__ALPHABET = {
                Alphabet.SingleLetterAlphabet: "S",
                Alphabet.ProteinAlphabet     : "P",
                Alphabet.NucleotideAlphabet  : "N",
                Alphabet.DNAAlphabet         : "D",
                Alphabet.RNAAlphabet         : "R",
                Alphabet.SecondaryStructure  : "SS",
                Alphabet.ThreeLetterProtein  : "3P",
                IUPAC.ExtendedIUPACProtein   : "xp",
                IUPAC.IUPACProtein           : "p",
                IUPAC.IUPACAmbiguousDNA      : "ad",
                IUPAC.ExtendedIUPACDNA       : "xd",
                IUPAC.IUPACAmbiguousRNA      : "ar",
                IUPAC.IUPACUnambiguousRNA    : "ur" }
            
            return cls.__ALPHABET
    
    
    def _alphabet_shortcode( self, a: Optional[Alphabet] ) -> Optional[str]:
        """
        Use alphabet short-codes to avoid polluting the database with long strings
        """
        alphabet = self.__alphabet()
        if type( a ) in alphabet:
            return alphabet[type( a )]
        
        t = str( a )
        TRUNCATE = "Alphabet()"
        if t.endswith( TRUNCATE ):
            return t[0:-len( TRUNCATE )]
        else:
            return t
    
    
    def _get_unique_id( self, x: Reference ) -> str:
        """
        Since there doesn't seem to be any consistency in the journal formats, this creates one
        It won't work for even slightly different formats, but at least comes up with something that will work for the same file
        """
        
        if x.pubmed_id:
            return x.pubmed_id
        
        if x.medline_id:
            return x.medline_id
        
        author = string_helper.first_words( x.authors )
        title = string_helper.first_words( x.title )
        journal = string_helper.first_words( x.journal )
        
        return author + "/" + title + "/" + journal


class IsParserFilter:
    def __init__( self, name: str, code: str, extension: Union[str, List[str]], description: str, detect_records: Optional[str] = None ):
        """
        :param name: Inherited 
        :param code: BioPython parser code 
        :param extension: Inherited 
        :param description: Inherited 
        """
        self.name = name
        self.extension = extension
        self.description = description
        self.detect_records = detect_records
        self.code = code


# noinspection SpellCheckingInspection
_SEQUENCE_EXT = (IsParserFilter( "ABIF", "abif", ".abif", "Applied Biosystem's sequencing trace format" ),
                 IsParserFilter( "ACE", "ace", ".ace", "Reads the contig. sequences from an ACE assembly file." ),
                 IsParserFilter( "EMBL", "embl", ".embl", "The EMBL flat file format." ),
                 IsParserFilter( "FASTA", "fasta", ".fasta", "The generic sequence file format where each record starts with an identifier line starting with a \">\" character, followed by lines of sequence.", detect_records = ">.*" ),
                 IsParserFilter( "FASTQ", "fastq", ".fastq", "A \"FASTA like\" format used by Sanger which also stores PHRED sequence quality values (with an ASCII offset of 33)." ),
                 IsParserFilter( "FASTQ (Sanger)", "fastq-sanger", ".fastq-sanger", "An alias for \"fastq\" for consistency with BioPerl and EMBOSS" ),
                 IsParserFilter( "FASTQ (Solexa)", "fastq-solexa", ".fastq-solexa", "Original Solexa/Illumnia variant of the FASTQ format which encodes Solexa quality scores (not PHRED quality scores) with an ASCII offset of 64." ),
                 IsParserFilter( "FASTQ (Illumina)", "fastq-illumina", ".fastq-illumina", "Solexa/Illumina 1.3 to 1.7 variant of the FASTQ format which encodes PHRED quality scores with an ASCII offset of 64 (not 33). Note as of version 1.8 of the CASAVA pipeline Illumina will produce FASTQ files using the standard Sanger encoding." ),
                 IsParserFilter( "Genbank", "genbank", [".genbank", ".gbff", ".gb"], "The GenBank or GenPept flat file format.", detect_records = "//.*" ),
                 IsParserFilter( "IntelliGenetics", "ig", ".ig", "The IntelliGenetics file format, apparently the same as the MASE alignment format." ),
                 IsParserFilter( "IMGT", "imgt", ".imgt", "An EMBL like format from IMGT where the feature tables are more indented to allow for longer feature types." ),
                 IsParserFilter( "Protein Data Bank", "pdb-seqres", ".pdb-seqres", "Reads a Protein Data Bank (PDB) file to determine the complete protein sequence as it appears in the header (no dependencies)." ),
                 IsParserFilter( "Bio.PDB", "pdb-atom", ".pdb-atom", "Uses Bio.PDB to determine the (partial) protein sequence as it appears in the structure based on the atom coordinate section of the file (requires NumPy for Bio.PDB)." ),
                 IsParserFilter( "PHRED-output", "phd", ".phd", "Output from PHRED, used by PHRAP and CONSED for input." ),
                 IsParserFilter( "NBRF", "pir", ".pir", "A \"FASTA like\" format introduced by the National Biomedical Research Foundation (NBRF) for the Protein Information Resource (PIR) database, now part of UniProt." ),
                 IsParserFilter( "XML (SeqXML)", "seqxml", ".seqxml", "SeqXML, simple XML format described in Schmitt et al (2011)." ),
                 IsParserFilter( "SFF", "sff", ".sff", "Standard Flowgram Format (SFF), typical output from Roche 454." ),
                 IsParserFilter( "SFF (trimmed)", "sff-trim", ".sff-trim", "Standard Flowgram Format (SFF) with given trimming applied." ),
                 IsParserFilter( "XML (UniProt)", "swiss", ".swiss", "Plain text Swiss-Prot aka UniProt format." ),
                 IsParserFilter( "TSV", "tab", [".tab", ".tsv"], "Simple two column tab separated sequence files, where each line holds a record's identifier and sequence. For example , this is used as by Aligent's eArray software when saving microarray probes in a minimal tab delimited text file." ),
                 IsParserFilter( "Quality", "qual", ".qual", "A \"FASTA like\" format holding PHRED quality values from sequencing DNA, but no actual sequences (usually provided in separate FASTA files)." ),
                 IsParserFilter( "TXT (UniProt)", "uniprot-xml", ".uniprot-xml", "The UniProt XML format (replacement for the SwissProt plain text format which we call \"swiss\")" ))

_ULocation = Union[FeatureLocation, int, List[FeatureLocation], List[int]]
"""
Union of types that can be used to identify a location within a sequence.
"""


class _LocationExtract:
    def __init__( self, locations: _ULocation ):
        if type( locations ) is not list:
            locations = [locations]
        
        start = []
        end = []
        
        # noinspection PyTypeChecker
        for location in locations:
            if type( location ) is int:
                start.append( location )
                end.append( location )
            elif type( location ) in [FeatureLocation, CompoundLocation]:
                start.append( location.start )
                end.append( location.end )
            else:
                raise SwitchError( "location", location )
        
        self.start, self.start_type = self.__translate_location( start )
        self.end, self.end_type = self.__translate_location( end )
    
    
    @staticmethod
    def __translate_location( positions ) -> Tuple[List[int], List[str]]:
        indices = []
        types = []
        
        for i, v in enumerate( positions ):
            if isinstance( v, int ):  # BioPython positions inherit int
                types.append( type( v ).__name__ )
                indices.append( int( v ) )
            else:
                raise ValueError( "Don't know how to convert the location value «{0}» of type «{1}»".format( v, type( v ) ) )
        
        return indices, types


def _read_scientific_names_db( database: neocommand.Origin ) -> Dict[int, str]:
    with database.open_reader() as reader:
        return { int( k ): v for k, v in reader.on_read_all_props( "Taxon", "scientific_name" ) }
