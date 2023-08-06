import getpass
import os.path
import sys

import mhelper
import neocommand
import bio42


class Config:
    def __init__( self ):
        assert bio42.Application.is_running
        self.sample_root = sys.argv[1] if len( sys.argv > 1 ) else "/Users/martinrusilowicz/work/data/plasmids/genbank"
        table = [mhelper.file_helper.list_dir( self.sample_root )]
        self.genbank_file = self.__find_file( table, "all.gb", "b1b2ec60136ad9ec9c4f89d212594f8dc230f92b" ),
        self.annotations_file = self.__find_file( table, "seq-to-familiy-and-go.tsv", "ddc8657c1d4a342044b212de0ff2bfe325d57e19" )
        self.blast_file = self.__find_file( table, "todo", "????" )
        self.coincidence_family_file = self.__find_file( table, "seq-to-family.csv", "????" )
        self.coincidence_edge_file = self.__find_file( table, "significant.csv", "????" )
        self.db_driver = "neo4jv1"
        self.db_host = "127.0.0.1"
        self.db_user = "neo4j"
        self.db_directory = os.path.expanduser( "~/bin/neo4j330" )
        self.db_operating_system = neocommand.EOperatingSystem.UNIX
        self.db_port = 7474
        self.coincidence_family_map = { "sequence": "Sequence.uid:ID(Sequence)",
                                        "family"  : "Family.uid:ID(Family)" }
        self.coincidence_edge_map = { ""      : "",
                                      "Source": "",
                                      "Target": "",
                                      "name_i": "Association.:START_ID(Family)",
                                      "name_j": "Association.:END_ID(Family)",
                                      "p"     : "Association.p:float",
                                      "suc"   : "Association.suc:int",
                                      "obs"   : "Association.obs:int",
                                      "rate"  : "Association.rate:float",
                                      "exp"   : "Association.exp:float",
                                      "tot_i" : "Association.tot_i:int",
                                      "tot_j" : "Association.tot_j:int",
                                      "frac_i": "Association.frac_i:int",
                                      "frac_j": "Association.frac_j:int" }
        self.genbank_user_edges = ["_organism=Taxon"] 
        self.refresh_downloads = True
        self.remove_downloads = True
        print( "The following assumptions have been made:" )
        print( "\n".join( "{}: {}".format( k, v ) for k, v in self.__dict__.items() ) )
        self.db_password = getpass.getpass( "Database password: " )
    
    
    def __find_file( self, table, name, hash ):
        poss = []
        
        for x in table:
            if mhelper.file_helper.get_file_name( x ) == name:
                poss.append( x )
        
        if not poss:
            raise ValueError( "The data provided is missing the required file - name: '{}', hash: '{}'. There is no file with this name.".format( name, hash ) )
        elif len( poss ) > 1:
            raise ValueError( "The data provided is missing the required file - name: '{}', hash: '{}'. There are multiple files with this name ({}).".format( name, hash, poss ) )
        
        file_name = poss[0]
        
        achash = mhelper.io_helper.hash_file( file_name )
        
        if achash != hash:
            raise ValueError( "The data provided is missing the required file - name: '{}', hash: '{}'. There is a file with this name ({}) but the hash is different ({}).".format( name, hash, file_name, achash ) )
        
        return file_name


def log( message ):
    print( mhelper.ansi.BACK_BLUE + mhelper.ansi.FORE_WHITE + message + mhelper.ansi.RESET )
