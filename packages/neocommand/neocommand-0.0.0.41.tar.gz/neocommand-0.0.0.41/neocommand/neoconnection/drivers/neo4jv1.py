import neo4j.v1
import py2neo

from neocommand.data import constants
from neocommand import NcNode, NcEdge, MemoryEndpoint, Writer, NcData
from neocommand.neoconnection.database_manager import DbManager, DbStats, IDbDriverSession


class Neo4jv1Session( IDbDriverSession ):
    """
    NEO4J DRIVER
    """
    __neo4j_v1_driver_object = None
    
    
    def __init__( self, db: DbManager ):
        cls = type( self )
        
        if cls.__neo4j_v1_driver_object is None:
            url = "bolt://" + db.remote_address + ":7687"
            auth = neo4j.v1.basic_auth( db.user_name, db.password )
            cls.__neo4j_v1_driver_object = neo4j.v1.GraphDatabase.driver( url, auth = auth )
        else:
            url = None
        
        try:
            self.driver: neo4j.v1.Session = cls.__neo4j_v1_driver_object.session()
        except Exception as ex:
            raise ConnectionError( "Failed to connect to the database using the following connection: URL = «{0}», auth = «{1}», password = «{2}». The error returned is «{3}: {4}»".format( url, db.user_name, "*****" if db.password else "[MISSING]", type( ex ).__name__, ex ) )
    
    
    def run( self, cypher: str, parameters: dict, database: DbManager, output: Writer ) -> DbStats:
        cursor = self.driver.run( cypher, parameters )
        self._convert_neo4j_entity( "", cursor, database, output )
        return DbStats( cypher, parameters, output, cursor.consume().counters.__dict__ )
    
    
    def _convert_neo4j_entity( self, var_name: str, entity: object, db_manager: DbManager, output: Writer ) -> None:
        if isinstance( entity, neo4j.v1.StatementResult ):
            self._convert_neo4j_cursor( var_name, entity, db_manager, output )
        elif isinstance( entity, neo4j.v1.Node ):
            self._convert_neo4j_node( var_name, entity, output )
        elif isinstance( entity, neo4j.v1.Relationship ):
            self.convert_neo4j_edge( var_name, entity, db_manager, output )
        elif isinstance( entity, neo4j.v1.Path ):
            self._convert_neo4j_path( var_name, entity, db_manager, output )
        else:
            output.write_data( NcData( var_name, entity ) )
    
    
    def _convert_neo4j_cursor( self, var_name: str, cursor: neo4j.v1.StatementResult, db_manager: DbManager, output: Writer ):
        if var_name:
            var_name += "/"
        
        for record in cursor:
            for name, entity in record.items():
                self._convert_neo4j_entity( var_name + name, entity, db_manager, output )
    
    
    def _convert_neo4j_path( self, var_name: str, p: py2neo.Path, db_manager: DbManager, output: Writer ) -> None:
        with output.open_folder( var_name ) as folder:
            for x in p:
                self._convert_neo4j_entity( var_name, x, db_manager, folder )
    
    
    def _convert_neo4j_node( self, var_name: str, node: neo4j.v1.Node, output: Writer ) -> None:
        """
        Converts a NcNode to a Docket.
        """
        if len( node.labels ) != 1:
            raise ValueError( "Convert node to docket expected 1 label but {0} were received: {1}".format( len( node.labels() ), ", ".join( node.labels() ) ) )
        
        uid = node[constants.PRIMARY_KEY]
        
        if not uid:
            raise ValueError( "I can't read this node because it hasn't got a «{0}» property. Please make sure all your database nodes have a unique key named «{0}».".format( constants.PRIMARY_KEY ) )
        
        label = "".join( str( x ) for x in node.labels )
        
        output.write_node( NcNode( varname = var_name, label = label, uid = uid, properties = dict( node ) ) )
    
    
    def convert_neo4j_edge( self, var_name: str, edge: neo4j.v1.Relationship, db_manager: DbManager, output: Writer ) -> None:
        start = self.lookup_node( edge.start, db_manager )
        end = self.lookup_node( edge.end, db_manager )
        edge_ = NcEdge( varname = var_name, 
                        label = edge.type, 
                        iid = edge.id, 
                        start = start,
                        end = end, 
                        properties = dict( edge ) )
        output.write_edge( edge_ )
    
    
    def lookup_node( self, iid, db_manager: DbManager ):
        mep = MemoryEndpoint( "node_lookup" )
        
        with mep.open_writer() as ep:
            db_manager.run_cypher( title = "lookup_node",
                                   cypher = self.NODE_LOOKUP_IID,
                                   parameters = { "id": iid },
                                   output = ep )
            return mep.only_child( NcNode )
    
    
    NODE_LOOKUP_IID = "MATCH (n) WHERE ID(n) = {id} RETURN n"
