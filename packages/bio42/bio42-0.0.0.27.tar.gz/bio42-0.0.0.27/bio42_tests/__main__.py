import bio42 as b4
import time

from bio42_tests._helpers import Config, log


def main():
    """
    This is our test program's entry point.
    """
    # Read our configuration from the command line
    log( "Read our configuration from the command line" )
    config = Config()
    
    # Open a connection to our database
    log( "Open a connection to our database" )
    database  = b4.open_database( name      = "db_endpoint",
                                  driver    = config.db_driver,
                                  host      = config.db_host,
                                  user      = config.db_user,
                                  password  = config.db_password,
                                  directory = config.db_directory,
                                  os        = config.db_operating_system,
                                  port      = config.db_port )
    
    # Create our destination "parcels"
    base_parcel      = b4.open_parcel( name = "base_parcel"         )
    taxa_parcel      = b4.open_parcel( name = "taxa_parcel"         )
    ontology_parcel  = b4.open_parcel( name = "ontology_parcel"     )
    sequences_parcel = b4.open_parcel( name = "sequences_parcel"    )
    blast_parcel     = b4.open_parcel( name = "blast_parcel"        )
    anno_parcel      = b4.open_parcel( name = "anno_parcel"         )
    fam_parcel       = b4.open_parcel( name = "fam_parcel"          )
    coin_parcel      = b4.open_parcel( name = "coin_parcel"         )
    
    # Download and import taxa
    log( "Download and import taxa" )
    b4.download_taxonomy( destination   = taxa_parcel,
                          refresh       = config.refresh_downloads,
                          clean         = config.remove_downloads )
    
    # Download and import GO terms
    log( "Download and import GO terms" )
    b4.download_ontology( destination   = ontology_parcel,
                          refresh       = config.refresh_downloads,
                          clean         = config.remove_downloads )
    
    # Import our sequence data
    log( "Import our sequence data" )
    b4.import_sequences( file            = config.genbank_file,
                         destination     = sequences_parcel,
                         create          = b4.ESequenceFlags.ALL,
                         user_edges      = config.genbank_user_edges,
                         taxonomy_source = taxa_parcel )
    
    # Import our BLAST data
    log( "Import our BLAST data" )
    b4.import_blast( file_name      = config.blast_file,
                     destination    = blast_parcel,
                     deep_query     = True )
    
    # Import our annotations
    log( "Import our annotations" )
    b4.import_annotations( file_name    = config.annotations_file,
                           destination  = anno_parcel )
    
    # Import our gene families
    log( "Import our gene families" )
    b4.import_csv( file_name        = config.coincidence_family_file,
                   destination      = coin_parcel,
                   mapping          = config.coincidence_family_map )
    
    # Import our coincidence network
    log( "Import our coincidence network" )
    b4.import_csv( file_name        = config.coincidence_edge_file,
                   destination      = fam_parcel,
                   mapping          = config.coincidence_edge_map )
    
    # Move our data into the database!
    # Note that we use a variety of methods for testing, not because it's efficient!
    
    # Create a 'base_parcel' that contains most of the information
    log( "Move taxa_parcel to base_parcel" )
    b4.transfer( origin             = taxa_parcel,
                 destination        = base_parcel )
    
    log( "Move ontology_parcel to base_parcel" )
    b4.transfer( origin             = ontology_parcel,
                 destination        = base_parcel )
    
    log( "Move sequences_parcel to base_parcel" )
    b4.transfer( origin             = sequences_parcel,
                 destination        = base_parcel )
    
    log( "Move blast_parcel to base_parcel" )
    b4.transfer( origin             = blast_parcel,
                 destination        = base_parcel )
    
    # Create a new database from our 'base_parcel' and switch Neo4j to using it
    log( "Move base_parcel to database" )
    b4.transfer( origin             = base_parcel,
                 destination        = database,
                 method             = b4.EParcelMethod.CREATE )
    
    log( "Set database as active" )
    b4.set_database( server         = database,
                     database       = base_parcel.name )
    
    log( "Restart database server" )
    b4.control_server( server       = database,
                       command      = b4.ENeo4jCommand.RESTART )
    
    log( "Wait for server to restart" )
    while not b4.test_connection( server = database ).is_running:
        print( "Waiting for Neo4j to restart." )
        time.sleep( 2 )
    
    # Add our other information using the remaining methods we haven't yet tested
    log( "Move anno_parcel to database" )
    b4.transfer( origin         = anno_parcel,
                 destination    = database,
                 method         = b4.EParcelMethod.DIRECT )
    
    log( "Move fam_parcel to database" )
    b4.transfer( origin         = fam_parcel,
                 destination    = database,
                 method         = b4.EParcelMethod.ADD )
    
    log( "Move coin_parcel to database" )
    b4.transfer( origin         = coin_parcel,
                 destination    = database,
                 method         = b4.EParcelMethod.IMPORT )
    
    # Clean up 
    for parcel in (base_parcel, taxa_parcel, ontology_parcel, sequences_parcel,
                   blast_parcel, anno_parcel, fam_parcel, coin_parcel):
        log( "Delete {} from disk".format( parcel.name ) )
        b4.close_endpoint( endpoint = parcel, 
                           delete   = True )
    
    log( "Close the database connection" )
    b4.close_endpoint( database )


if __name__ == "__main__":
    main()
