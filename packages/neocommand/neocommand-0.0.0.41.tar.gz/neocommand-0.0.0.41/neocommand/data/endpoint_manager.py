"""
Classes for managing "parcels" - folders that contain a formatted set of entries to be added to the database
"""

from intermake.engine.environment import Controller


__author__ = "Martin Rusilowicz"

from typing import List, cast, Optional, Iterator, Tuple
from warnings import warn
from neocommand.endpoints.db_endpoint import DatabaseEndpoint
from neocommand.endpoints.abstract_endpoints import Endpoint, Destination
from mhelper import NotFoundError, ExistsError


class EndpointManager:
    """
    Manages pipeline folders
    """
    
    
    def __init__( self ) -> None:
        """
        CONSTRUCTOR
        See methods of same name for parameter details
        """
        self.__user_endpoints = cast( List[Endpoint], Controller.ACTIVE.app.local_data.retrieve( "user_endpoints", [] ) )
        self.__other_endpoints = []
        self.__temporary_endpoints = []
        self.__num_temporary_endpoints = 0
        
        # Normally, endpoints should be registered externally, but we register these defaults here because they also rely on us
        from neocommand.endpoints import NULL_ENDPOINT, ECHOING_ENDPOINT
        self.register( NULL_ENDPOINT )
        self.register( ECHOING_ENDPOINT )
    
    
    def find_endpoint( self, name: str ) -> Optional[Endpoint]:
        for endpoint in self:
            if endpoint.name == name:
                return endpoint
        
        return None
    
    
    def register( self, endpoint: Endpoint ):
        self.__other_endpoints.append( endpoint )
    
    
    @property
    def user_endpoints( self ) -> Tuple[Endpoint, ...]:
        return tuple( self.__user_endpoints )
    
    
    def rename_user_endpoint( self, endpoint: Endpoint, new_name: str ):
        if endpoint not in self.__user_endpoints:
            raise NotFoundError( "Only user-defined endpoints can be renamed. «{}» is not a user endpoint.".format( endpoint.name ) )
        
        endpoint.name = new_name
    
    
    def remove_user_endpoint( self, endpoint: Endpoint, delete: bool ):
        """
        Removes the specified endpoint from the user endpoint collection.
        """
        if endpoint not in self.__user_endpoints:
            raise NotFoundError( "Only user-defined endpoints can be removed. «{}» is not a user endpoint.".format( endpoint.name ) )
        
        try:
            endpoint.on_removed( delete )
        except Exception as ex:
            raise ValueError( "«{}» has not been removed due to a previous error.".format( endpoint.name ) ) from ex
        
        try:
            self.__user_endpoints.remove( endpoint )
        except ValueError as ex:
            raise ValueError( "«{}» is not in the list of endpoints. Perhaps it has already been deleted?".format( endpoint.name ) ) from ex
        
        self.__save_endpoints()
    
    
    def __save_endpoints( self ) -> None:
        Controller.ACTIVE.app.local_data.store.commit( "user_endpoints", self.__user_endpoints )
    
    
    def add_user_endpoint( self, endpoint: Endpoint ) -> None:
        for x in self:
            if x.name == endpoint.name:
                raise ExistsError( "The new endpoint has not been added:"
                                       "The endpoint name «{}» is already in use, "
                                       "please use a different name. ".format( x.name ) )
        
        self.__user_endpoints.append( endpoint )
        self.__save_endpoints()
    
    
    def __len__( self ):
        return len( self.__user_endpoints ) + len( self.__temporary_endpoints ) + len( self.__other_endpoints )
    
    
    def __str__( self ) -> str:
        return "{} endpoints".format( len( self ) )
    
    
    def __iter__( self ) -> Iterator[Endpoint]:
        yield from self.__other_endpoints
        yield from self.__user_endpoints
        yield from self.__temporary_endpoints
    
    
    def get_temporary_destination( self ) -> Destination:
        self.__num_temporary_endpoints += 1
        name = "temp{}".format( self.__num_temporary_endpoints )
        from neocommand.endpoints import MemoryEndpoint
        ep = MemoryEndpoint( name )
        self.__temporary_endpoints.append( ep )
        
        if len( self.__temporary_endpoints ) > 3:
            self.__temporary_endpoints.pop( 0 )
        
        return ep
    
    
    def get_database_endpoint( self, tolerant = False ) -> Optional[DatabaseEndpoint]:
        database = None
        
        for ep in self:
            if isinstance( ep, DatabaseEndpoint ):
                if database is not None:
                    message = "Problem obtaining default database: I found multiple «DatabaseEndpoint»s that could act as a reasonable default. Perhaps you meant to specify the a database explicitly?"
                    
                    if tolerant:
                        warn( message, UserWarning )
                        return None
                    
                    raise ValueError( message )
                
                database = ep
        
        if database is None:
            message = "Problem obtaining default database: I could not find any «DatabaseEndpoint» to act as a reasonable default. Perhaps you meant to call «open_database» first?"
            
            if tolerant:
                warn( message, UserWarning )
                return None
            
            raise ValueError( message )
        
        return database
