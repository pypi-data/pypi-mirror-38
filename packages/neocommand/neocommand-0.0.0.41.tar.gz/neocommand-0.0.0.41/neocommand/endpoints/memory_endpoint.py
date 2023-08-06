from typing import List, Optional, Iterator

from neocommand.data import NcEdge, NcNode, NcData
from neocommand.endpoints.abstract_endpoints import AbstractListBackedEndpoint


class MemoryEndpoint( AbstractListBackedEndpoint ):
    """
    An endpoint, in local system memory.
    
    Can be pickled to disk (meaning it can form part of other endpoints - if the user creates one it will not be!).
    """
    
    
    def on_flush( self ) -> None:
        pass
    
    
    def __str__( self ) -> str:
        return "Memory: n={}".format( len( self.__contents ) )
    
    
    def __init__( self, name: Optional[str] = None ) -> None:
        super().__init__( name )
        self.__contents = _SafeList()
    
    
    @property
    def contents( self ) -> List[Optional[object]]:
        return self.__contents
    
    
    def __iter__( self ):
        return iter( self.__contents )
    
    
    def recurse( self ) -> Iterator[object]:
        """
        Recurses over the entities of the endpoint, and any sub-endpoints
        """
        for x in self.contents:
            if isinstance( x, MemoryEndpoint ):
                yield from x.recurse()
            else:
                yield x


class _SafeList( list ):
    SAFE_TYPES = (int, str, float, bool, list, tuple, NcNode, NcEdge, NcData, MemoryEndpoint)
    
    
    def append( self, item: object ) -> None:
        if not type( item ) in self.SAFE_TYPES:
            raise ValueError( "Attempt to add an item «{}» of type «{}» to a SafeList, but the SafeList doesn't expect such items.".format( item, type( item ) ) )
        
        super().append( item )
