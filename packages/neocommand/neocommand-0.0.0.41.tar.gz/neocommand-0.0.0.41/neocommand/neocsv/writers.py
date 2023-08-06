from typing import Dict, Union

from os import path

from progressivecsv import ProgressiveCsvWriter, ProgressiveCsvHeader
from ..data import NcNode, NcEdge

from .types import NEO_FALSE, NEO_TRUE
from .filenames import NcvFilename
from .headers import ENcvSpecial, NcvHeader


class NcvMultiWriter:
    """
    Used for writing to a NeoCsv folder.
    """
    
    
    def __init__( self, folder_path, append ):
        self.__folder_path = folder_path
        self.__append = append
        self.__node_files: Dict[str, NcvWriter] = { }
        self.__edge_files: Dict[str, NcvWriter] = { }
    
    
    def write_node( self, node: NcNode ) -> None:
        """
        Writes the node to the appropriate file. 
        """
        file = self.__node_files.get( node.label )
        
        if file is None:
            file_name = NcvFilename.construct_from_node( self.__folder_path, node.label )
            file = NcvWriter( file_name, self.__append )
            self.__node_files[node.label] = file
        
        new_props = dict( node.properties )
        new_props[ENcvSpecial.UID] = node.uid
        file.write_row( new_props )
    
    
    def write_edge( self, edge: NcEdge ) -> None:
        """
        Writes the edge to the appropriate file. 
        """
        key = self.__edge_key( edge.start.label, edge.label, edge.end.label )
        
        file = self.__edge_files.get( key )
        
        if file is None:
            file_name = NcvFilename.construct_from_edge( self.__folder_path, edge.label, edge.start.label, edge.end.label )
            file = NcvWriter( file_name, self.__append )
            self.__edge_files[key] = file
        
        assert edge.start.uid
        assert edge.end.uid
        
        new_props = dict( edge.properties )
        new_props[ENcvSpecial.START] = edge.start.uid
        new_props[ENcvSpecial.END] = edge.end.uid
        file.write_row( new_props )
    
    
    def any_open( self ) -> bool:
        """
        Returns if any file is open
        :return: 
        """
        return len( self.__node_files ) != 0 or len( self.__edge_files ) != 0
    
    
    def close_all( self ) -> None:
        """
        Finalises and closes all files
        """
        for v in self.__node_files.values():
            v.close()
        
        for v in self.__edge_files.values():
            v.close()
        
        self.__node_files.clear()
        self.__edge_files.clear()
    
    
    @staticmethod
    def __edge_key( start_label, label, end_label ):
        """
        Determines the key of an edge for the internal dictionary.
        """
        return start_label + "," + label + "," + end_label


class NcvWriter:
    """
    Writes a NeoCsv file.
    
    In contrast to `dictwriter`, this parses the keys, adding extra type and label information to the headers actually written to the file.
    
    In addition, it can append new columns to to existing files, though it does so by rewriting the entirety of the file (which is slow).
    """
    
    
    def __init__( self, neo_csv_filename: NcvFilename, append: bool ):
        """
        CONSTRUCTOR
        :param neo_csv_filename: Parsed filename 
        """
        if path.exists( neo_csv_filename.filename ) and not append:
            raise FileExistsError( "Refusing to open the file «{}» because the file already exists and the `append` flag is set to `False`.".format( neo_csv_filename.filename ) )
        
        self.__file_name = neo_csv_filename
        self.__writer = ProgressiveCsvWriter( neo_csv_filename.filename, on_read = self.__on_read )
    
    
    def write_row( self, row_dict: Dict[Union[str, ENcvSpecial], object] ) -> None:
        """
        Writs a row.
        """
        self.__encompass( row_dict )
        
        # Modify the properties so they are acceptable to a typed csv
        for k, v in list( row_dict.items() ):
            row_dict[k] = self.__translate_to_neo4j( v )
        
        self.__writer.write_row( row_dict )
    
    
    def close( self ):
        """
        Closes the stream (mandatory).
        """
        self.__writer.close()
    
    
    def __on_read( self, header: ProgressiveCsvHeader ) -> None:
        """
        Header creation handler.
        Populates the `tag_neo` property with a `NcvHeader`.
        """
        tag_neo = NcvHeader.from_decorated_name( self.__file_name, header.text )
        header.tag_neo = tag_neo
        header.key = tag_neo.name if tag_neo.special == ENcvSpecial.NONE else tag_neo.special
    
    
    def __encompass( self, row_dict: Dict[str, object] ) -> None:
        """
        Recognise the fields provided by this entity.
        Returns a boolean indicating if any changes have occurred.
        """
        for key, value in row_dict.items():
            header = self.__writer.headers.get( key )
            
            if header is None:
                header = self.__writer.append_header( NcvHeader.from_value( key, value ).decorated_name( self.__file_name ) )
            
            # noinspection PyUnresolvedReferences
            tag_neo = header.tag_neo  # type: NcvHeader
            
            if tag_neo.encompass_value( value ):
                header.text = tag_neo.decorated_name( self.__file_name )
    
    
    def __translate_to_neo4j( self, value ) -> str:
        """
        Given a value, which could be anything, translate it into a string that Neo4j will recognise.
        :param value: Value to convert
        :return: The converted string
        """
        type_ = type( value )
        
        if type_ is list or type_ is tuple:
            # Output a list
            return "\t".join( self.__translate_to_neo4j( x ) for x in value )
        elif type_ is bool:
            return NEO_TRUE if value else NEO_FALSE
        elif type_ in (float, int):
            return str( value )
        elif type_ is str:
            # Quotes cause problems to Neo4j, so get rid of them
            return value.replace( '"', "'" )
        else:
            raise ValueError( "Don't know how to translate the Python type «{}» (value = «{}») into a Neo4j-recognisable string.".format( type_, value ) )
