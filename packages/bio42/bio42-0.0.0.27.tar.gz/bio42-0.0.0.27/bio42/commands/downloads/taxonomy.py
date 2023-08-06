from typing import Optional

import warnings
import intermake
import neocommand
import os
import os.path
import zipfile

from bio42.application import app
from bio42.commands.downloads import _common

@app.command( folder = "import" )
def download_taxonomy( destination: Optional[neocommand.Destination], extract: bool = True, refresh: bool = False, clean: bool = False, url: str = "" ) -> None:
    """
    Downloads and optionally imports the NCBI taxonomy database.
    
    :param refresh:     Downloads and extracts the ZIP file into a database file, even either
                        already exist on disk.
    :param destination:        Endpoint to import into.
                        `None` = Just download and extract, don't import 
    :param extract:     ZIPs are extracted into databases.
                        Unsetting this parameter prevents that.
                        This parameter is enforced if an `endpoint` is specified.
    :param clean:       ZIP files are deleted after extraction and database files are deleted
                        after importation.
                        Unsetting this parameter prevents that.
    :param url:         Specifies the location of the NCBI taxonomy database dump to use.
                        If this is left blank, a default location is assumed:
                            
                            ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.zip
                            
                        The ZIP will be downloaded, extracted and imported.
                        Please make sure that you trust the source.
    """
    url = url or "ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.zip"
    
    dir = intermake.Controller.ACTIVE.app.local_data.local_folder( "downloads", "taxonomy" )
    zip_fn = os.path.join( dir, "new_taxdump.zip" )
    tax_fn = os.path.join( dir, "nodes.dmp" )
    nam_fn = os.path.join( dir, "names.dmp" )
    
    zip_exists = os.path.isfile( zip_fn )
    tax_exists = os.path.isfile( tax_fn )
    nam_exists = os.path.isfile( nam_fn )
    dat_exists = tax_exists and nam_exists
    
    is_my_zip = False
    download = True
    my_extraction = ()
    
    if not extract and destination is not None:
        warnings.warn( "Setting `extract` to `True` because an `endpoint` was specified." )
        extract = True
    
    #
    # If there is only half a database, remove it
    #
    if nam_exists and not tax_exists:
        os.remove( nam_fn )
        dat_exists = False
        warnings.warn( "A partial database existed, this has been now deleted:\n * {}".format( nam_fn ) )
    elif tax_exists and not nam_exists:
        os.remove( tax_fn )
        dat_exists = False
        warnings.warn( "A partial database existed, this has been now deleted:\n * {}".format( tax_fn ) )
    
    #
    # If a ZIP file already exists, remove it
    #
    if zip_exists:
        if refresh:
            os.remove( zip_fn )
            warnings.warn( "The existing ZIP has been deleted: {}".format( zip_fn ) )
        else:
            print( "Not downloading anything because the ZIP file already exists:\n * {}".format( zip_fn ) )
            download = False
    
    #
    # If a database already exists, remove it
    #
    if dat_exists:
        if refresh:
            os.remove( tax_fn )
            os.remove( nam_fn )
            warnings.warn( "The existing database has been deleted:\n * {}\n * {}".format( tax_fn, nam_fn ) )
        else:
            print( "Not downloading anything because the database files already exist:\n * {}\n * {}".format( tax_fn, nam_fn ) )
            download = False
            extract = False
    
    #
    # Download the data
    #
    if download:
        _common.download_file( url, zip_fn )
        is_my_zip = True
    
    #
    # Extract the data?
    #
    if extract:
        with intermake.pr.pr_action( "Extracting" ):
            zip = zipfile.ZipFile( zip_fn, 'r' )
            zip.extract( "nodes.dmp" )
            zip.extract( "names.dmp" )
            my_extraction = zip.namelist() if clean else ()
            zip.close()
        
        #
        # Remove the ZIP
        #
        if clean and is_my_zip:
            with intermake.pr.pr_action( "Deleting downloaded zip" ):
                os.remove( zip_fn )
    
    #
    # Import the database
    #
    if destination is not None:
        import bio42
        bio42.import_taxonomy( destination, tax_fn, nam_fn )
        
        #
        # Clean the extracted files
        #
        if clean and my_extraction:
            for name in intermake.pr.pr_iterate( my_extraction, title = "Deleting extracted files" ):
                name = os.path.join( dir, name )
                os.remove( name )


