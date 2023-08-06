import warnings
from os import path
from typing import Dict, Iterator, List, Optional, Tuple, Type, TypeVar, Union
from intermake import pr
from mhelper import ManagedWith, NotSupportedError, SwitchError, TTristate, array_helper, io_helper, exception_helper

from neocommand.data import NcData, NcEdge, NcEntity, NcNode
from neocommand.helpers import EdgeSchema, NodeSchema
from neocommand.helpers.resolver import EdgeNodeDict


class Endpoint:
    """
    ABSTRACT
    
    Base class for all endpoints.
    
    All endpoints possess a `name` field and a `remove` method, the latter of which is used to
    clean-up after removing an endpoint. The `name` field is for accessing user-created endpoints
    and may be left as `None` for temporary endpoints.
    
    .. note::
    
        Only `Origin` and `Destination` should derive from this class directly.
        Concrete endpoints should derived from one or both of these.
        
    .. note::
        
        User-creatable endpoints should be serialisable.
    """
    
    
    def __init__( self, name = None ):
        self.name: str = name if name is not None else ("untitled_{}".format( type( self ).__name__ ))
    
    
    def remove( self, delete: bool ):
        """
        Cleans up the endpoint before removal.
        
        :param delete:  Request to delete data from disk also.
        :except         Exception:  The endpoint may raise any `Exception`, this prevents deletion.
        """
        self.on_removed( delete )
    
    
    def on_removed( self, delete: bool ) -> None:
        """
        VIRTUAL
        
        The derived class should perform any handling when the endpoint is deleted by the user.
        Calling the base class is optional: this simply raises a "Cannot delete data from disk"
        error if the `delete` flag is set.
        
        :param delete:      Request to delete data from disk also.
                            A exception should be raised if this is not applicable.
        :except Exception:  The endpoint may raise any `Exception`, this prevents deletion.
        """
        if delete:
            raise ValueError( "Cannot delete data from disk for this endpoint." )
    
    
    def __repr__( self ):
        """
        OVERRIDE
        """
        return "{}({})".format( type( self ).__name__, repr( self.name ) )


class Origin( Endpoint ):
    """
    ABSTRACT
    
    Endpoints that have an `open_reader` method that can be used to obtain a target to read data from.
    """
    
    
    def open_reader( self ) -> ManagedWith["Reader"]:
        return ManagedWith["OpenOrigin"]( target = self.on_open_reader(),
                                          on_exit = Reader.close )
    
    
    def on_open_reader( self ) -> "Reader":
        raise NotImplementedError( "abstract" )


class Reader( Origin ):
    """
    ABSTRACT
    
    An `Origin` `Endpoint` that is open for reading.
    
    Its life cycle begins with a call to `with Destination.open_reader` and is ended when that
    `with` block terminates, calling `Reader.close`.
    
    .. note::
    
        A `Reader` can itself act as an `Origin`, however an `Origin` should never be a `Reader`,
        since `Reader` is unable to close itself.
    """
    
    
    def open_reader( self ) -> ManagedWith["Reader"]:
        return ManagedWith[Reader]( target = self )
    
    
    def on_open_reader( self ) -> "Reader":
        raise ValueError( "Unexpected call." )
    
    
    def close( self ):
        self.on_close()
    
    
    def on_close( self ):
        pass
    
    
    def read_all( self ) -> Iterator[object]:
        """
        Iterates over all contents of this endpoint.
        
        Contents include:
            * `NcNode` - Nodes
            * `NcEdge` - Edges
            * `NcData` - Data items
            * `Origin` - Nested endpoints
        """
        return self.on_read_all()
    
    
    def read_all_flat( self ) -> Iterator[NcEntity]:
        """
        Applies `read_all` but any nested endpoints are extracted recursively.
        """
        for x in self.read_all():
            if isinstance( x, NcEntity ):
                yield x
            elif isinstance( x, Origin ):
                with x.open_reader() as r:
                    yield from r.read_all_flat()
            else:
                warnings.warn( "Unrecognised `Origin` `on_read_all` yield: {}".format( repr( x ) ), UserWarning )
    
    
    def read_all_props( self, label: str, property: str ) -> Iterator[Tuple[str, object]]:
        return self.on_read_all_props( label, property )
    
    
    def on_read_all( self ) -> Iterator[object]:
        """
        The derived class should yield all its contents: Nodes, edges, data items and any nested endpoints (i.e. paths or folders).
        
        :except InvalidEntityError:    Failed to locate entity
        :except EndpointSupportError:  The endpoint does not support this feature
        """
        raise EndpointSupportError( self )
    
    
    def on_read_all_props( self, label: str, property: str ) -> Iterator[Tuple[str, object]]:
        """
        Gets a UID-to-property dictionary for the specified node label.
         
        :param label:      Label of node 
        :param property:   Property to get 
        :return:           Iterator over UIDs and properties: Tuple[UID, property-value]
        :except NotSupportedError:  The endpoint does not support this feature
        """
        raise EndpointSupportError( self )


# noinspection PyAbstractClass
class Destination( Endpoint ):
    """
    ABSTRACT
    
    Endpoints that have an `open_writer` method that can be used to obtain a target to write data into.
    """
    
    
    def open_writer( self ) -> ManagedWith["Writer"]:
        """
        Allows a `with` block to encapsulate `prepare` and `close`.
        """
        return ManagedWith["OpenDestination"]( target = self.on_open_writer(),
                                               on_exit = Writer.close )
    
    
    def on_open_writer( self ) -> "Writer":
        raise NotImplementedError( "abstract" )


class Writer( Destination ):
    """
    ABSTRACT
    
    A `Destination` `Endpoint` that is open for writing.
    
    Its life cycle begins with a call to `with Destination.open_writer` and is ended when that
    `with` block terminates, calling `Writer.close`.
    
    .. note::
    
        A `Writer` can itself act as a `Destination`, however a `Destination` should never be a
        `Writer`, since `Writer` is unable to close itself.
    """
    
    
    def close( self ):
        self.on_close()
    
    
    def open_writer( self ) -> ManagedWith["Writer"]:
        return ManagedWith[Writer]( target = self )
    
    
    def on_open_writer( self ) -> "Writer":
        raise ValueError( "Unexpected call." )
    
    
    def create_node( self, *, label: NodeSchema, uid: str, properties: Dict[str, object] ):
        """
        FINAL
        
        Adds a node to the endpoint.

        If a node with the same label and UID does not already exists it should be created.
        The endpoint should update the specified `properties` on the node. object other properties should remain intact.
        
        :param label:       Node label 
        :param uid:         Node UID 
        :param properties:  Node properties to be updated.
                                ¡WARNING!
                                The caller should NOT assume that `properties` is not modified.
                                The implementing class is free to modify this dictionary (thus avoiding copies where unnecessary).
        :return:            The created node
        :except AddFailedError:     The add failed.
        :except NotSupportedError:  The endpoint does not support this feature
        """
        node = NcNode( label = label.label, uid = uid, properties = properties )
        self.write_node( node )
        return node
    
    
    def create_edge( self,
                     *,
                     label: EdgeSchema,
                     start_uid: str,
                     end_uid: str,
                     properties: Dict[str, object] ):
        """
        FINAL
        
        Adds an edge to the endpoint.
        
        If an edge with the same label does not exist between the specified nodes, the edge should be created.
        The endpoint should update the specified `properties` on the edge. object other properties should remain intact.
        
        If the specified nodes do not exist, the behaviour is undefined (preferably an exception, though this cannot be guaranteed).
         
        :param label:           Edge schema 
        :param start_uid:       Starting node UID 
        :param end_uid:         Ending node UID 
        :param properties:      Edge properties to be updated.
                                    ¡WARNING!
                                    The caller should NOT assume that `properties` is not modified.
                                    The implementing class is free to modify this dictionary (thus avoiding copies where unnecessary).
        :return: The created edge
        :except AddFailedError:     The add failed.
        :except NotSupportedError:  The endpoint does not support this feature
        """
        start = NcNode( label = label.start_label, uid = start_uid, properties = { } )
        end = NcNode( label = label.end_label, uid = end_uid, properties = { } )
        edge = NcEdge( label = label.label, start = start, end = end, properties = properties )
        self.write_edge( edge )
        return edge
    
    
    def write_node( self, node: NcNode ):
        """
        FINAL
        
        See `create_node`. 
        """
        exception_helper.safe_cast( "node", node, NcNode )
        self.on_write_node( node )
    
    
    def write_edge( self, edge: NcEdge ):
        """
        FINAL
        
        See `create_edge`.
        """
        exception_helper.safe_cast( "edge", edge, NcEdge )
        self.on_write_edge( edge )
    
    
    def open_folder( self, name: str ) -> ManagedWith["Writer"]:
        """
        FINAL
        
        This allows a `with` block to encapsulate `write_folder`.
        The folder is returned from `with as` and flushed at the end of the
        `with` block.
        """
        return self.write_folder( name ).open_writer()
    
    
    def write_folder( self, name: str ) -> "Destination":
        """
        FINAL
        
        Adds a folder to the endpoint.
        
        Folders logically sort the results for the GUI, they may not have any actual effect if writing
        to a file, in which case the endpoint may just return it`self`.
        
        The default implementation of this function returns `self`, hence this function should never raise a `NotSupportedError`.
        
        :param name:                Folder name 
        :return:                    The new endpoint for this folder
        :except AddFailedError:     The add failed.
        """
        return self.on_write_folder( name )
    
    
    def write_data( self, data: NcData ) -> None:
        """
        FINAL
        
        Adds arbitrary data to the endpoint.
        Note that not all endpoints support the addition of arbitrary data.
        
        If the endpoint does not support this operation it will ideally fail silently or issue a warning, allowing other operations to proceed,
        This does not mean that this function will not raise, cases such as malformed data may still raise the appropriate exception.
        
        :param data: Data to add.
        :return: 
        """
        exception_helper.safe_cast( "data", data, NcData )
        self.on_write_data( data )
    
    
    def write_entity( self, entity: object ):
        """
        FINAL
        
        Inspects the type to call `write_edge`/`write_node`/`write_data`/`write_all` as appropriate.
        May not be used for arbitrary data.
        
        :param entity:  Node or edge to add.
        """
        if isinstance( entity, NcEdge ):
            self.write_edge( entity )
        elif isinstance( entity, NcNode ):
            self.write_node( entity )
        elif isinstance( entity, NcData ):
            self.write_data( entity )
        elif isinstance( entity, Origin ):
            self.write_all( entity )
        else:
            raise SwitchError( "entity", entity, instance = True )
    
    
    def write_all( self, origin: Origin ):
        """
        FINAL
        
        Iterates the `origin` and adds all entities to this endpoint.
        """
        with self.open_folder( origin.name ) as folder:
            with origin.open_reader() as reader:
                for x in reader.read_all():
                    folder.write_entity( x )
    
    
    def on_write_data( self, data: NcData ):
        """
        VIRTUAL
        
        Abstracted implementation of `write_data`.
        """
        if data is None:
            return
        
        warnings.warn( "This {} endpoint «{}» does not support the adding of arbitrary (non-node/edge) data «{}». This action has been ignored.".format( type( self ).__name__, self, data ) )
    
    
    def on_write_node( self, node: NcNode ):
        """
        ABSTRACT
        
        Abstracted implementation of `write_node`.
        """
        raise NotImplementedError( "abstract" )
    
    
    def on_write_edge( self, edge: NcEdge ):
        """
        ABSTRACT
        
        Abstracted implementation of `write_edge`.
        """
        raise NotImplementedError( "abstract" )
    
    
    def on_write_folder( self, name: str ) -> "Destination":
        """
        VIRTUAL
        
        Abstracted implementation of `write_folder`.
        """
        return self
    
    
    def on_close( self ) -> None:
        """
        VIRTUAL
        
        This is called when `close` is called for the final time and the endpoint is flagged as dirty.
        The derived class may perform any cool-down or write the results to disk.
        """
        pass


class AddFailedError( Exception ):
    """
    Endpoints raise this if an add fails for any reason.
    """
    pass


class InvalidEntityError( Exception ):
    """
    An error used when trying to retrieve an entity from the database when that entity does not exist in the database.
    """
    pass


class EndpointSupportError( NotSupportedError ):
    def __init__( self, endpoint ):
        super().__init__( "Sorry, but this «{}» endpoint does not support the requested feature. Please use a different endpoint for this purpose.".format( endpoint ) )


T = TypeVar( "T" )


# noinspection PyAbstractClass
class AbstractListBackedEndpoint( Origin, Destination ):
    def __init__( self, name: str ):
        super().__init__( name )
    
    
    @property
    def contents( self ) -> List[Optional[object]]:
        raise NotImplementedError( "abstract" )
    
    
    def only_child( self, expected: Optional[Type[T]] = None ) -> T:
        """
        Returns the only child of this folder, or `None` if it is empty.
        Raises a `ValueError` if there is more than 1 item.
        """
        contents = self.contents
        
        if len( contents ) == 0:
            raise ValueError( "Cannot obtain the only child of a {} «{}» because the folder doesn't contain any elements.".format( type( self ), self ) )
        elif len( contents ) == 1:
            result = contents[0]
            
            from neocommand.endpoints.memory_endpoint import MemoryEndpoint
            if isinstance( result, MemoryEndpoint ):
                result = result.only_child( expected )
            
            if expected is not None:
                if not isinstance( result, expected ):
                    raise ValueError( "Cannot obtain the only child of a {} «{}» because the result is of type «{}», not the expected type «{}».".format( type( self ), self, type( result ), expected ) )
            
            return result
        
        else:
            raise ValueError( "Cannot obtain the only child of a {} «{}» because the folder contains more than 1 child.".format( type( self ), self ) )
    
    
    def as_text( self ) -> List[str]:
        """
        Sometimes we want basic text from the database, such as UIDs or names.
        Our `DbManager` still gives back the results as `Docket`s, so we use this function to pull the text from the dockets into a simple list. 
        :return: 
        """
        result = [array_helper.decomplex( x ) for x in self.contents]  # due to mistakes in parsing, sometimes items are stored in the database as strings inside lists of length 1, this just pulls them out
        
        for x in result:
            if not isinstance( x, str ):
                raise ValueError( "At least one element is not `str` in `docket_to_text. The offending item is of type «{0}» and has a value of «{1}»".format( type( x ).__name__, repr( x ) ) )
        
        # noinspection PyTypeChecker
        return result
    
    
    def on_open_writer( self ):
        return _ListBackedEndpointWriter( self.contents )
    
    
    def on_open_reader( self ):
        return _ListBackedEndpointReader( self.contents )


class _ListBackedEndpointReader( Reader ):
    def __init__( self, contents: List[Optional[object]] ):
        super().__init__()
        self.contents = contents
    
    
    def on_read_all( self ) -> Iterator[object]:
        return iter( self.contents )
    
    
    def on_read_all_props( self, label: str, property: str ) -> Iterator[Tuple[str, object]]:
        for x in self.on_read_all():
            if not isinstance( x, NcNode ) or x.label != label:
                continue
            
            if x.data is not None and property in x.data:
                yield x.uid, x.data[property]


class _ListBackedEndpointWriter( Writer ):
    def __init__( self, contents: List[Optional[object]] ):
        super().__init__()
        self.contents = contents
    
    
    def on_write_folder( self, name: str ) -> Destination:
        from neocommand.endpoints.memory_endpoint import MemoryEndpoint
        result = MemoryEndpoint( name = name )
        self.contents.append( result )
        return result
    
    
    def on_write_data( self, data: object ):
        self.contents.append( data )
    
    
    def on_write_edge( self, edge: NcEdge ):
        self.contents.append( edge )
    
    
    def on_write_node( self, node: NcNode ):
        self.contents.append( node )


class AbstractFileDestination( Writer ):
    
    
    def __init__( self, file_name, overwrite ):
        super().__init__()
        self.__file_name = file_name
        self.__overwrite: TTristate = overwrite
        self.__edges: List[NcEdge] = []
        self.__nodes: List[NcNode] = []
    
    
    @property
    def file_name( self ) -> str:
        return self.__file_name
    
    
    def on_write_edge( self, edge: NcEdge ):
        self.__edges.append( edge )
    
    
    def on_write_node( self, node: NcNode ):
        self.__nodes.append( node )
    
    
    def on_close( self ) -> None:
        if self.__overwrite is not False:
            if path.exists( self.__file_name ):
                if self.__overwrite is False:
                    raise FileExistsError( "Refusing to write to the file endpoint targeted at «{}» because the overwrite flag is «{}» on this endpoint and the file already exists, «{}».".format( self.__overwrite, self.__file_name, self ) )
                elif self.__overwrite is None:
                    warnings.warn( "The output file already exists and will be overwritten: {}".format( self.__file_name ) )
                else:
                    raise SwitchError( "self.__overwrite", self.__overwrite )
        
        end = EdgeNodeDict( self.__nodes, self.__edges )
        data = self.on_create_content( end )
        ext = self.on_get_file_type()
        
        with io_helper.open_write( self.__file_name, ext, type( data ) ) as file_out:
            file_out.write( data )
        
        pr.printx( "<verbose>Flushed {} endpoint to disk: {}\n" \
                   "{} nodes and {} edges.</verbose>".format(
                self.on_get_file_type(),
                self.__file_name,
                len( end.nodes_and_ids ),
                len( end.edges_and_ids ) ) )
        
        self.__edges.clear()
        self.__nodes.clear()
    
    
    def on_get_file_type( self ) -> str:
        """
        The derived class should implement this method by returning a short string denoting the file type being written, e.g. "GEXF" or "XML".
        """
        raise NotImplementedError( "abstract" )
    
    
    def on_create_content( self, data: "EdgeNodeDict" ) -> Union[str, bytes]:
        """
        The derived class should implement this method by converting the provided data to a string and returning it.
        """
        raise NotImplementedError( "abstract" )
