"""
This subpackage contains abstract "endpoint" base classes, representing data sources and destinations,
as well as a selection of concrete endpoints, such as endpoints for the database and Gephi.

`Endpoint`s themselves subclass `Destination` and/or `Origin`.
These are factory classes, returning a `Reader` or a `Writer` when it's time for business.

                                 Endpoint
                          Origin          Destination                                
             .open_writer                             .open_reader                   
  Reader <--                                                        --> Writer       
     
 
"""
from .abstract_endpoints import Destination, Endpoint, Origin, Reader, Writer
from .visjs_endpoint import VisJsEndpoint
from .edgecsv_endpoint import EdgeCsvEndpoint
from .gexf_endpoint import GexfEndpoint
from .csvfolder_endpoint import CsvFolderEndpoint
from .memory_endpoint import MemoryEndpoint
from .counting_endpoint_wrapper import CounterWriter
from .pickle_endpoint import PickleEndpoint
from .db_endpoint import DatabaseEndpoint
from .null_endpoint import NULL_ENDPOINT
from .echoing_endpoint import ECHOING_ENDPOINT
from .mgraph_endpoint import MGraphEndpoint
