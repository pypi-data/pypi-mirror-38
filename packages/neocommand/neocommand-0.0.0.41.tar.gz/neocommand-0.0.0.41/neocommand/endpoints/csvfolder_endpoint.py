import warnings
import os.path
from typing import Iterator, Tuple, Dict, List

from mhelper import file_helper, override, array_helper
from neocommand.data import NcNode, NcEdge
from neocommand.neocsv import filenames
from neocommand.neocsv.headers import NcvFilename, ENcvSpecial, NcvHeader
from neocommand.neocsv.readers import NcvReader
from neocommand.neocsv.writers import NcvMultiWriter
from neocommand.endpoints.abstract_endpoints import Origin, Destination, Writer, Reader


class CsvFolderEndpoint( Destination, Origin ):
    """
    Endpoint that uses a folder containing one or more neo4j-compatible CSVs.
    """
    
    
    def __init__( self, name: str, path: str, append: bool ):
        """
        CONSTRUCTOR 
        """
        super().__init__( name )
        self.path = path
        self.append = append  # TODO: Replace this with `overwrite`
    
    
    def __str__( self ) -> str:
        return "CSV-folder: {}".format( file_helper.get_filename( self.path ) )
    
    
    def on_open_reader( self ):
        return _ReadCsvFolderEndpoint( self )
    
    
    def on_open_writer( self ):
        return _OpenCsvFolderEndpoint( self )
    
    
    def on_removed( self, delete: bool ):
        if delete:
            file_helper.recycle_file( self.path )
    
    
    def list_contents( self ) -> List[NcvFilename]:
        r = []
        
        if not os.path.isdir( self.path ):
            return r
        
        for file_name in file_helper.list_dir( self.path, filenames.EXT_B42CSV, False ):
            try:
                r.append( NcvFilename.construct_from_file( file_name ) )
            except:
                pass
        
        return r


class _ReadCsvFolderEndpoint( Reader ):
    def __init__( self, owner: CsvFolderEndpoint ):
        super().__init__()
        self.owner = owner
    
    
    @override
    def __len__( self ) -> int:
        return len( list( self.owner.list_contents() ) )
    
    
    @override
    def on_read_all( self ) -> Iterator[object]:
        for file in self.owner.list_contents():
            reader = NcvReader( file )
            
            is_edge = file.is_edge
            
            assert (isinstance( x, NcvHeader ) for x in reader.headers)
            
            if is_edge:
                try:
                    start_h: NcvHeader = array_helper.single_or_error( (x for x in reader.headers if x.special == ENcvSpecial.START) )
                    end_h: NcvHeader = array_helper.single_or_error( (x for x in reader.headers if x.special == ENcvSpecial.END) )
                except KeyError as ex:
                    raise ValueError( "The CSV file «{}» for the edge does not have the mandatory start or end column.".format( file.filename ) ) from ex
                
                for line in reader:
                    start_uid = line[start_h]
                    end_uid = line[end_h]
                    
                    start = NcNode( label = file.start_label, uid = start_uid, iid = None, properties = None )
                    end = NcNode( label = file.end_label, uid = end_uid, iid = None, properties = None )
                    data = self.__convert_row_to_data( line )
                    
                    yield NcEdge( label = file.label, start = start, end = end, properties = data )
            else:
                try:
                    uid_h: NcvHeader = array_helper.single_or_error( (x for x in reader.headers if x.special == ENcvSpecial.UID) )
                except KeyError as ex:
                    raise ValueError( "The CSV file «{}» for the edge does not have the mandatory ID column.".format( file.filename ) ) from ex
                
                for line in reader:
                    uid = line[uid_h]
                    data = self.__convert_row_to_data( line )
                    yield NcNode( label = file.label, uid = uid, properties = data )
    
    
    def __convert_row_to_data( self, line: Dict[NcvHeader, str] ) -> Dict[str, str]:
        data = { }
        
        for key, value in line.items():
            if key.is_regular:
                data[key.name] = value
        
        return data
    
    
    @override
    def on_read_all_props( self, label: str, property: str ) -> Iterator[Tuple[str, object]]:
        raise NotImplementedError( "Not implemented yet, sorry." )


class _OpenCsvFolderEndpoint( Writer ):
    def __init__( self, owner: CsvFolderEndpoint ):
        super().__init__()
        file_helper.create_directory( owner.path )
        self.owner = owner
        self.__writer = NcvMultiWriter( owner.path, owner.append )
    
    
    @override
    def on_write_folder( self, name: str ) -> Destination:
        """
        OVERRIDE Destination
        Does nothing
        """
        return self
    
    
    @override
    def on_write_data( self, data: object ):
        warnings.warn( "This endpoint «{}» does not support the adding of arbitrary (non-node/edge) data «{}». This action has been ignored.".format( self, data ) )
    
    
    @override
    def on_write_edge( self, edge: NcEdge ):
        """
        Adds an edge-csv
        """
        self.__writer.write_edge( edge )
    
    
    @override
    def on_write_node( self, node: NcNode ):
        """
        OVERRIDE
        Write a node
        """
        assert all( node.properties.keys() )
        
        try:
            self.__writer.write_node( node )
        except Exception as ex:
            ss = ["Failed to write node. See causing error for details. Node details follow:",
                  "-- label = {}".format( node.label ),
                  "-- uid = {}".format( node.uid ),
                  "\n--",
                  "\n-- ".join( "{} = {}".format( k, v ) for k, v in node.properties.items() )]
            
            raise ValueError( "\n".join( ss ) ) from ex
    
    
    @override
    def on_close( self ) -> None:
        """
        OVERRIDE
        Flush 
        """
        self.__writer.close_all()
