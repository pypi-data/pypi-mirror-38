"""
Module containing functions for exporting data "parcels" to Neo4j
"""
import csv
import re
import shutil
from os import path, system
from typing import Callable, List, Optional

import neocommand.neocsv.constants
from intermake import pr
from mhelper import EFileMode, isFilename, MEnum, SwitchError, file_helper, string_helper
from neocommand.application import app
from neocommand import Destination, CounterWriter, NcvFilename, NcvHeader
from neocommand.endpoints import DatabaseEndpoint, NULL_ENDPOINT, CsvFolderEndpoint
from neocommand.endpoints.abstract_endpoints import Origin
from neocommand.neocsv import filenames
from neocommand.neocsv.types import NeoType


IMPORT_DOT_CYPHER = "import.cypher"
IMPORT_DOT_SH = "import.sh"
READ_CYPHER_FILE = isFilename[EFileMode.READ, neocommand.neocsv.constants.EXT_CYPHER]
READ_SHELL_FILE = isFilename[EFileMode.READ, neocommand.neocsv.constants.EXT_SH]


class EParcelMethod( MEnum ):
    """
    How to import a parcel into the database.

    :cvar DEFAULT:     The default is normally the same as `DIRECT`.
                       Since there may be a better option, this is not a valid choice when
                       transferring from a parcel to a database.
                       
    :cvar DIRECT:      Import the parcel directly using the `transfer` command.
                       Note that you can use the `transfer` directly to convert between different types of endpoint.
                       
    :cvar ADD:         Create and execute a single, self contained cypher script that will import the parcel.
                       
    :cvar MAKE_ADD:    Same as `ADD` but does not execute the script.
                       
    :cvar IMPORT:      Create a cypher script that will point to the parcel and import it into the database.
                       
                       This action cannot be performed remotely as it requires the database and parcel both be
                       present on the executing machine.

    :cvar MAKE_IMPORT: Same as `IMPORT` but does not execute the script.
    :cvar CREATE:      Create, and optionally execute, a shell script that will convert the parcel to a new database.
                       This action does not change the existing database but requires a database connection to identify
                       the location of the binaries. This action cannot be performed remotely.

    :cvar MAKE_CREATE: Same as `CREATE` but does not execute the script.
    :cvar RUN:         If an existing script was generated but not executed (i.e. using a `MAKE_` command), this
                       executes that script.
    """
    DEFAULT = 0
    DIRECT = 1
    ADD = 2
    MAKE_ADD = 3
    IMPORT = 4
    MAKE_IMPORT = 5
    CREATE = 6
    MAKE_CREATE = 7
    RUN = 8


@app.command( folder = "import" )
def transfer( origin: Origin, destination: Destination, method: EParcelMethod = EParcelMethod.DEFAULT ):
    """
    Transfers all information from one endpoint to another.
     
    :param origin:   Input, where to source data from.
    :param destination:  Output, where to send data to. 
    :param method:      Method by which to import
    """
    if method == EParcelMethod.DEFAULT:
        if isinstance( origin, CsvFolderEndpoint ) and isinstance( destination, DatabaseEndpoint ):
            raise TypeError( "When transferring a parcel «{}» to a database «{}» the `method` (protocol) parameter must be specified and cannot be «{}».".format( origin, destination, EParcelMethod.DEFAULT ) )
        
        method = EParcelMethod.DIRECT
    
    if method == EParcelMethod.DIRECT:
        text_ = lambda index,: "{} entities, {} nodes, {} edges".format( index, cew.num_nodes, cew.num_nodes )
        num = 0
        
        with destination.open_writer() as writer:
            with origin.open_reader() as reader:
                cew = CounterWriter( writer )
                
                for entity in pr.pr_iterate( reader.read_all(), "Iterating {}".format( origin ), text = text_ ):
                    num += 1
                    cew.write_entity( entity )
                
                pr.printx( "<verbose>Transfer completed. {} items. {}.</verbose>".format( num, cew ) )
                return
    
    if not isinstance( origin, CsvFolderEndpoint ):
        raise TypeError( "For transfer method «{}» the `input` endpoint must be of type «{}».".format( method, CsvFolderEndpoint.__name__ ) )
    
    if not isinstance( destination, DatabaseEndpoint ):
        raise TypeError( "For transfer method «{}» the `output` endpoint must be of type «{}».".format( method, DatabaseEndpoint.__name__ ) )
    
    if method in (EParcelMethod.ADD, EParcelMethod.MAKE_ADD):
        __add_parcel_via_script( origin, destination, method == EParcelMethod.MAKE_ADD )
    elif method in (EParcelMethod.IMPORT, EParcelMethod.MAKE_IMPORT):
        __csv_import_parcel( origin, destination, method == EParcelMethod.MAKE_IMPORT )
    elif method in (EParcelMethod.CREATE, EParcelMethod.MAKE_CREATE):
        __new_database_from_parcel( origin, destination, method == EParcelMethod.MAKE_CREATE )
    elif method == EParcelMethod.RUN:
        __run_existing_import_script( origin, destination )
    else:
        raise SwitchError( "method", method )


def __run_existing_import_script( parcel: CsvFolderEndpoint, endpoint: DatabaseEndpoint ):
    """
    Runs the import script from the specified parcel.
     
    :param endpoint:    Where to send the data
    :param parcel:      CsvFolderEndpoint 
    :return: 
    """
    scr_cypher = path.join( parcel.path, IMPORT_DOT_CYPHER )
    scr_shell = path.join( parcel.path, IMPORT_DOT_SH )
    
    if path.isfile( scr_cypher ):
        if path.isfile( scr_shell ):
            raise ValueError( "Cannot run the import script in this folder because it is ambiguous between «{0}» and «{1}». Either run the file manually or delete one of the scripts.".format( scr_cypher, scr_shell ) )
        
        # noinspection PyTypeChecker
        __parcel_run_cypher( endpoint, scr_cypher )
    elif path.isfile( scr_shell ):
        # noinspection PyTypeChecker
        __parcel_run_shell( scr_shell )
    else:
        raise ValueError( "Cannot run the import script in this folder a script file «{0}» or «{1}» cannot be found. Perhaps you meant to create the script first (see `help_parcels`)".format( scr_cypher, scr_shell ) )


# noinspection PyUnusedLocal
def __new_database_from_parcel( input: CsvFolderEndpoint, endpoint: DatabaseEndpoint, halt: bool = False ) -> str:
    """
    Generates and runs an `neo4j-import.exe` script that generates a new database from the parcel.
    
    :param halt:                If set, does not run the script after generating it
    :param endpoint:            Path to the new database to be created
    :param input:               CsvFolderEndpoint being used - also where the script will be written (see `help parcels`)
    :return:                    Name of resulting script file
    """
    db_name = input.name
    binary_dir = endpoint.get_binary_directory()
    
    if not binary_dir or not path.isdir( binary_dir ):
        raise ValueError( "Setting invalid : endpoint.get_binary_directory() = " + binary_dir )
    
    result = []
    result.append( "cd \"{0}\"".format( binary_dir ) )
    script = []
    
    files = __get_files( input )
    
    for file in files:
        if file.is_edge:
            statement = string_helper.strip_lines( __NEW_EDGE )
        else:
            statement = string_helper.strip_lines( __NEW_NODE )
        
        statement = string_helper.bulk_replace( statement, label = file.label, file_name = file.filename )
        script.append( statement )
    
    script_text = " ".join( script )
    
    result.append( "./neo4j-import --into {0} {1} --multiline-fields=true --array-delimiter TAB --skip-bad-relationships=true --skip-duplicate-nodes=true --bad-tolerance=100000000 --ignore-empty-strings=true".format( db_name, script_text ) )
    
    file_name = path.join( input.path, IMPORT_DOT_SH )
    file_helper.write_all_text( file_name, "\n\n".join( result ) )
    
    if not halt:
        # noinspection PyTypeChecker
        __parcel_run_shell( file_name )
    
    return file_name


# noinspection PyUnusedLocal
def __csv_import_parcel( input: CsvFolderEndpoint, endpoint: DatabaseEndpoint, halt: bool = False ) -> str:
    """
    Generates and runs a Cypher "bulk import" script from a parcel.
    
    :param endpoint:             Database information.
    :param halt:                Whether to run the script.
    :param input:              CsvFolderEndpoint being used - also where the script will be written
    :return:                   Name of resulting script file
    """
    result = []
    nc_files = __get_files( input )
    
    for nc_file in nc_files:
        headers, first_line = __get_csv_head( nc_file.filename )
        
        attributes, name_column, start_column, end_column = __create_attribute_script( nc_file, headers, __neo4j_type_to_csv_neo4j_conversion, None )
        
        # Generate the "merge" part of the statement
        if nc_file.is_edge:
            assert name_column is None, "{} {}".format( nc_file.filename, name_column )
            assert start_column is not None, "{} {}".format( nc_file.filename, start_column )
            assert end_column is not None, "{} {}".format( nc_file.filename, end_column )
            
            statement = string_helper.bulk_replace( string_helper.strip_lines( __CSV_EDGE ),
                                                    start_label = nc_file.start_label,
                                                    end_label = nc_file.end_label,
                                                    start_column = headers[start_column],
                                                    end_column = headers[end_column] )
        
        else:
            assert name_column is not None, "{} {}".format( nc_file.filename, name_column )
            assert start_column is None, "{} {}".format( nc_file.filename, start_column )
            assert end_column is None, "{} {}".format( nc_file.filename, end_column )
            
            statement = string_helper.bulk_replace( string_helper.strip_lines( __CSV_NODE ),
                                                    uid = headers[name_column] )
        
        # The filenames are different under UNIX and Windows
        if endpoint.get_is_unix():
            file_prefix = neocommand.neocsv.constants.PREFIX_UNIX
        else:
            file_prefix = neocommand.neocsv.constants.PREFIX_WINDOWS
        
        # The creation method depends on the user's settings and the entity flags
        method = "MERGE"  # now it's always just "Merge", it keeps things simple
        
        statement = string_helper.bulk_replace( statement,
                                                label = nc_file.label,
                                                creation = method,
                                                file_name = file_prefix + nc_file.alone + filenames.EXT_B42CSV,
                                                attributes = attributes )
        
        result.append( statement )
    
    file_name = path.join( input.path, IMPORT_DOT_CYPHER )
    file_helper.write_all_text( file_name, "\n\n".join( result ) )
    
    if not halt:
        # noinspection PyTypeChecker
        __parcel_run_cypher( endpoint, file_name )
    
    return file_name


# noinspection PyUnusedLocal
def __add_parcel_via_script( input: CsvFolderEndpoint, database: DatabaseEndpoint, halt: bool = False ) -> str:
    """
    Generates and runs a simple Cypher script from a parcel.
    
    :param halt:                Whether to run the script
    :param input:              CsvFolderEndpoint being used - also where the script will be written
    :return:                   Name of resulting script file
    """
    results = []
    files = __get_files( input )
    
    for file in files:
        with open( file.filename, "r" ) as in_file:
            reader = csv.reader( in_file )
            headers = next( reader )
            method = "MERGE"  # Now it's always just "MERGE", it keeps things simple
            
            for row in pr.pr_iterate( reader, title = "reading rows" ):
                attributes, name_column, start_column, end_column = __create_attribute_script( file, headers, __neo4j_type_to_direct_neo4j_conversion, row )
                
                if file.is_edge:
                    result = string_helper.bulk_replace( string_helper.strip_lines( __ADD_EDGE ),
                                                         start_label = file.start_label,
                                                         start_uid = row[start_column],
                                                         end_label = file.end_label,
                                                         end_uid = row[end_column],
                                                         creation = method,
                                                         label = file.label,
                                                         attributes = attributes )
                else:
                    result = string_helper.bulk_replace( string_helper.strip_lines( __ADD_NODE ),
                                                         creation = method,
                                                         label = file.label,
                                                         uid = row[name_column],
                                                         attributes = attributes )
                
                results.append( result )
    
    file_name = path.join( input.path, IMPORT_DOT_CYPHER )
    file_helper.write_all_text( file_name, "\n\n".join( results ) )
    
    if not halt:
        # noinspection PyTypeChecker
        __parcel_run_cypher( database, file_name )
    
    return file_name


def __create_attribute_script( filename: NcvFilename, headers, expression: Callable[[NcvFilename, str, int, Optional[List[object]]], Optional[str]], row_data: Optional[List[object]] ):
    """
    Creates the attribute Cypher script given a set of headers and their values.
    """
    name_column = None
    start_column = None
    end_column = None
    attributes = []
    
    for i, header in enumerate( headers ):
        if header.startswith( neocommand.neocsv.constants.PRIMARY_KEY_DECORATED_NAME ):
            name_column = i
        elif header.startswith( neocommand.neocsv.constants.NEO4J_START_ID_SUFFIX ):
            start_column = i
        elif header.startswith( neocommand.neocsv.constants.NEO4J_END_ID_SUFFIX ):
            end_column = i
        else:
            row_value = expression( filename, header, i, row_data )
            
            if row_value is not None:
                attributes.append( row_value )
    
    if attributes:
        attributes = "SET\n" + ",\n".join( attributes )
    else:
        attributes = ""
    
    return attributes, name_column, start_column, end_column


def __get_csv_head( file_name: str ) -> (str, str):
    """
    Gets the CSV headers and the first line of the CSV
    """
    
    with open( file_name, "r" ) as file:
        reader = csv.reader( file )
        try:
            first = next( reader )
            second = next( reader )
            return first, second
        except StopIteration as ex:
            raise ValueError( "Failed to read head from «{}».".format( file_name ) ) from ex


# noinspection PyUnusedLocal
def __neo4j_type_to_csv_neo4j_conversion( nc_file_name: NcvFilename, header_text: str, index: int, row: Optional[List[object]] ) -> Optional[str]:
    """
    Produces the Cypher query that moves from a field `r.X` (which is a string) to `z.X` (which is a T).
    Where field name `X` and field type `T` are defined in the `header_text`.
    """
    nch = NcvHeader.from_decorated_name( nc_file_name, header_text )
    
    value = "r.`{0}`".format( header_text )
    
    if nch.type is NeoType.INT:
        result = "toInt({0})".format( value )
    elif nch.type is NeoType.FLOAT:
        result = "toFloat({0})".format( value )
    elif nch.type is NeoType.STR:
        result = value
    elif nch.type is NeoType.BOOL:
        result = "(case {0} when \"True\" then true else false end)".format( value )
    elif nch.type is NeoType.STR.ARRAY:
        result = 'split({0},"\\t")'.format( value )
    else:
        raise SwitchError( "nch.type", nch.type )
    
    return "z.`{0}` = {1}".format( nch.name, result )


def __neo4j_type_to_direct_neo4j_conversion( nc_file_name: NcvFilename, header_text: str, index: int, row: Optional[List[str]] ) -> Optional[str]:
    """
    Produces the Cypher query that moves the `value` to a field called `z.X` (which is a `T`).
    Where field name `X` and field type `T` are defined in the `header_text`.
    The value is obtained from `row[index]`.
    """
    if header_text.count( ":" ) != 1:
        raise ValueError( "The column name «{}» isn't a valid NEO4J-style header. The format should be «name:type», but it isn't.".format( header_text ) )
    
    nch = NcvHeader.from_decorated_name( nc_file_name, header_text )
    value = row[index]
    
    if nch.type.is_array:
        result = "[{}]".format( ",".join( __convert_value( x, nch.type.NO_ARRAY ) for x in value.split( "\t" ) ) )
    else:
        result = __convert_value( value, nch.type )
    
    return "z.`{0}` = {1}".format( nch.name, result )


def __convert_value( value, nc_type: NeoType ):
    if value is None:
        return None
    
    if nc_type is NeoType.INT:
        # noinspection PyTypeChecker
        int( value )  # assertion
        return value
    elif nc_type is NeoType.FLOAT:
        # noinspection PyTypeChecker
        float( value )  # assertion
        return value
    elif nc_type is NeoType.STR:
        return '"{0}"'.format( str( value ).replace( '"', '\\"' ).replace( "\t", "\\t" ).replace( "\n", "\\n" ) )
    elif nc_type is NeoType.BOOL:
        assert value in ("true", "false")
        return value
    else:
        raise SwitchError( "nc_type", nc_type )


def __type_error( header: str, value: Optional[object], type_: type ):
    return "Expected the column with header «{0}» to be of type «{1}» but got a value of type «{2}» (value = «{3}»). This error should never happen because the correct types should have been obtained in the header-type determining step.".format( header, type_.__name__, type( value ).__name__, value )


def __get_files( directory: CsvFolderEndpoint, files: Optional[List[NcvFilename]] = None ) -> List[NcvFilename]:
    """
    Gets files, or if not specified, all files.
    Sorts them nodes-first (because we need to create nodes before edges).
    """
    if files is None:
        files = list( directory.list_contents() )
    
    files = list( sorted( files, key = lambda x: x.is_edge ) )
    
    return files


__NEW_EDGE = "--relationships:<label> <file_name>"

__NEW_NODE = "--nodes:<label> <file_name>"

__CSV_NODE = \
    """
    CREATE INDEX ON :<label>(name)
    ;
    
    USING PERIODIC COMMIT
    LOAD CSV WITH HEADERS FROM \"<file_name>\" AS r
    <creation> (z:<label> {uid: r.`<uid>`})
    <attributes>
    ;
    
    """

__CSV_EDGE = \
    """
    USING PERIODIC COMMIT
    LOAD CSV WITH HEADERS FROM \"<file_name>\" AS r
    MATCH (x:<start_label> {uid: r.`<start_column>`})
    MATCH (y:<end_label> {uid: r.`<end_column>`})
    <creation> (x)-[z:<label>]->(y)
    <attributes>
    ;
    
    """

__ADD_NODE = \
    """
    <creation> (z:<label> {uid: "<uid>"})
    <attributes>
    ;
    """

__ADD_EDGE = \
    """
    MATCH (x:<start_label> {uid: "<start_uid>"})
    MATCH (y:<end_label> {uid: "<end_uid>"})
    <creation> (x)-[z:<label>]->(y)
    <attributes>
    ;
    
    """


def __parcel_run_cypher( endpoint: DatabaseEndpoint, file: READ_CYPHER_FILE ) -> None:
    """
    Runs a cypher script produced by `neocsv_to_cypher_bulk_script` or `neocsv_to_cypher_add_script`
    
    It breaks the file up into smaller scripts separated by "\n;\n" in order to show progress, but this won't work for files produced outside of these two commands. 
    :param endpoint: Where to send the data (only the directory is used)
    :param file: File to run 
    :return: Nothing
    """
    with pr.pr_action( "Reading file" ):
        text = file_helper.read_all_text( file )
    
    if "LOAD CSV FROM" in text:
        files_needed = re.findall( r'[^"/]*.' + filenames.EXT_B42CSV + r'(?=")', text )
        import_folder = endpoint.get_import_directory()
        
        for file_needed in pr.pr_iterate( files_needed, "Transferring files to import folder" ):
            if not import_folder or not path.isdir( import_folder ):
                raise FileNotFoundError( "Cannot prepare files for import because I can't find the Neo4j import folder «{0}». Please define it in settings first.".format( import_folder ) )
            
            # Move file to import directory of Neo4j
            source = path.join( file_helper.get_directory( file ), file_needed )
            dest = path.join( import_folder, file_needed )
            
            if not path.isfile( source ):
                if path.isfile( dest ):
                    if not pr.pr_question( "A file noted in the import script («{0}») cannot be found locally («{1}») but appears to exist remotely («{2}»). This may be due to a previously failed import. If you are sure this is the intended file, then we can use recover by using the remote file. If you are unsure, do not continue. Continue?".format( file, source, dest ) ):
                        raise FileNotFoundError( "Cannot prepare files for import because a file noted in the import script («{0}») appears to be missing locally («{1}»). A remote version («{2}») does exist but the user chose to ignore it.".format( file, source, dest ) )
                    else:
                        continue
                else:
                    raise FileNotFoundError( "Cannot prepare files for import because a file noted in the import script («{0}») appears to be missing locally («{1}»). A remote version of this file («{2}») does not exist.".format( file, source, dest ) )
            elif path.isfile( dest ):
                raise FileExistsError( "Cannot prepare files for import a file noted in the import script («{0}») needs to be transferred from the local parcel («{1}») but a file with the same name already exists remotely («{2}»).".format( file, source, dest ) )
            
            shutil.move( source, dest )
    else:
        import_folder = None
        files_needed = ()
    
    scriptlets = text.split( "\n;\n" )
    
    try:
        for scriptlet in pr.pr_iterate( scriptlets, "Running commands" ):
            if scriptlet.strip():
                with endpoint.open_connection() as db:
                    db.run_cypher( cypher = scriptlet,
                                   output = NULL_ENDPOINT.WRITER,
                                   title = "transfer" )
    finally:
        for file_needed in pr.pr_iterate( files_needed, "Moving files back from import folder" ):
            source = path.join( file_helper.get_directory( file ), file_needed )
            dest = path.join( import_folder, file_needed )
            shutil.move( dest, source )


def __parcel_run_shell( file: str ) -> None:
    """
    Runs a shell script
     
    :param file: File to run 
    :return: Nothing
    """
    print( "Passing control to external command. See console output for details." )
    system( file )
