from os import path
from typing import Dict, Optional, cast
from mhelper import ManagedPassword, ManagedWith, NotSupportedError, TTristate, array_helper

import warnings

from neocommand.data import NcEdge, NcNode, isDriverName, constants
from neocommand.endpoints.abstract_endpoints import AddFailedError, Destination, Writer, Reader
from neocommand.endpoints.null_endpoint import NULL_ENDPOINT
from neocommand.endpoints.memory_endpoint import MemoryEndpoint


_DbManager = "neocommand.database.database_manager.DbManager"
KEYRING_NAME = "neocommand"


class DatabaseEndpoint( Destination ):
    """
    A read/write endpoint that reads and writes data to and from the database
    
    .. note::
    
        Even though this endpoint is used to write to the database (via its `open_connection`),
        it isn't actually an `Origin` because it does not support reading the entire
        database via `origin_get_all` (which would be incredibly slow).
    """
    
    
    def __init__( self,
                  *,
                  name: str,
                  driver: isDriverName,
                  remote_address: str,
                  user_name: str,
                  password: str,
                  directory: Optional[str],
                  is_unix: Optional[bool],
                  port: str,
                  keyring: bool,
                  managed_password: ManagedPassword = None ):
        """
        CONSTRUCTOR
        :param name:                  Endpoint name
        :param driver:                Connection details
        :param remote_address:        Connection details
        :param user_name:             Connection details
        :param password:              Connection details.
        :param directory:             Connection details
        :param is_unix:               Connection details
        :param port:                  Connection details
        """
        super().__init__( name )
        
        self.driver = driver
        self.remote_address = remote_address
        self.user_name = user_name
        self.directory = directory
        self.is_unix = is_unix
        self.port = port
        
        if managed_password:
            self.managed_password = managed_password
        else:
            from uuid import uuid4
            self.managed_password = ManagedPassword( password = password,
                                                     keyring = KEYRING_NAME,
                                                     key = "DatabaseEndpoint('{}', '{}', '{}')".format( self.user_name, self.remote_address, uuid4() ),
                                                     managed = keyring )
        
        self.__connections = []
        self.__used_connections = []
    
    
    def get_directory( self ) -> str:
        if self.directory:
            return self.directory
        
        raise NotSupportedError( "Cannot obtain the Neo4j directory because the directory was not specified when the DatabaseEndpoint was created." )
    
    
    def get_binary_directory( self ) -> str:
        return path.join( self.get_directory(), "bin" )
    
    
    def get_neo4j_exe( self, name = "neo4j" ):
        r = path.join( self.get_binary_directory(), name )
        
        if self.is_windows:
            r += ".exe"
        
        return r
    
    
    @property
    def is_windows( self ):
        return not self.is_unix
    
    
    def get_import_directory( self ) -> str:
        return path.join( self.get_directory(), "import" )
    
    
    def get_is_unix( self ) -> bool:
        if self.is_unix is not None:
            return self.is_unix
        
        raise NotSupportedError( "Cannot determine if Neo4j is running under Windows or Unix because that was not specified when the DatabaseEndpoint was created." )
    
    
    def __getstate__( self ) -> Dict[str, object]:
        return { "name"          : self.name,
                 "driver"        : self.driver,
                 "remote_address": self.remote_address,
                 "user_name"     : self.user_name,
                 "password"      : self.managed_password,
                 "directory"     : self.directory,
                 "is_unix"       : self.is_unix,
                 "port"          : self.port }
    
    
    def __setstate__( self, state: Dict[str, object] ) -> None:
        self.__init__( name = cast( str, state["name"] ),
                       driver = cast( str, state["driver"] ),
                       remote_address = cast( str, state["remote_address"] ),
                       user_name = cast( str, state["user_name"] ),
                       password = "",
                       managed_password = cast( ManagedPassword, state["password"] ),
                       directory = cast( Optional[str], state["directory"] ),
                       is_unix = cast( TTristate, state["is_unix"] ),
                       port = cast( str, state["port"] ),
                       keyring = True )
    
    
    def on_removed( self, delete: bool ) -> None:
        super().on_removed( delete )
        self.managed_password.delete()
    
    
    def __str__( self ) -> str:
        return "Database: {}@{}".format( self.user_name, self.remote_address )
    
    
    def _acquire_manager( self ) -> _DbManager:
        if not self.__connections:
            from neocommand.neoconnection.database_manager import DbManager
            self.__connections.append( DbManager( self.driver, self.remote_address, self.user_name, self.managed_password.password, self.port ) )
        
        result = self.__connections.pop()
        self.__used_connections.append( result )
        return result
    
    
    def _release_manager( self, manager: _DbManager ) -> None:
        self.__used_connections.remove( manager )
        self.__connections.append( manager )
    
    
    def open_connection( self ):
        """
        Opens a connection to a `DbManager` that allows you to control Neo4j.
        
        TODO: This is not the same as `open_writer`, which prepares an endpoint for writing, but it
              should be.
        
        usage::
        ```
        with ep.open_connection() as db:
            assert isinstance( db, DbManager )
            db.run_cypher( ... )
        ```
        """
        from neocommand.neoconnection.database_manager import DbManager
        x: ManagedWith[DbManager] = ManagedWith( on_get_target = self.__acquire_manager, on_exit = self._release_manager )
        return x
    
    
    def on_open_writer( self ):
        return _DatabaseEndpointWriter( self )
    
    
    def on_open_reader( self ):
        return _DatabaseEndpointReader( self )


class _DatabaseEndpointReader( Reader ):
    def __index__( self, owner: DatabaseEndpoint ):
        self.owner = owner
        self.connection = owner._acquire_manager()
    
    
    def on_close( self ):
        self.owner._release_manager( self.connection )
    
    
    def on_read_all_props( self, label: str, property: str ):
        ep = MemoryEndpoint()  # TODO: Inefficient, we should iterate, not keep everything
        
        with ep.open_writer() as dest:
            self.connection.run_cypher( title = "Reading {}/{}".format( label, property ),
                                        cypher = "MATCH (n:{}) RETURN n.`{}`, n.`{}`".format( label, constants.PRIMARY_KEY, property ),
                                        output = dest )
        
        return array_helper.deinterleave_as_list( ep.contents )  # TODO: Check


class _DatabaseEndpointWriter( Writer ):
    def __init__( self, owner: DatabaseEndpoint ):
        super().__init__()
        self.owner = owner
        self.connection = owner._acquire_manager()
    
    
    def on_close( self ):
        self.owner._release_manager( self.connection )
    
    
    def on_write_folder( self, _: str ) -> "Destination":
        return self
    
    
    def on_write_data( self, data: object ):
        warnings.warn( "This endpoint «{}» does not support the adding of arbitrary (non-node/edge) data «{}». This action has been ignored.".format( self, data ) )
    
    
    def on_write_edge( self, edge: NcEdge ):
        args = []
        for k in edge.properties.keys():
            args.append( "r.`" + k + "` = {" + k + "}" )
        
        args = ",".join( args )
        
        if args:
            args = " SET " + args
        
        text = "MATCH (n:`" + edge.start.label + "` {uid:{start_uid}}), (m:`" + edge.end.label + "` {uid:{end_uid}}) MERGE (n)-[r:`" + edge.label + "`]->(m)" + args
        
        # noinspection PyTypeChecker
        parameters = dict( edge.properties.items() )
        parameters["start_uid"] = edge.start.uid
        parameters["end_uid"] = edge.end.uid
        
        stats = None
        
        try:
            stats = self.connection.run_cypher( title = "Create edge",
                                                cypher = text,
                                                parameters = parameters,
                                                output = NULL_ENDPOINT )
            
            if stats.nodes_created != 0:
                raise AddFailedError( "stats.nodes_created is {0} (expected 0)".format( stats.nodes_created ) )
                
                # if stats.relationships_created != 1:
                #     raise AddFailedError( "stats.relationships_created is {0} (expected 1)".format( stats.relationships_created ) )
        
        except Exception as ex:
            raise AddFailedError( "Failed to add the edge due to the error «{0}». Properties: ({1} {2})-[{3}]>({4} {5}) {6}. Stats: {7}".format( ex, edge.start.label, edge.start.uid, edge.label, edge.end.label, edge.end.uid, edge.properties, stats ) ) from ex
    
    
    def on_write_node( self, node: NcNode ):
        args = []
        # noinspection PyTypeChecker
        parameters = dict( node.properties.items() )
        parameters["uid"] = node.uid
        
        for k in parameters.keys():
            args.append( "n.`" + k + "` = {" + k + "}" )
        
        args = ",".join( args )
        
        if args:
            args = " SET " + args
        
        text = "MERGE (n:`" + node.label + "` {uid: {uid}})" + args
        
        stats = None
        
        try:
            stats = self.connection.run_cypher( title = "Create node",
                                                cypher = text,
                                                parameters = parameters,
                                                output = NULL_ENDPOINT )
            
            # if stats.nodes_created != 1:
            #     raise AddFailedError( "stats.nodes_created is {0} (expected 1)".format( stats.nodes_created ) )
        except Exception as ex:
            raise AddFailedError( "Failed to add a database node due to the error «{0}». Label: «{1}»\nProperties: «{2}»\nStats: {3}".format( ex, node.label, node.properties, stats ) ) from ex
