from mhelper import MAnnotation


class MAnnotationWithLabel( MAnnotation ):
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )


isNodeUid = MAnnotationWithLabel( "isNodeUid", str )
isEntityProperty = MAnnotationWithLabel( "isEntityProperty", str )
isNodeProperty = MAnnotationWithLabel( "isNodeProperty", str )
isEdgeProperty = MAnnotationWithLabel( "isEdgeProperty", str )
isEntityLabel = MAnnotation( "isEntityLabel", str )
isNodeLabel = MAnnotation( "isNodeLabel", str )
isEdgeLabel = MAnnotation( "isEdgeLabel", str )
isEndpointName = MAnnotation( "isEndpointName", str )
isDriverName = MAnnotation( "isDriverName", str )
