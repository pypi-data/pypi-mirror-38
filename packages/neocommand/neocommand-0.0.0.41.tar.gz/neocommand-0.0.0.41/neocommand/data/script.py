"""
Contains the `ScriptCommand` class, an extension of the `intermake` package's `Command` that
represents re-usable Cypher/SQL scripts.
"""
from typing import Optional, Sequence
from mhelper import NOT_PROVIDED, MAnnotation, ArgInspector

import intermake

from neocommand.endpoints import Destination, DatabaseEndpoint


__author__ = "Martin Rusilowicz"

# isDbParam - used to denote arguments in ScriptPlugins that are passed as database arguments (i.e. direct to Neo4j).
# Replaces {xyz} in the script. The better option but Neo4j doesn't support this in all cases.
isDbParam = MAnnotation( "isDbParam" )

# isScriptParam - used to denote arguments in ScriptPlugins that are passed as a text replacement in the script.
# Replaces <XYZ> in the script.
isScriptParam = MAnnotation( "isScriptParam" )

TScriptTypes = "Union[ Type[ isDbParam ], Type[ isScriptParam ] ]"
TScriptParam = "Union[ TScriptTypes, Tuple[ TScriptTypes, object ] ]"


class ScriptCommand( intermake.Command ):
    """
    Wraps text with replaceable parameters up with some error checking

    These "parameters" are just text and should represent constants as far as the database is concerned.
    They should not be confused with, or used as a substitute for, database query parameters.
    
    The class vars marked ``(special)`` define the names of six special arguments common to all scripts.
    These arguments are documented during their instantiation in the constructor.
    
    :ivar filename:                 If the script was loaded from a file, this is the path to that file.
                                    This is `None` for scripts created in Python.
    :ivar direct_replace_args:      The subset of the ctor `args` that have the `isScriptParam` annotation.
                                    These define the arguments which are replaced in the script text.
    :ivar database_param_args:      The subset of the ctor `args` that have the `isDbParam` annotation.
                                    These define the arguments which are passed to the database driver.
    :ivar plain_text:               This is the unprocessed Cypher/SQL code, which may still contain
                                    placeholders if there are any `direct_replace_args`.
                                    
    :cvar ARG_QUIET:                (special)
    :cvar ARG_RETRIES:              (special)
    :cvar ARG_TIMEOUT:              (special)
    :cvar ARG_OUTPUT:               (special)
    :cvar ARG_DATABASE:             (special)
    :cvar ARG_DUMP:                 (special)
    """
    ARG_QUIET = "quiet"
    ARG_RETRIES = "retries"
    ARG_TIMEOUT = "timeout"
    ARG_OUTPUT = "output"
    ARG_DATABASE = "database"
    ARG_DUMP = "dump"
    
    
    def __init__( self,
                  *,
                  cypher: str,
                  args: Sequence[ArgInspector] = None,
                  timeout: int = 0,
                  retries: int = 1000,
                  filename: Optional[str] = None,
                  **kwargs ):
        """
        CONSTRUCTOR
        
        :param cypher:              Script text.
                                    This may contain placeholders as defined by the `args`.
        :param args:                Inherited from `Command`.
                                    Additionally, all `args` to a `ScriptCommand` must be annotated
                                    as either `isScriptParam` or `isDbParam`, designating how they
                                    are to be used. `isScriptParam` arguments replace the
                                    placeholders in the `cypher` text, whilst `isDbParam` are passed
                                    to the database.
        :param timeout:             Timeout when executing this script with the database.
                                    The default of 0 denotes no (an infinite) timeout. 
        :param retries:             How many times to retry if the operation times out or the
                                    connection fails.
        :param filename:            If the script was loaded from a file, this is the path to that
                                    file. This has no bearing on the script and is only used for
                                    reference. This is `None` for scripts created directly in
                                    Python.
        :param kwargs:              Passed to `Command.__init__`.
        """
        from neocommand.endpoints import ECHOING_ENDPOINT
        
        # Filename
        self.filename = filename
        
        # Arguments
        fa = list( args ) if args is not None else []
        self.direct_replace_args = set()
        self.database_param_args = set()
        
        for arg in fa:
            if arg.annotation.is_mannotation_of( isScriptParam ):
                self.direct_replace_args.add( arg.name )
            elif arg.annotation.is_mannotation_of( isDbParam ):
                self.database_param_args.add( arg.name )
            else:
                raise ValueError( "The arguments of a `ScriptCommand` should be annotated using «{}» or «{}» arguments, "
                                  "but this one has a «{}» argument. "
                                  "Please add the correct annotation to the code."
                                  .format( isScriptParam, isDbParam, arg.annotation ) )
        
        from neocommand.endpoints import DatabaseEndpoint, Destination
        fa.extend( (ArgInspector( self.ARG_DATABASE, Optional[DatabaseEndpoint], None, "Database to use. If this is `None` a reasonable default will be assumed." ),
                    ArgInspector( self.ARG_OUTPUT, Destination, ECHOING_ENDPOINT, "Where to send received data." ),
                    ArgInspector( self.ARG_TIMEOUT, int, timeout, "Parameter available to all scripts. Query timeout in seconds, use zero for no timeout." ),
                    ArgInspector( self.ARG_RETRIES, int, retries, "Parameter available to all scripts. Number of retries after timeouts before the query is considered a failure" ),
                    ArgInspector( self.ARG_QUIET, bool, False, "Don't display results in terminal." ),
                    ArgInspector( self.ARG_DUMP, bool, False, "Dump the script's code to standard output instead of running it." )) )
        
        super().__init__( **kwargs,
                          args = fa )
        
        # Cypher
        if not cypher:
            raise ValueError( "A {} needs some code.".format( repr( self ) ) )
        
        self.plain_text = cypher
    
    
    def on_run( self, **kwargs ) -> object:
        """
        FINAL OVERRIDE
        """
        #
        # GET ARGUMENTS
        #
        arg_dump: bool = kwargs.get( self.ARG_DUMP )
        arg_database: DatabaseEndpoint = kwargs.get( self.ARG_DATABASE )
        arg_timeout: int = kwargs.get( self.ARG_TIMEOUT )
        arg_retries: int = kwargs.get( self.ARG_RETRIES )
        arg_output: Destination = kwargs.get( self.ARG_OUTPUT )
        arg_quiet: bool = kwargs.get( self.ARG_QUIET )
        
        if arg_database is None:
            from neocommand.data.core import get_core
            arg_database = get_core().endpoint_manager.get_database_endpoint()
        
        #
        # GET CYPHER TEXT
        #
        cypher = self.create( kwargs )
        
        cypher_params = { }
        
        for name, value in kwargs.items():
            if name in self.database_param_args:
                cypher_params[name] = value
        
        #
        # SPECIAL CASE FOR CYPHER DUMP
        #
        if arg_dump:
            print( cypher )
            
            for k, v in cypher_params.items():
                print( "{} = {}".format( k, v ) )
            
            return None
        
        #
        # RUN THE SCRIPT!
        #
        with arg_database.open_connection() as db:
            with arg_output.open_writer() as writer:
                result = db.run_cypher( title = self.name,
                                        cypher = cypher,
                                        parameters = cypher_params,
                                        time_out = arg_timeout,
                                        retry_count = arg_retries,
                                        output = writer )
            
            if not arg_quiet:
                print( "----{}".format( result ) )
            
            return result
    
    
    def create( self,
                kwargs,
                ignore_missing: bool = False ) -> str:
        """
        Generates Cypher/SQL text from this script.
        
        :param kwargs:              Script direct-replace parameters 
        :param ignore_missing:      Whether to permit parameter placeholders to occur in the output.
        :return:                    Script text 
        """
        return self._create_from( self.plain_text, kwargs, ignore_missing )
    
    
    def _create_from( self,
                      statement: str,
                      kwargs,
                      ignore_missing: bool ) -> str:
        """
        Logic behind create().
        """
        
        for name, value in kwargs.items():
            if name in self.direct_replace_args:
                key = "<" + name.upper() + ">"
                
                # Assert parameter exists
                if value is NOT_PROVIDED:
                    if ignore_missing:
                        value = "{????}"
                    else:
                        raise ValueError( "The parameter «{0}» has not been provided.".format( name ) )
                
                statement = statement.replace( key, str( value ) )
        
        return statement
