from os import path
from typing import Optional

from intermake.engine.environment import Controller
from mhelper import file_helper


FILENAME_EDGE_PREFIX = "edge"
EXT_B42CSV = ".typed_csv"
FILENAME_NODE_PREFIX = "node"

class NcvEntitySpec:  # TODO: Remove - redundant with EntitySchema
    """
    The superclass of `NcvFilename`, that contains just the bare information.
    """
    
    
    def __init__( self, is_edge: bool, label: str, start_label: Optional[str], end_label: Optional[str] ):
        self.is_edge = is_edge
        self.label = label
        self.start_label = start_label
        self.end_label = end_label
    
    
    def __str__( self ):
        if self.is_edge:
            return "({})-[{}]->({})".format( self.start_label, self.label, self.end_label )
        else:
            return "({})".format( self.label )


class NcvFilename( NcvEntitySpec ):
    """
    We use specific filenames for the Neo4j CSVs, this class creates and interprets them.
    
    :remarks:
    Use the `construct_from` methods to create the object.
    """
    
    
    def __init__( self, file_name: str, is_edge: bool, label: str, start_label: Optional[str], end_label: Optional[str] ):
        self.filename = file_name
        self.alone = file_helper.get_filename_without_extension( file_name )
        super().__init__( is_edge, label, start_label, end_label )
    
    
    def __str__( self ):
        return "'{}' {}".format( self.filename, super().__str__() )
    
    
    
    
    @classmethod
    def construct_from_node( cls, folder_path: str, label: str ):
        assert label, "Invalid node label (blank)"
        file_name = path.join( folder_path, FILENAME_NODE_PREFIX + "-" + label ) + EXT_B42CSV
        return cls( file_name, False, label, None, None )
    
    
    @classmethod
    def construct_from_edge( cls, folder_path, label: str, start_label: str, end_label: str ):
        assert label, "Invalid edge label (blank)"
        assert start_label, "Invalid start_label (blank)"
        assert end_label, "Invalid end_label (blank)"
        file_name = path.join( folder_path, FILENAME_EDGE_PREFIX + "-" + start_label + "-" + label + "-" + end_label ) + EXT_B42CSV
        return cls( file_name, True, label, start_label, end_label )
    
    
    @classmethod
    def construct_from_file( cls, file_name ):
        filename_parts = file_helper.get_filename_without_extension( file_name ).split( "-" )
        
        if filename_parts[0] == FILENAME_NODE_PREFIX:
            # Nodes
            assert len( filename_parts ) == 2, "I don't understand the node-table filename «{}» because I expected it to have 2 parts but I got {}.".format( file_name, filename_parts )
            return cls( file_name, False, filename_parts[1], None, None )
        elif filename_parts[0] == FILENAME_EDGE_PREFIX:
            # Edges
            assert len( filename_parts ) == 4, "I don't understand the edge-table filename «{}» because I expected it to have 4 parts but I got {}.".format( file_name, filename_parts )
            return cls( file_name, True, filename_parts[2], filename_parts[1], filename_parts[3] )
        else:
            # Something else :(
            raise ImportError( "A 'NcvFilename' cannot be constructed from the filename «{0}» because it is not a valid " + Controller.ACTIVE.app.name + " filename.".format( file_name ) )
