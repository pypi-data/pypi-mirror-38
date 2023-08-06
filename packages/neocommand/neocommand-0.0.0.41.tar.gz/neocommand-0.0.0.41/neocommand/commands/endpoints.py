from mhelper import isDirname, isFilename, isOptional, isUnion, isPassword, SwitchError, file_helper, MEnum, TTristate
from typing import Optional

import intermake

from neocommand.application import app
from neocommand.data import isDriverName
from neocommand.data.core import get_core
from neocommand.endpoints import DatabaseEndpoint, EdgeCsvEndpoint, GexfEndpoint, CsvFolderEndpoint, VisJsEndpoint
from neocommand.endpoints.abstract_endpoints import Endpoint
from neocommand.endpoints.mgraph_endpoint import MGraphEndpoint
from neocommand.helpers.schema_helper import NodeSchema, EdgeSchema


class EFileType( MEnum ):
    """
    :cvar GEXF:     GEXF, for Gephi.
    :cvar VISJS:    VISJS, for viewing in your browser.
    :cvar MGRAPH:   MGraph, can be converted to a variety of other formats in B42. 
    :cvar CSV:      CSV, for viewing in Excel.
    """
    # TODO: Remove other options - MGraph can already be converted to the other formats and more.
    #       Rather than forcing the user to perform yet another conversion, all of the MGraph export formats
    #       should be just listed here.
    GEXF = 1
    VISJS = 2
    MGRAPH = 3
    CSV = 4


@app.command( names = ["endpoints", "eps"] )
def print_endpoints():
    """
    Lists endpoints.
    """
    # Just use the ready-made `ls` function
    r = ["<section name='Endpoints'><ul>"]
    for ep in get_core().endpoint_manager:
        r.append( "<li>{} ({})</li>".format( ep.name, ep ) )
    
    r.append( "</ul></section>" )
    intermake.pr.printx( "".join( r ) )


@app.command( highlight = True )
def open_file( name: str = "",
               path: isOptional[isFilename] = None,
               type: EFileType = EFileType.MGRAPH,
               overwrite: TTristate = None ) -> Endpoint:
    """
    Adds an endpoint: A Gephi, HTML, binary or CSV file 
    
    At least the `name` or `path` argument must be specified.
    
    :param overwrite:   Permit file overwriting.
                        If `False` an error is raised if an overwrite is attempted.
                        If `True` the file can be overwritten.
                        If unspecified or `None`, the file can be overwritten but a warning is displayed.
    :param type:        Type of file to open.
    :param name:        Name of the endpoint.
                        If not specified, the filename will be used.
    :param path:        Path to GEXF file.
                        This will be created if it doesn't already exist.
                        If not specified, a file in the `workspace` will be created with the specified `name`.
                        Note that the following special paths are also accepted:
                            `ui` - write to redirected `sys.stdout` (`sys.stderr` for CLI, the output window for the GUI)
                            `stdout` - write to the original `sys.stdout`. Not compatible with GUI.
    :return:            The endpoint is returned. 
    """
    name, path = __resolve_name_and_path( name, path )
    
    if type == EFileType.GEXF:
        endpoint = GexfEndpoint( name, path, overwrite )
    elif type == EFileType.VISJS:
        endpoint = VisJsEndpoint( name, path, overwrite )
    elif type == EFileType.CSV:
        endpoint = EdgeCsvEndpoint( name, path, overwrite )
    elif type == EFileType.MGRAPH:
        endpoint = MGraphEndpoint( name, path, overwrite )
    else:
        raise SwitchError( "type", type )
    
    get_core().endpoint_manager.add_user_endpoint( endpoint )
    print( "New endpoint created: «{}»".format( endpoint ) )
    return endpoint


@app.command( highlight = True )
def open_parcel( name: str = "", path: isOptional[isDirname] = None, append: bool = False ) -> CsvFolderEndpoint:
    """
    Adds an endpoint: A folder containing multiple CSVs
    
    These endpoints are folders containing CSV files in the correct format for bulk importing into the database.
    
    At least the `name` or `path` argument must be specified.
    
    :param name:    Name of the endpoint.
                    If not specified, the name will be taken from the last element of the path.
    :param path:    Path to folder.
                    This will be created if it doesn't already exist.
                    If not specified, a folder in the `workspace` will be created with the specified `name`.
    :param append:  When `True` this permits appending to a parcel that already exists.
                    
    :return: The endpoint is returned. 
    """
    
    name, path = __resolve_name_and_path( name, path )
    endpoint = CsvFolderEndpoint( name, path, append )
    get_core().endpoint_manager.add_user_endpoint( endpoint )
    
    if len( endpoint.list_contents() ) == 0:
        print( "New parcel «{}» created at «{}».".format( endpoint.name, endpoint.path ) )
    else:
        print( "Existing parcel «{}» opened at «{}».".format( endpoint.name, endpoint.path ) )
    
    return endpoint


class EOperatingSystem( MEnum ):
    UNKNOWN = 0
    WINDOWS = 1
    UNIX = 2


@app.command( highlight = True )
def open_database( name: str = "neo4j",
                   driver: isDriverName = "neo4jv1",
                   host: str = "127.0.0.1",
                   user: str = "neo4j",
                   password: isPassword = "",
                   directory: isOptional[isDirname] = None,
                   os: EOperatingSystem = EOperatingSystem.UNKNOWN,
                   port: int = 7474,
                   keyring: bool = True ) -> DatabaseEndpoint:
    """
    Adds an endpoint: Neo4j database
    
    :param os:          Set to the OS of the system upon which the database is hosted.
    :param directory:   Set to the local Neo4j installation directory. Optional.
    :param name:        Name you will call the endpoint
    :param driver:      Database driver, e.g. `neo4jv1` or `py2neo`. 
    :param host:        Database host. Typically an IP address of the form `000.000.000.000`.
    :param user:        Database username.
    :param password:    Database password. Nb. If you are using the terminal you can use `password=prompt` to be prompted by the CLI discretely.
    :param port:        Database port. 
    :param keyring:     Normally, passwords will be stored on the system keyring (requires the `keyring` Python package) and are not displayed to the user.
                        If this flag is unset, the password is stored in plain text and is not masked by the UI.
    :return:            The endpoint is returned.  
    """
    if ":" in host:
        raise ValueError( "Invalid database host name: {}".format( host ) )
    
    if not password:
        raise ValueError( "A password is required." )
    
    endpoint = DatabaseEndpoint( name = name,
                                 driver = driver,
                                 remote_address = host,
                                 user_name = user,
                                 password = password,
                                 directory = str( directory ) if directory else None,
                                 is_unix = True if os == EOperatingSystem.UNIX else False if os == EOperatingSystem.WINDOWS else None,
                                 port = str( port ),
                                 keyring = keyring )
    
    get_core().endpoint_manager.add_user_endpoint( endpoint )
    return endpoint


def __resolve_name_and_path( name: str, path: isOptional[isUnion[isFilename, isDirname]] ):
    if not name:
        if not path:
            raise ValueError( "A name and/or a path must be specified." )
        
        name = file_helper.get_filename_without_extension( path )
    
    if not path:
        path = file_helper.join( intermake.Controller.ACTIVE.app.local_data.local_folder( "user_endpoints" ), name )
    
    return name, path


@app.command()
def close_endpoint( endpoint: Optional[Endpoint] = None,
                    delete: bool = False,
                    all: bool = False ):
    """
    Removes endpoints.
    (This affects |app_name| only - contents on disk, if any, are unaffected)
    
    :param delete:      Also delete the data from disk. 
    :param endpoint:    The endpoint to remove.
    :param all:         When set, all endpoints are removed.
    """
    if all:
        if endpoint is not None:
            raise ValueError( "Both the `endpoint` and the `all` parameter must not provided simultaneously." )
        
        eps = get_core().endpoint_manager.user_endpoints
        
        if not eps:
            print( "No endpoints to close." )
            return
        
        for endpoint in eps:
            print( "Endpoint closed: {}".format( endpoint.endpoint_name ) )
            get_core().endpoint_manager.remove_user_endpoint( endpoint )
        
        print( "{} endpoints closed".format( len( eps ) ) )
        print( "(Note that closing endpoints does not remove them from disk)" )
    elif endpoint is not None:
        get_core().endpoint_manager.remove_user_endpoint( endpoint, delete )
        print( "Endpoint closed: {}".format( endpoint.name ) )
        print( "(Note that closing endpoints does not remove them from disk)" )
    else:
        raise ValueError( "Either the `endpoint` or the `all` parameter must be provided." )


_TEST_SCHEMA = NodeSchema( "TestNode" )
_TEST_EDGE_SCHEMA = EdgeSchema( _TEST_SCHEMA, "TestEdge", _TEST_SCHEMA )
