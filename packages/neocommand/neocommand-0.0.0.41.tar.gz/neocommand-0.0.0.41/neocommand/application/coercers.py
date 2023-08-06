"""
Creates and registers additional string coercers.
"""
from typing import List
from mhelper import isUnion

import stringcoercion
import mgraph

from neocommand.data import isEdgeLabel, isEntityProperty, isNodeLabel
from neocommand.endpoints import MGraphEndpoint, Endpoint


class __EndpointCoercer( stringcoercion.AbstractEnumCoercer ):
    """
    Endpoint are referenced using their names.
    """
    
    
    def on_get_archetype( self ) -> type:
        from neocommand import Endpoint
        return Endpoint
    
    
    def on_get_options( self, info: stringcoercion.CoercionInfo ) -> List[object]:
        from neocommand.data.core import get_core
        return list( x for x in get_core().endpoint_manager if isinstance( x, info.annotation.value_or_optional_value ) )
    
    
    def on_get_option_name( self, value: Endpoint ):
        if value is None:
            return "(none)"
        
        return value.name


class __LabelCoercer( stringcoercion.AbstractEnumCoercer ):
    """
    Node labels, edge labels, and property names are specified verbatim.
    """
    
    
    def on_coerce( self, info: stringcoercion.CoercionInfo ):
        try:
            super().coerce( info )
        except stringcoercion.CoercionError:
            return info.source
    
    
    def on_get_archetype( self ) -> type:
        return isUnion[isEdgeLabel, isNodeLabel, isEntityProperty]
    
    
    def on_get_options( self, info: stringcoercion.CoercionInfo ) -> List[object]:
        from neocommand.data.core import get_core
        r = []
        
        if info.annotation.is_optional:
            r.append( None )
        
        if info.annotation.value_or_optional_value is isEdgeLabel:
            r.extend( get_core().name_cache.edge_labels() )
        elif info.annotation.value_or_optional_value is isNodeLabel:
            r.extend( get_core().name_cache.node_labels() )
        elif info.annotation.value_or_optional_value is isEntityProperty:
            r.extend( get_core().name_cache.properties( info.annotation.type_label() ) )
        
        return r


class __MGraphCoercer( stringcoercion.AbstractEnumCoercer ):
    """
    **Graphs** can be denoted by specifying the name of an endpoint holding a graph or by specifying
    a string suitable for use with `mgraph.importing.import_string` (e.g. as newick or an edge list).
    """
    
    
    def on_get_archetype( self ) -> type:
        return mgraph.MGraph
    
    
    def on_get_options( self, info: stringcoercion.CoercionInfo ) -> List[object]:
        from neocommand.data.core import get_core
        from neocommand.endpoints.mgraph_endpoint import MGraphEndpoint
        return list( x for x in get_core().endpoint_manager if isinstance( x, MGraphEndpoint ) )
    
    
    def on_get_option_name( self, value: MGraphEndpoint ) -> str:
        if value is None:
            return "(none)"
        
        return value.name
    
    
    def on_convert_user_option( self, info: stringcoercion.CoercionInfo ):
        mgraph.importing.import_string( info.source )
    
    
    def on_convert_option( self, info: stringcoercion.CoercionInfo, option: MGraphEndpoint ) -> mgraph.MGraph:
        return option.read_graph()
    
    
    def on_get_accepts_user_options( self ):
        return True


def init( coercers: stringcoercion.CoercerCollection ):
    coercers.register( __EndpointCoercer(), __LabelCoercer(), __MGraphCoercer() )
