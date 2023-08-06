"""
This subpackage contains wrappers for two popular Neo4j drivers.

The only export is the function, `init`, which registers the drivers with the
database manager. Nothing else is exported.

The driver wrappers are only loaded when they are used, so this package will
function even if the user does not have the specific drivers installed.
"""


def init():
    def __driver_1( m ):
        from .neo4jv1 import Neo4jv1Session
        return Neo4jv1Session( m )
    
    
    def __driver_2( m ):
        from .py2neo import Py2neoSession
        return Py2neoSession( m )
    
    
    from neocommand.neoconnection.database_manager import DbManager
    DbManager.DRIVER_CLASSES["neo4jv1"] = __driver_1
    DbManager.DRIVER_CLASSES["py2neo"] = __driver_2
