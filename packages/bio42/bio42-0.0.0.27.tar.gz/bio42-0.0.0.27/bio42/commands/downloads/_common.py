import urllib.request
import intermake
import os
from mhelper import string_helper


def download_file( url, zip_fn ):
    BUFFER = 1000
    tmp_fn = zip_fn + ".download.tmp"
    print( "Downloading: {} --> {}".format( url, tmp_fn ) )
    with intermake.pr.pr_action( "Downloading", text = string_helper.format_size ) as action:
        with urllib.request.urlopen( url ) as input:
            with open( tmp_fn, "wb" ) as output:
                while True:
                    x = input.read( BUFFER )
                    
                    if not x:
                        break
                    
                    output.write( x )
                    action.increment( len( x ) )
        
        os.replace( tmp_fn, zip_fn )
