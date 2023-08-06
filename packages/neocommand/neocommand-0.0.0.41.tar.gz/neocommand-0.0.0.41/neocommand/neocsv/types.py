from typing import Optional, List, Dict

from mhelper import NOT_PROVIDED, array_helper, NotFoundError, string_helper


class NeoType:
    """
    Represents a neo4j type.
    
    :ivar neo4j_name:   Name in Neo4j
    :ivar element_type: Python type (never an array)
    :ivar is_array:     Is this an array
    :ivar ARRAY:        Array equivalent
    :ivar NO_ARRAY:     Not-an-array equivalent
    """
    
    
    def __init__( self, neo4j_name: str, element_type: type, parent: "NeoType" = None ):
        self.neo4j_name = neo4j_name
        self.element_type: type = element_type
        
        if parent is None:
            self.is_array = False
            self.ARRAY = NeoType( neo4j_name + "[]", element_type, self )
            self.NO_ARRAY = self
        else:
            self.is_array = True
            self.ARRAY = self
            self.NO_ARRAY = parent
        
        assert self.ARRAY is not None
        assert self.NO_ARRAY is not None
    
    
    def get_id( self ):
        if self.is_array:
            return self.neo4j_name
        else:
            return self.neo4j_name + "[]"
    
    
    def string_to_value( self, text: str, array_delimiter: Optional[str] ) -> object:
        """
        Given a `text` string, convert it into a (Python) value of this type.
        """
        if self.is_array:
            return [self.NO_ARRAY.string_to_value( x, None ) for x in text.split( array_delimiter )]
        else:
            # noinspection PyTypeChecker
            return self.element_type( text )
    
    
    def __str__( self ):
        return "Neo4j::{} ({}{})".format( self.neo4j_name, "LIST OF " if self.is_array else "", self.element_type )
    
    
    def to( self, neo_type: "NeoType" ):
        if self.is_array:
            return neo_type.ARRAY
        else:
            return neo_type.NO_ARRAY
    
    
    @classmethod
    def from_name( cls, text: str ) -> "NeoType":
        """
        Find the type from the name.
        
        :param text:        Neo4j type name 
        :return:            Corresponding type
        :except KeyError:   Not found 
        """
        try:
            return cls._BY_NAME[text]
        except KeyError as ex:
            raise NotFoundError( "The value «{}» is not a valid Neo4j type name from the options «{}».".format( text, string_helper.join_ex( cls._BY_NAME ) ) ) from ex
    
    
    @classmethod
    def from_type( cls, element_type: type ):
        """
        Find the type from the `element_type` (never an array).
        """
        return cls._BY_TYPE[element_type]
    
    
    INT: "NeoType" = None
    FLOAT: "NeoType" = None
    STR: "NeoType" = None
    BOOL: "NeoType" = None
    ALL: List["NeoType"] = None
    ALLA: List["NeoType"] = None
    _BY_NAME: Dict[str, "NeoType"] = None
    _BY_TYPE: Dict[type, "NeoType"] = None


NEO_TYPE_COLLECTION = NeoType  # deprecated
NEO_FALSE = "false"
NEO_TRUE = "true"  # Note the only root_object neo4j sees as True for a boolean property is "true", everything else (even "1" and "True") is False, apart from "", which is null.

NeoType.INT = NeoType( "int", int )
NeoType.FLOAT = NeoType( "float", float )
NeoType.STR = NeoType( "string", str )
NeoType.BOOL = NeoType( "boolean", bool )
NeoType.ALL = [NeoType.INT, NeoType.FLOAT, NeoType.STR, NeoType.BOOL]
NeoType.ALLA = list( NeoType.ALL ) + [x.ARRAY for x in NeoType.ALL]
NeoType._BY_NAME = dict( (x.neo4j_name, x) for x in NeoType.ALLA )
NeoType._BY_TYPE = dict( (x.element_type, x) for x in NeoType.ALL )
NeoType.by_name = NeoType._BY_NAME  # deprecated
NeoType.by_type = NeoType._BY_TYPE  # deprecated
