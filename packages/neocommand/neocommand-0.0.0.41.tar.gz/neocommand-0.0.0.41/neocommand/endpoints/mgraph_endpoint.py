import os.path
from typing import Dict, Tuple, List

import mgraph as mg
from neocommand.data import NcEdge, NcNode
from neocommand.endpoints.abstract_endpoints import Destination, Writer


_TNodeLookup = Dict[Tuple[str, str], mg.MNode]
_TEdgeLookup = Dict[Tuple[mg.MNode, str, mg.MNode], mg.MNode]


class MGraphEndpoint( Destination ):
    """
    An endpoint which writes and reads to/from a `MGraph`.
    
    The graph is not part of `__getstate__`, and so a file-name must be provided
    if the graph is to be kept on disk.
    """
    
    
    def __init__( self, name: str, file_name: str = "", overwrite: bool = True ):
        """
        CONSTRUCTOR
        
        :param name:            Inherited. 
        :param file_name:       Name of the file to load/save the graph to/from.
                                This can be empty in which case the graph exists in memory only. 
        :param overwrite:       Whether overwriting an existing file is permitted.
                                Setting this to `False` effectively makes the endpoint write-once
                                and then read-only. 
        """
        super().__init__( name )
        self.file_name = file_name
        self.overwrite = overwrite
        self.__writer = None
    
    
    def __getstate__( self ):
        return { "name"     : self.name,
                 "file_name": self.file_name,
                 "overwrite": self.overwrite }
    
    
    def __setstate__( self, state ):
        self.__init__( state["name"],
                       state["file_name"],
                       state["overwrite"] )
    
    
    def __str__( self ) -> str:
        return "Graph: ({}) {}".format( self.file_name or "in memory", self.__writer )
    
    
    def read_graph( self ) -> mg.MGraph:
        self.on_open_writer()
        return self.__writer.graph
    
    
    def on_open_writer( self ):
        if self.__writer is None:
            self.__writer = _MGraphEndpointWriter( self.file_name, self.overwrite )
        
        return self.__writer


class _MGraphEndpointWriter( Writer ):
    def __init__( self, file_name: str, overwrite: bool ):
        super().__init__()
        
        self.file_name = file_name
        if not overwrite and file_name and os.path.isfile( file_name ):
            self.graph = mg.importing.import_binary( file_name )
        else:
            self.graph = mg.MGraph()
            self.graph.data = []
        
        self.nodes = { }
        self.edges = { }
        
        for node in self.graph:
            self.nodes[node.data.label, node.data.uid] = node
        
        for edge in self.graph:
            self.edges[edge.data.start, edge.data.label, edge.data.end] = edge
    
    
    def on_write_data( self, data: object ):
        d: List[object] = self.graph.data
        d.append( data )
    
    
    def on_write_node( self, node: NcNode ):
        existing: mg.MNode = self.nodes.get( (node.label, node.uid) )
        
        if existing is None:
            existing = self.graph.add_node( node )
        else:
            d: NcNode = existing.data
            d.properties.update( node.properties )
        
        return existing
    
    
    def on_write_edge( self, edge: NcEdge ):
        start = self.write_node( edge.start )
        end = self.write_node( edge.end )
        
        existing = self.edges.get( (start, edge.label, end) )
        
        if existing is None:
            self.graph.add_edge( start, end, data = edge )
        else:
            d: NcEdge = existing.data
            d.properties.update( edge.properties )
            existing.data = edge
        
        return
    
    
    def on_close( self ) -> None:
        if self.file_name:
            mg.exporting.export_binary( self.graph, self.file_name )
    
    
    def __str__( self ):
        return str( self.graph )
