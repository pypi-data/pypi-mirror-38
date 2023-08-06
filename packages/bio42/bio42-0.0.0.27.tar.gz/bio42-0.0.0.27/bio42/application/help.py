import intermake


def init( app: intermake.Application ):
    app.help.add( "user_edges", "Specifying user-defined edges",
                  """
                  These are used to create 'X-->CONTAINS-->SEQUENCE' relationships.
                                                            
                  Specify a list of key-value pairs:
                  
                     `property=label,property=label`
                     
                  * `property` is the name of the sequence property used to obtain the UID of the target
                  * `label` is the label (node-type) of the target.
                     
                  Example:
                     
                     `_organism=Taxon,_plasmid=Plasmid`
                  
                  A special case is made when 'Taxon' is specified as the `label`. This allows `property` to specify the 
                  'scientific_name', rather than the 'uid', providing the `taxa` argument is specified.
                  
                  Note that for FASTA files, the properties are specified in the `id_parts` argument, but for GENBANK files they
                  are automatically inferred from the available data. 
                  
                  If you have trouble determining what the property names are, you can trial-import a smaller portion of your file, 
                  sending the data to the ECHO endpoint.
                  """ )
    
    app.help.add( "id_parts", "Specifying accessions",
                  """
                  Many FASTA files have identifiers in a `|` separated format, e.g.::
                      
                     >eggs|beans|spam
                     
                  * The `beans` sequence
                  * The `eggs` database
                  * The `spam` organism.
                  
                  The ``id_parts`` parameter on ``import_sequences`` allows you to pull apart these
                  identifiers. Specify a list of strings denoting the names of the properties for
                  each component, e.g.::
                  
                     sequence|database|organism
                  
                  You should specify as many values as are in your FASTA file.
                  Values may be blank, in which case these elements in the identifier are ignored.
                  You will normally use one of these properties as the `uid` of the node, which is
                  the accession: If not at least one of the elements is ``uid``, the entirety of
                  the name is used as the accession (``eggs|beans|spam`` in the example above).
                  
                  A simple example for a common FASTA file with extraneous information is::
                  
                     ,,,uid,
                     
                  This ignores elements 1, 2, 3 and 5, and assumes the 4th element as the accession. 
                  """ )
