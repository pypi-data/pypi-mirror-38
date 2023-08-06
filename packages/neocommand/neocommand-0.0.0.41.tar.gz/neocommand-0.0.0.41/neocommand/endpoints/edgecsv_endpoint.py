from os import path

from mhelper import isFilename, TTristate, EFileMode
from neocommand.data import NcNode, NcData, NcEdge
from neocommand.endpoints.abstract_endpoints import Destination, Writer
from progressivecsv import ProgressiveCsvWriter


_EXT_CSV = ".csv"


class EdgeCsvEndpoint( Destination ):
    
    
    def __init__( self,
                  name: str,
                  file_name: isFilename[EFileMode.WRITE, _EXT_CSV],
                  overwrite: TTristate ):
        super().__init__( name )
        self.file_name = file_name
        self.overwrite = overwrite
    
    
    def __str__( self ):
        return "CSV: {}".format( self.file_name )
    
    
    def on_open_writer( self ):
        return _EdgeCsvEndpointWriter( self.file_name, self.overwrite )


class _EdgeCsvEndpointWriter( Writer ):
    def __init__( self, file_name, overwrite ):
        super().__init__()
        self.file_name = file_name
        self.overwrite = overwrite
        self.file: ProgressiveCsvWriter = None
        self.row = None
    
    
    def on_prepare( self ):
        if path.exists( self.file_name ) and not self.overwrite:
            raise FileExistsError( self.file_name )
        
        self.file = ProgressiveCsvWriter( self.file_name )
        self.row = { }
    
    
    def on_close( self ) -> None:
        self.__flush_row()
        self.file.close()
        self.file = None
    
    
    def write( self, k, v ):
        if k in self.row:
            self.__flush_row()
        
        self.row[k] = str( v )
    
    
    def __flush_row( self ):
        if self.row:
            self.file.write_row( self.row )
            self.row = { }
    
    
    def on_write_data( self, data: NcData ):
        self.write( data.varname, data.value )
    
    
    def on_write_folder( self, name: str ) -> "Destination":
        pass
    
    
    def on_write_node( self, node: NcNode ):
        self.write( "{}.{}".format( node.varname, "uid" ), node.uid )
        self.write( "{}.{}".format( node.varname, "label" ), node.label )
        
        for k, v in node.properties.items():
            self.write( "{}.{}".format( node.varname, k ), v )
    
    
    def on_write_edge( self, edge: NcEdge ):
        edge.start.varname = edge.varname + ".start"
        edge.end.varname = edge.varname + ".end"
        
        self.on_write_node( edge.start )
        self.on_write_node( edge.end )
        
        for k, v in edge.properties.items():
            self.write( "{}.{}".format( edge.varname, k ), v )
