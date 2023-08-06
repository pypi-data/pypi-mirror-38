"""
The "schema" contains the set of node labels, edge types and properties in the database.

This looks a bit weired: a `NodeSchema` instance is a `Node`, but the class itself has special fields,
methods and a metaclass (`NodeSchemaType`) which allow it to verify its properties.

The same goes for `EdgeSchema`.

When inheriting from `NodeSchema` or `EdgeSchema` the derived class must override the `class_*` fields
to provide information on the class structure. These fields are documented inline below.
"""
import warnings
from typing import Dict, Iterable, Iterator, Tuple, Union, Optional, List, Set, TypeVar

from mhelper import SimpleTypeError, SwitchError, abstract
from neocommand.data import NcNode, NcEdge
from neocommand.neocsv import NeoType


_T = TypeVar( "_T" )


class PropertySchema:
    def __init__( self,
                  name: str,
                  type_: Union[type, NeoType],
                  *,
                  key: Union["NodeSchema", str] = None,
                  is_unique: bool = False,
                  is_index: bool = False,
                  doc: str = None,
                  is_default: bool = False,
                  is_optional: bool = None,
                  is_primary_key: bool = False ):
        """
        :param type_:           Type of the field.
                                Either a python `type` or a `NeoType` are acceptable. 
        :param key:             `None`, or if this field references the primary key of another node, this should be the type of that node.
                                Either the `NodeSchema` type or the `str` label are acceptable. 
        :param is_unique:       If this field should have a unique constraint.
                                (This isn't actually supported for Neo4j edges but Neocommand still allows this to be used as a hint to the programmer). 
        :param is_index:        If this field should be indexed.
        :param doc:             `None`, or any documentation on this field as a `str`. 
        :param is_default:      If this field should be used as the default display the entity to the user.
                                There should only be one such field per entity. 
        :param is_optional:     If the field is optional.
                                If `None`, then the value `not EntitySchema.is_complete` flag is taken.
                                (This isn't actually supported for Neo4j edges but Neocommand still allows this to be used as a hint to the programmer).
        :param is_primary_key:      Reserved for future use. At present `uid` is the only acceptable primary key.
                                Denotes a primary key.
                                If this is set `is_index` and `not is_optional` are assumed.
        """
        if isinstance( type_, type ):
            type_ = NeoType.from_type( type_ )
        
        if is_primary_key:
            is_optional = False
            is_index = True
            is_unique = True
        
        self.type: NeoType = type_
        self.doc = doc
        self.key = key
        self.is_index = is_index
        self.is_default = is_default
        self.__is_optional = is_optional
        self.name = name
        self.entity = None
        self.is_unique = is_unique
        self.is_primary_key = is_primary_key
    
    
    def set_entity( self, entity: "EntitySchema" ) -> None:
        """
        Sets the entity schema upon which this property is present.
        
        :param entity: 
        :return: 
        """
        self.entity = entity
    
    
    @property
    def is_optional( self ) -> bool:
        """
        See __init__
        """
        if self.__is_optional is None:
            return not self.entity.is_complete
        else:
            return self.__is_optional
    
    
    def __repr__( self ):
        return self.get_schema_description()
    
    
    def get_schema_description( self ) -> str:
        x = ["PROP {}:{}".format( self.name, self.type.neo4j_name )]
        
        if self.key:
            x.append( "KEY:{}".format( self.key ) )
        
        if self.is_unique:
            x.append( " UNIQUE" )
        
        if self.is_index:
            x.append( " INDEX" )
        
        if self.is_default:
            x.append( " DEFAULT" )
        
        if self.is_optional:
            x.append( " OPTIONAL" )
        
        if self.is_unique:
            x.append( " UNIQUE" )
        
        if self.is_primary_key:
            x.append( " PRIMARY_KEY" )
        
        return "".join( x )
    
    
    def get_schema_cypher( self ):
        r = []
        
        if isinstance( self.entity, NodeSchema ):
            if self.is_index and not self.is_unique:  # ignore indices where `unique` is set because this is implicit and causes an error in neo4j
                r.append( "CREATE INDEX ON :{}({});".format( self.entity.label, self.name ) )
            
            # TODO: Composite index
            
            if self.is_unique:
                r.append( "CREATE CONSTRAINT ON (x:{}) ASSERT x.{} IS UNIQUE;".format( self.entity.label, self.name ) )
            
            # TODO: Node key
            
            if not self.is_optional:
                r.append( "CREATE CONSTRAINT ON ()-[x:{}]-() ASSERT exists(x.{});".format( self.entity.label, self.name ) )
        else:
            if self.is_index:
                warnings.warn( "Cannot create index on relationship property in neo4j «{}.{}».".format( self.entity.label, self.name ) )
            
            if self.is_unique:
                warnings.warn( "Cannot create unique constraint on relationship property in neo4j «{}.{}».".format( self.entity.label, self.name ) )
            
            if not self.is_optional:
                r.append( "CREATE CONSTRAINT ON ()-[x:{}]-() ASSERT exists(x.{});".format( self.entity.label, self.name ) )
        
        return "\n".join( r )


class PropertyCollection:
    """
    The collection of properties associated with an entity schema.
    """
    
    
    def __init__( self, entity: "EntitySchema", properties: Optional[Iterable[PropertySchema]] ):
        self.entity: EntitySchema = entity
        self.__contents: List[PropertySchema] = []
        self.default: PropertySchema = None
        self.primary_key: PropertySchema = None
        
        if properties is None:
            properties = ()
        
        for property in properties:
            self.__append( property )
        
        if isinstance( entity, NodeSchema ):
            if self.primary_key is None:
                self.__append( PropertySchema( "uid", str, is_primary_key = True ) )
    
    
    def __append( self, property: PropertySchema ) -> None:
        property.set_entity( self.entity )
        
        if property.is_default:
            self.default = property
        
        if property.is_primary_key:
            self.primary_key = property
        
        self.__contents.append( property )
    
    
    def __iter__( self ) -> Iterator[PropertySchema]:
        return iter( self.__contents )
    
    
    def __len__( self ):
        return len( self.__contents )


@abstract
class EntitySchema:
    """
    Base class that defines the schema of a node or edge.
    See `__init__` for field descriptions.
    """
    
    
    def __init__( self, label: str, properties: Optional[Iterable[PropertySchema]], is_complete: bool, is_verified: bool ):
        """
        :param label:           Label of node or type of edge 
        :param properties:      Properties on entity. See `PropertySchema`. 
        :param is_complete:     True if the properties presented represent the complete set.  
        :param is_verified:     Only `False` if the `DatabaseSchema` had to create this schema itself because
                                no suitable schema for a node or edge exists. 
        """
        self.label: str = label
        self.is_complete: bool = is_complete
        self.is_verified = is_verified
        self.properties = PropertyCollection( self, properties )
    
    
    @property
    def default_property( self ):
        """
        See `PropertyCollection.default`
        """
        return self.properties.default
    
    
    def get_schema_cypher( self ) -> str:
        r = []
        
        for property in self.properties:
            cypher = property.get_schema_cypher()
            if cypher:
                r.append( cypher )
        
        return "\n".join( r )
    
    
    def __str__( self ):
        return self.label


class NodeSchema( EntitySchema ):
    """
    Schema on nodes
    See `__init__` for field descriptions.
    """
    
    
    def __init__( self, label: str, properties: Iterable[PropertySchema] = None, *, is_complete: bool = None, is_verified: bool = True ):
        """
        :param label:         See `EntitySchema.__init__`.
        :param properties:    See `EntitySchema.__init__`.
        :param is_complete:   See `EntitySchema.__init__`.
        :param is_verified:   See `EntitySchema.__init__`.
        """
        super().__init__( label, properties, is_complete, is_verified )
    
    
    def get_schema_description( self ):
        r = []
        r.append( "NODE (:{}){}".format( self.label, "" if self.is_verified else " (?)" ) )
        
        for v in self.properties:
            r.append( "  " + v.get_schema_description() )
        
        if not self.is_complete:
            r.append( "  PROP __any_custom__:any" )
        
        return "\n".join( r )
    
    
    def describe( self, node: NcNode ) -> str:
        """
        Uses the available schema to get a human-readable description of a node.
        """
        if self.default_property is None or self.default_property.name == "uid":
            r = node.uid
        else:
            r = node.properties.get( self.default_property, None )
            
            if r is not None:
                return str( r )
            
            r = node.uid
        
        if r is not None:
            return r
        
        if node.iid:
            return "ID={}".format( node.iid )
        else:
            return "?"


class EdgeSchema( EntitySchema ):
    """
    Schema on edges
    See `__init__` for field descriptions.
    """
    
    
    def __init__( self,
                  start: Union[NodeSchema, str],
                  label: str,
                  end: Union[NodeSchema, str],
                  properties: Iterable[PropertySchema] = None,
                  *,
                  is_complete: bool = None,
                  is_verified: bool = True ):
        """
        :param start:              `NodeSchema` or `str` denoting the start node type or label.
        :param label:              See `EntitySchema.__init__`.
        :param end:                `NodeSchema` or `str` denoting the end node type or label.
        :param properties:         See `EntitySchema.__init__`.
        :param is_complete:        See `EntitySchema.__init__`.
        :param is_verified:        See `EntitySchema.__init__`.
        """
        if isinstance( start, NodeSchema ):
            start = start.label
        
        if isinstance( end, NodeSchema ):
            end = end.label
        
        super().__init__( label = label, properties = properties, is_complete = is_complete, is_verified = is_verified )
        self.start_label = start
        self.end_label = end
    
    
    def get_schema_description( self ):
        r = []
        r.append( "  EDGE (:{})-[:{}]->(:{}){}".format( self.start_label, self.label, self.end_label, "" if self.is_verified else " (?)" ) )
        
        for property in self.properties:
            r.append( "    " + property.get_schema_description() )
        
        if not self.is_complete:
            r.append( "    PROP __any_custom__:any" )
        
        return "\n".join( r )


class NodeSchemaCollection:
    """
    Collection of node schemas.
    """
    
    
    def __init__( self ):
        self.__content: Dict[str, NodeSchema] = { }
    
    
    def __str__( self ):
        return "{} node schema".format( len( self.__content ) )
    
    
    def append( self, t: NodeSchema ):
        self.__content[t.label] = t
    
    
    def __iter__( self ) -> Iterator[NodeSchema]:
        return iter( self.__content.values() )
    
    
    def items( self ):
        return self.__content.items()
    
    
    def __len__( self ):
        return len( self.__content )
    
    
    def __getitem__( self, label ):
        return self.__content[label]
    
    
    def get( self, label, default = None ):
        """
        Obtains the matching schema.
        """
        return self.__content.get( label, default )
    
    
    def create( self, label ) -> NodeSchema:
        """
        Obtains the schema associated with a label, or creates it if it doesn't exist.
        Any new schema is created unverified, meaning it can be overwritten by a more concrete version without error.
        
        :param label:   Label on the schema 
        :return:        Existing or new schema 
        """
        schema = self.get( label )
        
        if schema is None:
            schema = NodeSchema( label, is_verified = False )
            self.append( schema )
        
        return schema


class EdgeSchemaCollection:
    """
    Collection of edge schemas.
    """
    
    
    def __init__( self ):
        self.__content: Dict[Tuple[str, str, str], EdgeSchema] = { }
    
    
    def __str__( self ):
        return "{} edge schema".format( len( self.__content ) )
    
    
    def append( self, t: EdgeSchema ):
        self.__content[(t.start_label, t.label, t.end_label)] = t
    
    
    def items( self ):
        return self.__content.items()
    
    
    def __iter__( self ) -> Iterator[EdgeSchema]:
        return iter( self.__content.values() )
    
    
    def __len__( self ):
        return len( self.__content )
    
    
    def __getitem__( self, labels: Tuple[str, str, str] ):
        return self.__content[labels]
    
    
    def get( self, start_label: str, edge_label: str, end_label: str, default = None ):
        """
        Obtains the matching schema.
        """
        return self.__content.get( (start_label, edge_label, end_label), default )
    
    
    def create( self, start_label: str, edge_label: str, end_label: str ):
        """
        Obtains the schema associated with a label, or creates it if it doesn't exist.
        Any new schema is created unverified, meaning it can be overwritten by a more concrete version without error.
        
        :param start_label:  Label on the schema
        :param edge_label:   Label on the schema
        :param end_label:    Label on the schema
        :return:             Existing or new schema
        """
        schema = self.get( start_label, edge_label, end_label )
        
        if schema is None:
            schema = EdgeSchema( start_label, edge_label, end_label, is_verified = False )
            self.append( schema )
        
        return schema


class DatabaseSchema:
    """
    Manages a collection of node and `NodeSchema` and `EdgeSchema` types.
    This is a "documentation" of the schema available, and probably won't reflect the schema of the database itself.
    
    :ivar node_schema: Node schema types, a list of `NodeSchema`.
    :ivar edge_schema: Edge schema types. a list of `EdgeSchema`.
    """
    
    
    def __init__( self ):
        self.node_schema = NodeSchemaCollection()
        self.edge_schema = EdgeSchemaCollection()
    
    
    def iter_entity_types( self ) -> Iterator[EntitySchema]:
        """
        Iterates all schemas.
        """
        yield from self.node_schema
        yield from self.edge_schema
    
    
    def get_distinct_property_names( self ) -> Set[str]:
        """
        Gets the set of all property names, only listing identical names once.
        """
        s = set()
        
        for nt in self.iter_entity_types():
            s.update( x.name for x in nt.properties )
        
        return s
    
    
    def __repr__( self ):
        return "DatabaseSchema(n={},e={})".format( len( self.node_schema ), len( self.edge_schema ) )
    
    
    def get_schema( self, node: Union[NcNode, NcEdge] ) -> EntitySchema:
        """
        Gets the relevant schema for a node or edge.
        If not present, a default one is created.
        
        :param node: `NcNode` or `NcEdge`.    
        :return:     The schema for that node. 
        """
        if isinstance( node, NcNode ):
            return self.node_schema.create( node.label )
        elif isinstance( node, NcEdge ):
            return self.edge_schema.create( node.start.label, node.label, node.end.label )
        else:
            raise SimpleTypeError( "entity", node, Union[NodeSchema, EdgeSchema] )
    
    
    def describe( self, node: NcNode ) -> str:
        """
        Uses the available schema to get a human-readable description of a node.
        """
        return self.node_schema.create( node.label ).describe( node )
    
    
    def get_schema_cypher( self ):
        """
        Obtains the Cypher script used to instantiate the documented schema in the database.
        """
        r = []
        
        for entity in self.iter_entity_types():
            cypher = entity.get_schema_cypher()
            if cypher:
                r.append( cypher )
        
        return "\n".join( r )
    
    
    def get_schema_description( self ):
        """
        Obtains text to describe the documented schema.
        """
        r = []
        r.append( "{} node and {} edge schema".format( len( self.node_schema ), len( self.edge_schema ) ) )
        
        e = list( self.edge_schema )
        
        for node in self.node_schema:
            r.append( node.get_schema_description() )
            
            for edge in self.edge_schema:
                if edge.start_label == node.label:
                    r.append( edge.get_schema_description() )
                    e.remove( edge )
        
        if e:
            r.append( "UNPAIRED EDGES:" )
            for edge in e:
                r.append( edge.get_schema_description() )
        
        return "\n".join( r )
    
    
    def register( self, schema: _T ) -> _T:
        """
        Documents a new schema.
        """
        if isinstance( schema, NodeSchema ):
            self.node_schema.append( schema )
        elif isinstance( schema, EdgeSchema ):
            self.edge_schema.append( schema )
        else:
            raise SwitchError( "schema", schema, instance = True )
        
        return schema
