"""
This subpackage contains the basic classes for dealing with a graph database - (nodes, edges, etc.),
as well as classes for managing the user's data within Neocommand (schema, endpoint list, etc.) 
It also contains constants and several objects that can be used as PEP484 function annotations. 
"""

from .annotations import isNodeUid, isEntityProperty, isNodeProperty, isEdgeProperty, isEntityLabel, isNodeLabel, isEdgeLabel, isEndpointName, isDriverName

from .entities import NcNode, NcEdge, NcEntity, NcData

from .script import isDbParam, isScriptParam, ScriptCommand

from .constants import PRIMARY_KEY

from .core import get_core
