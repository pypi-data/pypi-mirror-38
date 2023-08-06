"""
The set of core $(APP_NAME) commands.

Use `cmdlist` to obtain the list of most commonly used commands.
"""
import re
import time
from warnings import warn
from collections import namedtuple
from os import path
from typing import List, Optional, Tuple
from intermake import Theme, visibilities, pr
from mhelper import MEnum, file_helper, string_helper
from neocommand import get_core, DbManager, DbStats, MemoryEndpoint
from neocommand.application import app
from neocommand.data.script import ScriptCommand
from neocommand.endpoints import Destination, DatabaseEndpoint


__author__ = "Martin Rusilowicz"


class ENeo4jCommand( MEnum ):
    NONE = 0
    START = 1
    STOP = 2
    RESTART = 3
    STATUS = 4
    VERSION = 5


@app.command( visibility = visibilities.ADVANCED )
def set_database( server: DatabaseEndpoint,
                  database: Optional[str] = None
                  ) -> str:
    """
    Displays and optionally changes the neo4j database.
    Note that Neo4j must be restarted in order for this to take effect.
    
    :param server: Database to modify 
    :param database: OPTIONAL. New database to use. Leave blank for unchanged.
    :return: if `restart` is passed     : The object returned from `neo4j`.
             else a tuple of `(EBinStatus.QUERY, <database>)`
    """
    if not server.directory:
        raise ValueError( "Cannot display or set the database when `endpoint.directory` has not been provided." )
    
    file_name = path.join( server.directory, "conf", "neo4j.conf" )
    text = file_helper.read_all_text( file_name )
    
    PATTERN = "[#]?dbms\.active_database=.*"
    rx = re.search( PATTERN, text )
    current_db = rx.group( 0 ).split( "=", 1 )[1]
    
    pr.printx( "<verbose>INI: {}</verbose>".format( rx.group( 0 ) ) )
    pr.printx( "<verbose>CURRENT VALUE: {}</verbose>".format( current_db ) )
    
    if database:
        text = re.sub( PATTERN, "dbms.active_database=" + database, text, 1 )
        
        file_helper.recycle_file( file_name )
        file_helper.write_all_text( file_name, text )
        
        pr.printx( "<verbose>NEW VALUE: {}</verbose>".format( database ) )
    
    return current_db


Neo4jStatus = namedtuple( "Neo4jStatus", ["endpoint", "database", "is_running", "is_connected", "version", "error"] )


@app.command()
def test_connection( server: DatabaseEndpoint ) -> Neo4jStatus:
    """
    Tests the database connection.
    
    :param server:    Connection to test 
    :return:          Connection status 
    """
    if server.directory:
        # Get the database
        current_database = set_database( server )
        
        # Get the version
        version = control_server( server, ENeo4jCommand.VERSION )
        
        # Get the server status
        is_running = "Neo4j is running" in control_server( server, ENeo4jCommand.STATUS )
    else:
        current_database = ""
        version = ""
        is_running = None
    
    # Test the connection
    if is_running is True or is_running is None:
        is_connected = None
        error = None
        
        for n in pr.pr_iterate( range( 10 ), "Attempting connection" ):  # keep trying because if we've just turned the server on it might take a while
            if n > 0:
                time.sleep( 1 )
            
            try:
                __check_connection( server )
                is_connected = True
                error = None
                break
            except Exception as ex:
                is_connected = False
                error = str( ex )
    else:
        is_connected = False
        error = None
    
    return Neo4jStatus( server, current_database, is_running, is_connected, version, error )


def __check_connection( endpoint: DatabaseEndpoint ):
    from neocommand.endpoints.memory_endpoint import MemoryEndpoint
    ep = MemoryEndpoint( "test" )
    
    with ep.open_writer() as writer:
        with endpoint.open_connection() as db:
            db.run_cypher( cypher = "RETURN 1",
                           output = writer,
                           title = "Testing connection" )
    
    if ep.contents[0].value == 1:
        return True
    
    raise ValueError( "Unexpected result from server." )


@app.command( names = ["server"], visibility = visibilities.ADVANCED )
def control_server( server: DatabaseEndpoint, command: ENeo4jCommand = ENeo4jCommand.NONE ) -> str:
    """
    Starts or stops neo4j

    :param server: Database to control
    :param command: The command to issue to Neo4j.
    
    :return The output from the command.
    """
    if not server.directory:
        raise ValueError( "Cannot run server commands when `endpoint.directory` is not set" )
    
    from intermake.helpers import subprocess_helper
    args = [server.get_neo4j_exe()]
    
    if command != ENeo4jCommand.NONE:
        args.append( command.name.lower() )
    
    out = []
    subprocess_helper.run_subprocess( args, collect = out.append, no_err = True )
    out = "\n".join( out )
    
    if command == ENeo4jCommand.NONE:
        okay = bool( re.search( "{ (.*) }", out ) )
    elif command == ENeo4jCommand.STATUS:
        okay = "Neo4j is running" in out or "Neo4j is not running" in out
    elif command == ENeo4jCommand.VERSION:
        okay = bool( out )
    elif command == ENeo4jCommand.START:
        okay = bool( re.search( "Active database: (.*)", out ) )
    elif command == ENeo4jCommand.STOP:
        okay = "stopped" in out
    else:
        okay = False
    
    if not okay:
        warn( "Output from Neo4j did not match the expected output.", UserWarning )
    
    return out


@app.command( visibility = visibilities.ADVANCED )
def save_script( file_name: str, script: ScriptCommand ):
    """
    Saves a ScriptCommand's script to a file
    
    :param file_name: Where to save the file. Defaults to ".cypher" extension. 
    :param script: Script to save
    """
    
    file_name = file_helper.default_extension( file_name, ".cypher" )
    
    file_helper.write_all_text( file_name, script.create( None, True ) )
    
    pr.printx( "Written file: <file>{}</file>", file_name )


@app.command( names = ["cypher"] )
def send_cypher( code: str,
                 output: Optional[Destination] = None,
                 database: Optional[DatabaseEndpoint] = None ) -> DbStats:
    """
    Runs some Cypher code
    
    NOTE: From the CLI you can use the much abbreviated `=` command to run a cypher query.
          Otherwise you will have to be careful with special symbols (' ', '=', '"') in your code, which have meaning to the CLI.
    
    :param database:    Database to run code on. This parameter can be ignored if you only have one database-connected endpoint.
    :param output:      Where to send the result to.
                        If not specified the result is sent to a temporary memory endpoint.
                        (Please don't use this for big queries!) 
    :param code:        The code to run
    
    :return:        A `DbStats` object containing statistics and endpoint execution. 
    """
    output = output or get_core().endpoint_manager.get_temporary_destination()
    
    database: DatabaseEndpoint = database or get_core().endpoint_manager.get_database_endpoint()
    
    with database.open_connection() as connection:
        with output.open_writer() as output_:
            assert isinstance( connection, DbManager )
            result: DbStats = connection.run_cypher( title = "User script",
                                                     cypher = code,
                                                     output = output_ )
    
    print( "----{}".format( result ) )
    
    return result


@app.command()
def print_schema( cypher: bool = False ):
    """
    Prints the |app_name| schema
    (this is _not_ the same as the current database schema - use `:schema` in Cypher for that).
    Use `apply_schema` to apply the schema.
    
    :param cypher: Return text as Cypher
    """
    if cypher:
        schema = get_core().schema.get_schema_cypher()
    else:
        schema = get_core().schema.get_schema_description()
        
        schema = string_helper.highlight_regex( schema, " \\(:([a-zA-Z_]+)\\)\n", Theme.COMMAND_NAME, Theme.RESET )
        schema = string_helper.highlight_regex( schema, "\\[:([a-zA-Z_]+)\\]", Theme.FIELD_NAME, Theme.RESET )
        schema = string_helper.highlight_regex( schema, "PROP ([a-zA-Z_]+):", Theme.ARGUMENT_NAME, Theme.RESET )
    
    print( schema )


@app.command()
def apply_schema( database: Optional[DatabaseEndpoint] = None ) -> Tuple[MemoryEndpoint, List[DbStats]]:
    """
    Applies the Neocommand schema schema to the database.
        
    :param database:    Database to apply schema to, or `None` for the default database. 
    :return:            Tuple of the endpoint and list of `DbStats` objects returned from creating the schema.  
    """
    schema = get_core().schema.get_schema_cypher()
    database = database or get_core().endpoint_manager.get_database_endpoint()
    
    ep = MemoryEndpoint( "schema_temp" )
    r = []
    ns = False
    rl = []
    rnl = []
    
    with ep.open_writer() as writer:
        with database.open_connection() as db:
            assert isinstance( db, DbManager )
            lines = schema.split( "\n" )
            for line in pr.pr_iterate( lines, title = "Schema" ):
                try:
                    r.append( db.run_cypher( title = "schema",
                                             cypher = line,
                                             output = writer ) )
                    
                    rl.append( "Okay: " + line )
                except ValueError as ex:
                    if "Property existence constraint requires Neo4j Enterprise Edition" not in str( ex ):
                        raise ValueError( "Problem creating schema «{}». See causing exception for details.".format( line ) ) from ex
                    
                    ns = True
                    rnl.append( "Not supported: " + line )
    
    pr.printx( "<verbose>{}</verbose>".format( "\n".join( rl ) ) )
    pr.printx( "<verbose>{}</verbose>".format( "\n".join( rnl ) ) )
    
    print( "Schema created. It may take some time for any new indexes to be created." )
    
    if ns:
        warn( "One or more schema were not created because they require Neo4j Enterprise Edition.", UserWarning )
    
    return ep, r
