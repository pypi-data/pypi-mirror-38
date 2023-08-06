from typing import Dict
from neocommand.endpoints.abstract_endpoints import Destination, Writer
from neocommand.data import NcNode, NcEdge


class _EchoingEndpoint( Destination ):
    """
    An write-only endpoint that echos data to the terminal.
    """
    
    
    def __init__( self, name = "echo" ) -> None:
        super().__init__( name )
    
    
    def on_open_writer( self ):
        return _Open( self )
    
    
    def __str__( self ):
        return "EchoingEndpoint"


class _Open( Writer ):
    def __init__( self, owner: _EchoingEndpoint ):
        super().__init__()
        self.owner = owner
        
        t = self.name
        if "/" in t:
            t = t.split( "/", 1 )[1]
        self.__print( "+++ OPENED {}".format( t ) )
    
    
    def on_write_folder( self, name: str ) -> "Destination":
        self.__print( "[F] “{}”".format( name ) )
        return type( self )( self.name + "/" + name )
    
    
    def on_write_data( self, data: object ):
        self.__print( "[D] {}".format( data ) )
    
    
    def on_write_edge( self, edge: NcEdge ):
        self.__print( "[E] {}".format( edge ) )
        self.__print_properties( edge.properties )
    
    
    def on_write_node( self, node: NcNode ):
        self.__print( "[N] {}".format( node ) )
        self.__print_properties( node.properties )
    
    
    def on_close( self ) -> None:
        self.__print( "--- CLOSED" )
    
    
    def __print( self, message: str ):
        print( "+++ {}) {}".format( self.name.ljust( 20, "." ), message ) )
    
    
    def __print_properties( self, properties: Dict[str, object] ):
        if not properties.items():
            return
        
        items = sorted( properties.items(), key = lambda x: str( x[0] ) )
        longest = max( len( str( item[0] ) ) for item in items )
        
        for k, v in items:
            print( "{})            {} = {}".format( self.name, str( k ).ljust( longest ), v ) )


ECHOING_ENDPOINT = _EchoingEndpoint()
