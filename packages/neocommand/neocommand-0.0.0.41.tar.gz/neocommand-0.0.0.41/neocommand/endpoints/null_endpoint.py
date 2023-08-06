from neocommand.endpoints.abstract_endpoints import Destination, Writer, Origin, Reader
from neocommand.data import NcNode, NcEdge


class _NullEndpoint( Destination, Origin ):
    """
    A write-only endpoint that doesn't write the data anywhere.
    
    :ivar `READER`: A fixed value that may be used to access the reader directly.
    :ivar `WRITER`: A fixed value that may be used to access the writer directly. 
    """
    
    
    def __init__( self, name = "null" ):
        super().__init__( name )
        self.WRITER = _NullEndpointWriter()
        self.READER = _NullEndpointReader()
    
    
    def __str__( self ):
        return "NullEndpoint"
    
    
    def on_open_writer( self ):
        return self.WRITER
    
    
    def on_open_reader( self ):
        return self.READER


class _NullEndpointReader( Reader ):
    def on_read_all( self ):
        return ()
    
    
    def on_read_all_props( self, label: str, property: str ):
        return ()


class _NullEndpointWriter( Writer ):
    def on_write_data( self, data: object ):
        pass  # by intent
    
    
    def on_write_folder( self, name: str ) -> "Destination":
        pass  # by intent
    
    
    def on_write_edge( self, edge: NcEdge ):
        pass  # by intent
    
    
    def on_write_node( self, node: NcNode ):
        pass  # by intent
    
    
    def on_close( self ) -> None:
        pass
    
    
    def __bool__( self ) -> bool:
        return False


NULL_ENDPOINT = _NullEndpoint()
