from typing import cast

from intermake import Controller


__author__ = "Martin Rusilowicz"


class Core:
    """
    All the data.
    
    See the accessor properties for private field descriptions.
    """
    
    
    def __init__( self, application ):
        """
        CONSTRUCTOR
        """
        self.__application = application
        self.__endpoints = None
        self.__schema = None
    
    
    @property
    def schema( self ):
        """
        Obtains the known set of node labels, edge types, and properties.
        
        We use this to make suggestions to the user but the set cannot always be guaranteed
        to be up to date or complete.
        """
        from neocommand.helpers.schema_helper import DatabaseSchema
        
        if self.__schema is None:
            self.__schema = self.__application.local_data.retrieve( "schema", DatabaseSchema() )
        
        return cast( DatabaseSchema, self.__schema )
    
    
    @property
    def endpoint_manager( self ):
        from neocommand.data.endpoint_manager import EndpointManager
        
        if self.__endpoints is None:
            self.__endpoints = EndpointManager()
        
        return cast( EndpointManager, self.__endpoints )


def get_core():
    return Controller.ACTIVE.app.core
