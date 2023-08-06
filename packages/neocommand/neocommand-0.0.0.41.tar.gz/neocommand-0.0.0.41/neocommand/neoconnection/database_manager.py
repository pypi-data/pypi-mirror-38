"""
Connecting to the database, executing queries, and conversion of results.
"""
import threading
from threading import Thread
from time import sleep, time
from typing import Callable, Dict
from warnings import warn
from intermake import pr, Streaming
from mhelper import override
from neocommand.data import isDriverName
from neocommand.endpoints.abstract_endpoints import Writer


__author__ = "Martin Rusilowicz"


class DbStats:
    """
    Simple type - statistics on a query
    """
    __props = ("relationships_deleted", "constraints_added", "nodes_created", "labels_added", "nodes_deleted", "constraints_removed", "relationships_created", "indexes_removed", "indexes_added", "labels_removed", "properties_set")
    
    
    def __init__( self, cypher: str, parameters: dict, output: Writer, dictionary: Dict[str, object] ):
        """
        CONSTRUCTOR
        :param cypher:      Cypher query 
        :param dictionary:  Dictionary of statistics.
                            See instance variables.
        """
        self.cypher = cypher
        self.parameters = parameters
        self.endpoint = output
        self.relationships_deleted = dictionary.get( "relationships_deleted", 0 )
        self.constraints_added = dictionary.get( "constraints_added", 0 )
        self.contains_updates = dictionary.get( "contains_updates", False )
        self.nodes_created = dictionary.get( "nodes_created", 0 )
        self.labels_added = dictionary.get( "labels_added", 0 )
        self.nodes_deleted = dictionary.get( "nodes_deleted", 0 )
        self.constraints_removed = dictionary.get( "constraints_removed", 0 )
        self.relationships_created = dictionary.get( "relationships_created", 0 )
        self.indexes_removed = dictionary.get( "indexes_removed", 0 )
        self.indexes_added = dictionary.get( "indexes_added", 0 )
        self.labels_removed = dictionary.get( "labels_removed", 0 )
        self.properties_set = dictionary.get( "properties_set", 0 )
        self.relationships_deleted = dictionary.get( "relationships_deleted", 0 )
    
    
    def __str__( self ):
        ss = []
        
        for prop in self.__props:
            if self.__dict__[prop]:
                ss.append( "{} {}".format( self.__dict__[prop], prop ) )
        
        if not ss:
            return "No changes"
        
        return ", ".join( ss )
    
    
    def __repr__( self ):
        return "{}({})".format( type( self ).__name__, self )
    
    
    def as_dict( self ):
        return dict( (x, y) for x, y in self.__dict__.items() if x in self.__props )
    
    


class IDbDriverSession:
    """
    Base class for driver wrappers.
    Driver wrappers convert the drivers into a common format.
    
    The wrapper need should implement:
        * the `run` function
        * a constructor taking a `DbManager` instance.
            The constructor need not be provided if the driver wrapper is registered to
            `DbManager.DRIVER_CLASSES` using a callable function (taking a `DbManager`
            instance) rather than the `IDbDriverSession` class itself.
    """
    
    
    def run( self, cypher: str, parameters: dict, database: "DbManager", output: Writer ) -> DbStats:
        """
        Requests the wrapper execute the script.
        
        :param cypher:          Script to execute. 
        :param parameters:      Parameters on the script. 
        :param database:        Back-reference to the executing database. 
        :param output:          An `Destination` into which the results of the execution should be inserted.
        :return:                A `DbStats` object denoting what has changed. 
        """
        raise NotImplementedError( "abstract" )


class DbManager:
    """
    Connects to the Neo4j database and executes queries
    
    :cvar _count:               Index of instance
    :cvar DRIVER_CLASSES:       List of possible driver wrappers and their associated names.
                                This field should be added to externally in order to register new driver wrappers.
                                Key:    Driver name
                                Value:  Either the driver class or a function returning a driver instance
    """
    
    _count = 0
    DRIVER_CLASSES: Dict[str, Callable[["DbManager"], IDbDriverSession]] = { }
    
    
    def __init__( self, driver: isDriverName, remote_address: str, user_name: str, password: str, remote_port: str ):
        """
        CONSTRUCTOR
        """
        DbManager._count += 1
        
        self.__index = self._count
        self.__cached_session: IDbDriverSession = None
        self.driver_name = driver
        self.remote_address = remote_address
        self.remote_port = remote_port
        self.user_name = user_name
        self.password = password
    
    
    def run_cypher( self,
                    title: str,
                    cypher: str,
                    output: Writer,
                    parameters: Dict[str, object] = None,
                    time_out: float = 604800,
                    retry_count: int = 9999 ) -> DbStats:
        """
        Runs a cypher procedure
        
        :param title: Title (for progress indicator) 
        :param cypher: Procedure text  
        :param parameters: Parameters on the procedure
        :param time_out: Timeout, in seconds 
        :param retry_count: How many times to retry 
        :param output: Where to send any output
        :return: Results dependent on results_mode.
        """
        
        session = self.__get_session()
        
        if parameters is None:
            parameters = { }
        
        
        def __thread_function():
            threading.currentThread().name = "thread_function_in_run_cypher_{}".format( title.replace( "_", " " ) )
            
            try:
                return session.run( cypher, parameters, self, output )  # note: any additional traceback at this point typically stops at the thread call
            except Exception as ex:
                ss = []
                ss.append( "Query failed:\n" )
                ss.append( "[EXCEPTION]\n" )
                ss.append( str( ex ) )
                ss.append( "\n\n" )
                ss.append( "[CYPHER]\n" )
                ss.append( cypher )
                ss.append( "\n\n" )
                ss.append( "[PARAMETERS]\n" )
                ss.append( "\n".join( "{}={}".format( k, v ) for k, v in parameters.items() ) )
                ss.append( "\n" )
                raise ValueError( "".join( ss ) ) from ex
        
        
        while True:
            worker_thread = DbManager.__FnThread( __thread_function )
            worker_thread.start()
            start_time = time()
            
            worker_thread.join( 5 )
            
            if not worker_thread.is_completed:
                # No result after 5 seconds - show that we are still busy
                with pr.pr_action( "Cypher: " + title ) as proggy:
                    while True:
                        worker_thread.join( 2 )  # 5 seconds is too long for iTerm to recognise that we are still alive, creating a somewhat irritating flickering timer icon. Use 2 seconds instead.
                        proggy.still_alive()
                        
                        if worker_thread.is_completed:
                            break
                        
                        if time_out:
                            elapsed_time = time() - start_time
                            
                            if elapsed_time > time_out:
                                break
            
            if time_out:
                if not worker_thread.is_completed:
                    # Timed out - our timer - no result was stored
                    try_again = True
                elif isinstance( worker_thread.exception, TimeoutError ):
                    # Timed out - Neo4j/HTTP timer - someone probably pulled out the network cable halfway through :(
                    try_again = True
                else:
                    # Some other error - fail
                    try_again = False
            else:
                # No timeout set - fail for anything (even a Neo4j timeout - we'll raise it as an exception further down
                try_again = False
            
            if try_again:
                # Timed out
                # - Drop the session, it's dead :(
                self.__cached_session = None
                retry_timer = 60
                retry_count -= 1
                
                if retry_count < 0:
                    warn( "Query timed out after {0} seconds. No retries remaining.".format( time_out ), UserWarning )
                    raise TimeoutError( "Database access timed out after {0} seconds. Please check that you are connected to the database. If you didn't expect this message you may wish to simplify your query or increase the timeout period. The query text follows: ".format( time_out ) + cypher )
                
                warn( "Query timed out after {0} seconds. {1} retries remaining, retrying in {2} seconds".format( time_out, retry_count, retry_timer ), UserWarning )
                
                with pr.pr_action( "Query timed out, retrying shortly", retry_timer ) as action:
                    for i in range( 0, retry_timer ):
                        action.increment()
                        sleep( 1 )
            else:
                break
        
        if worker_thread.exception is not None:
            # Session might be dead, drop it
            self.__cached_session = None
            raise worker_thread.exception
        
        return worker_thread.result
    
    
    def __is_connected( self ) -> bool:
        """
        Are we connected to the database?
        :return: 
        """
        return self.__cached_session is not None
    
    
    @override
    def __str__( self ):
        """
        String representation
        """
        return "Db#{0}( connection = {1} \)".format( self.__index, "Established" if self.__is_connected() else "Pending" )
    
    
    class __FnThread( Thread ):
        def __init__( self, fn: Callable[[], DbStats] ):
            """
            CONSTRUCTOR
            Simple function-as-thread
            """
            super().__init__()
            self._fn = fn
            self.is_completed: bool = False
            self.result: DbStats = None
            self.exception: Exception = None
            self.incoming_target = Streaming.INSTANCE.get_target()
        
        
        def run( self ):
            Streaming.target = self.incoming_target # TODO: This is dirty as it assumes the target is always going to be thread-safe
            
            try:
                self.result = self._fn()
                assert self.result is not None
            except Exception as ex:
                self.exception = ex
            
            self.is_completed = True
    
    
    def __get_session( self ) -> IDbDriverSession:
        """
        Obtains the active database session, connecting to the database if required
        Raises on failure
        """
        if self.__cached_session:
            return self.__cached_session
        
        fn_driver = self.DRIVER_CLASSES.get( self.driver_name )
        driver = fn_driver( self )
        
        if not driver:
            raise ValueError( "No such driver as «{}».", self.driver_name )
        
        # Assert the connection
        from neocommand.endpoints import MemoryEndpoint
        ep = MemoryEndpoint( "test" )
        
        with ep.open_writer() as writer:
            driver.run( "RETURN 1", { }, self, writer )
            
        check = ep.contents[0]
        
        if check.value != 1:
            raise ConnectionError( "Unexpected result from server «{0}» «{1}».".format( type( check ).__name__, check ) )
        
        self.__cached_session = driver
        return self.__cached_session
