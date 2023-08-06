from collections import OrderedDict
from typing import Dict, List, Tuple, ValuesView

from neocommand.data.entities import NcEdge, NcNode


class EdgeNodeDict:
    """
    Holds, processes and manages the data passed to the `on_create_content` function.
    """


    def __init__( self, nodes_: List[NcNode], edges_: List[NcEdge] ):
        self.__nodes: Dict[str, Tuple[NcNode, int]] = OrderedDict()
        self.__edges: Dict[str, Tuple[NcEdge, int, int, int]] = OrderedDict()
        
        for node in nodes_:
            self.__add_node_to_list( node, self.__nodes )

        for edge in edges_:
            start, start_id = self.__add_node_to_list( edge.start, self.__nodes )
            end, end_id = self.__add_node_to_list( edge.end, self.__nodes )

            if edge is None:
                continue

            local_key = "\t".join( [edge.label, start.label, start.uid, end.label, end.uid] )

            if local_key in self.__edges:
                continue

            self.__edges[local_key] = edge, len( self.__edges ), start_id, end_id


    @property
    def nodes_and_ids( self ) -> ValuesView[Tuple[NcNode, int]]:
        """
        Obtains an iterator over tuples specifying
            * the nodes to write
            * their arbitrary IDs for this session.
        """
        return self.__nodes.values()


    @property
    def edges_and_ids( self ):
        """
        Obtains an iterator over tuples specifying
            * the edges to write
            * their arbitrary IDs for this session.
            * the id of the start node
            * the id of the end node
        """
        return self.__edges.values()


    @property
    def edges( self ):
        """
        Obtains an iterator the edges to write.
        """
        return (x[0] for x in self.__edges.values())


    @property
    def nodes( self ):
        """
        Obtains an iterator the nodes to write.
        """
        return (x[0] for x in self.__nodes.values())


    def __add_node_to_list( self, node: NcNode, nodes: Dict[str, Tuple[NcNode, int]] ) -> Tuple[NcNode, int]:
        local_key: str = self.__get_node_local_key( node )

        if local_key in nodes:
            return nodes[local_key]

        id_ = len( nodes )
        nodes[local_key] = node, id_

        return node, id_


    @staticmethod
    def __get_node_local_key( node: NcNode ) -> str:
        assert node.label
        assert node.uid

        local_key = [str( node.label ), str( node.uid )]
        return "\t".join( local_key )


    def get_node_id( self, node: NcNode ):
        """
        Gets the arbitrary id for this session of a particular node.

        :except KeyError: NcNode not present in this session
        """
        return self.__nodes[self.__get_node_local_key( node )][1]
