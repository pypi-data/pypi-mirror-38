"""
Container classes which hold items destined for, or retrieved from, Neo4j.
"""
from typing import Dict, Optional

from mhelper import abstract


__author__ = "Martin Rusilowicz"

EDGE_UID_DELIMITER = ":"


@abstract
class NcEntity:
    """
    Base class for graph entities.
    
    The entities:
        * may have a database presence, or not
        * may be complete or partial
        * are internally serialisable
        * are abstracted from the endpoint
    """
    
    
    def __init__( self, varname: Optional[str] ):
        """
        CONSTRUCTOR
        
        :param varname: Name of the variable pointing to this entity.
                        Can be `None` if this is irrelevant in the current context. 
        """
        self.varname: str = varname
    
    
    def __str__( self ):
        v = self.on_get_str()
        if self.varname:
            return "“{} = {}”".format( self.varname, v )
        else:
            return "“untitled = {}”".format( v )
    
    
    def __repr__( self ):
        v = self.on_get_repr()
        if self.varname:
            return "{}(varname = {}, {})".format( type( self ).__name__, repr( self.varname ), v )
        else:
            return "{}(untitled, {})".format( type( self ).__name__, v )
    
    
    @abstract
    def on_get_str( self ):
        raise NotImplementedError( "abstract" )
    
    
    @abstract
    def on_get_repr( self ):
        raise NotImplementedError( "abstract" )


class NcData( NcEntity ):
    """
    Arbitrary data returned from a Neo4j query.
    Associates a value with a variable name.
    """
    
    
    def __init__( self, varname: str, value: object ):
        super().__init__( varname )
        self.value = value
    
    
    def on_get_str( self ):
        return "{}".format( repr( self.value ) )
    
    
    def on_get_repr( self ):
        return "value={}".format( repr( self.value ) )


class NcNode( NcEntity ):
    """
    A node returned from, or destined for, a Neo4j query.
    """
    
    
    def __init__( self,
                  *,
                  varname: Optional[str] = None,
                  label: str,
                  uid: str,
                  iid: Optional[int] = None,
                  properties: Dict[object, object] = None ):
        """
        :param *: 
        :param varname:     (passed to base class)
        :param label:       Label of the node. 
        :param uid:         UID of the node.
        :param iid:         ID of the node, if known. Can be `None`.  
        :param properties:  Data on the node, if known. `None` equates to `{}`.
        """
        if not label:
            raise ValueError( "A node must have a label." )
        
        if not uid:
            raise ValueError( "A node must have a UID." )
        
        super().__init__( varname )
        
        self.label = label
        self.uid = uid
        self.iid = iid
        
        if properties is not None:
            self.properties = properties
        else:
            self.properties = { }
    
    
    def on_get_str( self ):
        return "({}:{})".format( self.label, self.uid )
    
    
    def on_get_repr( self ):
        return "label={}, uid={}, iid={}, properties.len".format( repr( self.label ), repr( self.uid ), repr( self.iid ), len( self.properties ) )


class NcEdge( NcEntity ):
    """
    An edge returned from, or destined for, a Neo4j query.
    """
    
    
    def __init__( self,
                  *,
                  varname: str = None,
                  label: str,
                  start: NcNode,
                  end: NcNode,
                  iid: Optional[int] = None,
                  properties: Optional[Dict[object, object]] ):
        """
        :param *:   
        :param iid:         Neo4j ID of the edge, if known. 
        :param label:       Label of the edge.
        :param start:       Start node of the edge.
        :param end:         End node of the edge.
        :param properties:  Data on the edge, if known. `None` equates to `{}`.
        """
        super().__init__( varname )
        self.label = label
        self.start = start
        self.iid = iid
        self.end = end
        self.properties = properties
    
    
    def on_get_str( self ):
        return "{}-[{}:{}]->{}".format( self.start, self.iid if self.iid is not None else "", self.label, self.end )
    
    
    def on_get_repr( self ):
        return "label={}, start={}, iid={}, end={}, properties.len={}".format( repr( self.label ),
                                                                               repr( self.start ),
                                                                               repr( self.iid ),
                                                                               repr( self.end ),
                                                                               len( self.properties ) )
