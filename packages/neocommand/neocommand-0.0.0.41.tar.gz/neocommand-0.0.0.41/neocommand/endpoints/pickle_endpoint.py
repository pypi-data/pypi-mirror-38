from os import path
from typing import List, Optional, Dict

from mhelper import isFilename, io_helper, override
from neocommand.endpoints.abstract_endpoints import AbstractListBackedEndpoint


class PickleEndpoint( AbstractListBackedEndpoint ):
    """
    An endpoint, as a disk pickle.
    """
    # noinspection SpellCheckingInspection
    _EXT_ENDPOINT_PICKLE = ".eppickle"
    
    
    def __init__( self, name: str, file_name: isFilename[_EXT_ENDPOINT_PICKLE] ):
        super().__init__( name )
        self.__file_name = file_name
        self.__contents = None
    
    
    def __str__( self ):
        return "File: {}".format( self.__file_name )
    
    
    @property
    def contents( self ) -> List[Optional[object]]:
        if self.__contents is None:
            if path.isfile( self.__file_name ):
                try:
                    self.__contents = io_helper.load_binary( self.__file_name, type_ = list )
                    assert isinstance( self.__contents, list )
                except Exception as ex:
                    raise ValueError( "Failed to recover the PickleEndpoint disk-list from «{0}». The internal error is «{1}: {2}». If this is causing problems, you may have to delete the endpoint and recreate it.".format( self.__file_name, type( ex ).__name__, ex ) )
            else:
                self.__contents = []
        
        return self.__contents
    
    
    def on_flush( self ) -> None:
        io_helper.save_binary( self.__file_name, self.__contents )
    
    
    @override
    def __getstate__( self ) -> Dict[str, object]:
        return { "name"     : self.name,
                 "file_name": self.__file_name }
    
    
    @override
    def __setstate__( self, state: Dict[str, object] ) -> None:
        self.name = state["name"]
        self.__file_name = state["name"]
        self.__contents = None
