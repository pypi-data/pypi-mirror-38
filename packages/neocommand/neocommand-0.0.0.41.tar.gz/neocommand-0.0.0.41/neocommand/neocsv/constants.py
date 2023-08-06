"""
Constants relating to the processing of Neo4j-compatible CSVs.
"""
from neocommand.data import constants as _core_constants


NEO4J_START_ID_TYPE         = "START_ID"
NEO4J_END_ID_TYPE           = "END_ID"
NEO4J_ID_TYPE               = "ID"
NEO4J_START_ID_SUFFIX       = ":" + NEO4J_START_ID_TYPE
NEO4J_END_ID_SUFFIX         = ":" + NEO4J_END_ID_TYPE
NEO4J_ID_SUFFIX             = ":" + NEO4J_ID_TYPE
PRIMARY_KEY_DECORATED_NAME  = _core_constants.PRIMARY_KEY + NEO4J_ID_SUFFIX
PREFIX_UNIX                 = "file:///"
PREFIX_WINDOWS              = "file:/"
EXT_B42ZIP = ".parcel_zip"
EXT_CYPHER = ".cypher"
EXT_SH     = ".sh"