import intermake


def init( app: intermake.Application ):
    app.help.add( 
             "Needs resolve",
             """
             When transferring data from one endpoint to another (i.e. `source` --> `destination`) sometimes the origin may not contain all of the information you want to place in the endpoint. Consider the following Cypher query:
             
             ```cypher
             MATCH (:Sequence)-[r:Like]->(:Sequence) RETURN r LIMIT 1
             ```
             
             Unfortunately, the relationship is returned from Neo4j _without_ the node data, hence `destination` receives a relationship but is unable to specify the nodes that relationship is connected to.
             
             To fix this issue consider the following:
             
             * **Use the `PY2NEO` driver on your `source`** - When constructing your database, specify the PY2NEO driver. This driver does a better job of returning pertinent data.
             * **Specify a resolver on your `destination`** - The resolver argument specifies a database that can be queried, during the transfer, in order to fill out the missing information.
                 * The resolver takes a three arguments:
                     * `resolver` specifies the database used to resolve missing entries. The default `None` is the primary database. If you have multiple database connections then you should specify a database explicitly. You can use `null` endpoint to suppress automated resolution.
                     * `no_cache` disables the resolver cache. Resolved entities are retained in memory. The cache is enabled by default - disable it if you are expecting very large output where caching entries may lead to an out of memory error.
                     * `no_enforce` prevents raising an error if resolving fails. Errors are enabled by default - if you don't wish to resolve entities and don't care about missing data, disable this option.
             """ )
    
    app.help.add(
            "Node and class definition",
            """
            In Neo4j nodes do not have a "primary key".
            NeoCommand however mandates that all nodes do have a primary key, and that the primary key is named "uid" and is of type "string".
            """ )