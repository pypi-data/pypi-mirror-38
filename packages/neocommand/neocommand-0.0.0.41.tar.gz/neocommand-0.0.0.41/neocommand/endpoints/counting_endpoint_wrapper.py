from mhelper import override, string_helper
from neocommand.endpoints.abstract_endpoints import Writer, Destination
from neocommand.data import NcNode, NcEdge, NcData


class CounterWriter( Writer ):
    """
    A `Writer` that wraps another `Writer`, countint the number of items sent to it.
    """
    
    def __init__( self, endpoint: Writer ):
        super().__init__()
        self.endpoint = endpoint
        self.num_nodes = 0
        self.num_edges = 0
        self.num_data = 0
    
    
    @override
    def on_write_data( self, data: NcData ):
        self.num_data += 1
        return self.endpoint.write_data( data )
    
    
    def on_write_node( self, node: NcNode ):
        self.num_nodes += 1
        return self.endpoint.write_node( node )
    
    
    def on_write_edge( self, edge: NcEdge ):
        self.num_edges += 1
        return self.endpoint.write_edge( edge )
    
    
    def on_write_folder( self, name: str ) -> "Destination":
        return self.endpoint.write_folder( name = name )
    
    
    def __str__( self ):
        r = []
        
        if self.num_nodes:
            r.append( "{} nodes".format( self.num_nodes ) )
        
        if self.num_edges:
            r.append( "{} edges".format( self.num_edges ) )
        
        if self.num_data:
            r.append( "{} variables".format( self.num_data ) )
        
        if not r:
            r.append( "Nothing" )
        
        return "Counter: {} --> {}".format( string_helper.format_array( r, final = " and " ), self.endpoint )
