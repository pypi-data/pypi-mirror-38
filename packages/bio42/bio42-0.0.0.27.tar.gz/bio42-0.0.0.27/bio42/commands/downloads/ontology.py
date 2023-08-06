from typing import *

import os.path
import intermake
import neocommand

from bio42.application import app
from bio42.commands.downloads import _common


@app.command( folder = "import" )
def download_ontology( destination: Optional[neocommand.Destination], refresh: bool = False, clean: bool = False, url: str = "" ) -> None:
    """
    Downloads and optionally imports the Gene Ontology terms.
    
    :param refresh:     Downloads the database database file, even if it already exists on disk.
    :param destination:    Endpoint to import into.
                        `None` = Just download, don't import 
    :param clean:       Delete the downloaded file(s) after importation.
    :param url:         Specifies the location of the database dump to use.
                        If this is left blank, a default location is assumed:
                            
                            http://purl.obolibrary.org/obo/go.owl
                            
                        Suggested values include:
                        
                            GO Core: http://purl.obolibrary.org/obo/go.owl
                            GO Plus: http://purl.obolibrary.org/obo/go/extensions/go-plus.owl
                            
                        Please make sure that you trust the source.
    """
    url = url or "http://purl.obolibrary.org/obo/go.owl"
    dir = intermake.Controller.ACTIVE.app.local_data.local_folder( "downloads", "ontology" )
    file_name = os.path.join( dir, "go.owl" )
    
    if refresh and os.path.isfile( file_name ):
        os.remove( file_name )
        print( "The existing database has been deleted:\n* {}".format( file_name ) )
        
    if not os.path.isfile( file_name ):
        _common.download_file( url, file_name )
    else:
        print( "Not downloading anything because the database file already exists:\n* {}".format( file_name ) )
    
    if destination is None:
        return
    
    from bio42.commands.parsers import parser_go
    
    parser_go.import_go( destination, file_name )
    
    if clean:
        with intermake.pr.pr_action( "Deleting downloaded file" ):
            os.remove( file_name )
