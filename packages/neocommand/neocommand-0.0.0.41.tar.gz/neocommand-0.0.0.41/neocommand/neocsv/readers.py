import csv
from typing import Dict, Optional, Tuple

from .filenames import NcvFilename
from .headers import NcvHeader


NEO4J_LINE_TERMINATOR  = "\n"
NEO4J_ARRAY_DELIMITER = "\t" # delimiter WE are using for Neo4j CSVs (the default is `;`, but this is problematic)



class NcvReader:
    """
    Reads a NeoCsv file.
    
    In contrast to `csv.dictreader`, this parses the headers, stripping extraneous type and
    label information from the keys in the `dict` returned.
    """
    
    
    def __init__( self, neo_csv_filename: NcvFilename ):
        """
        CONSTRUCTOR
        :param neo_csv_filename: Parsed filename 
        """
        self.file_name = neo_csv_filename.filename
        self.__stream = open( self.file_name, "r" )
        self.__reader = csv.reader( self.__stream, lineterminator = NEO4J_LINE_TERMINATOR )
        self.__headers = self.__read_all_headers( neo_csv_filename, next( self.__reader ) )
    
    
    @property
    def headers( self ) -> Tuple[NcvHeader, ...]:
        """
        Obtains the headers.
        """
        return self.__headers
    
    
    @staticmethod
    def __read_all_headers( file: NcvFilename, decorated_names: Optional[list] ) -> Tuple[NcvHeader, ...]:
        """
        Static method that reads converts a list of decorated names to a list of headers.
        """
        result = []
        
        if decorated_names:
            for header_text in decorated_names:
                header = NcvHeader.from_decorated_name( file, header_text )
                result.append( header )
        
        return tuple( result )
    
    
    def next( self ) -> Dict[NcvHeader, object]:
        """
        Iterates rows, where each row is returned as a dict of headers versus cell content.
        """
        row = next( self.__reader )  # exception: StopIteration 
        
        result = { }
        
        for col_index, cell in enumerate( row ):
            header: NcvHeader = self.__headers[col_index]
            
            if header.is_regular:
                cell = header.type.string_to_value( cell, array_delimiter = NEO4J_ARRAY_DELIMITER )
            
            result[header] = cell
        
        return result
    
    
    def __iter__( self ):
        while True:
            yield self.next()
