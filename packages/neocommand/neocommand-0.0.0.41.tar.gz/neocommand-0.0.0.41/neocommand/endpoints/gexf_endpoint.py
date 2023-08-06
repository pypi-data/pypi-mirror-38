from string import Template
from typing import Union, List

from intermake.engine import Controller
from mhelper import TTristate
from neocommand.data import NcEdge, NcNode
from neocommand.endpoints.abstract_endpoints import AbstractFileDestination, Destination
from neocommand.helpers.resolver import EdgeNodeDict


class GexfEndpoint( Destination ):
    def __init__( self, name, file_name, overwrite ):
        super().__init__( name )
        self.file_name = file_name
        self.overwrite: TTristate = overwrite
    
    def __str__( self ):
        return "GEXF: {}".format( self.file_name )
    
    def on_open_writer( self ):
        return _GexfEndpointWriter( self.file_name, self.overwrite )


# noinspection SpellCheckingInspection
class _GexfEndpointWriter( AbstractFileDestination ):
    def on_get_file_type( self ):
        return "GEXF"
    
    
    def __str__( self ):
        return "GEXF: {}".format( self.file_name )
    
    
    def on_create_content( self, data: EdgeNodeDict ) -> None:
        TEMPLATE = Template(
                """
                <gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
                    <meta lastmodifieddate="2017-04-20">
                        <creator>${app_name}</creator>
                        <description>This file was exported by ${app_name}'s GephiExport plugin</description>
                    </meta>
                    <graph mode="static" defaultedgetype="directed">
                        <attributes class="node">
                            ${node_attributes}
                        </attributes>
                        <attributes class="edge">
                            ${edge_attributes}
                        </attributes>
                        <nodes>
                            ${nodes}
                        </nodes>
                        <edges>
                            ${edges}
                        </edges>
                    </graph>
                </gexf>
                """ )
        
        node_xml = []
        edge_xml = []
        node_attrs = { }
        node_attr_xml = []
        edge_attrs = { }
        edge_attr_xml = []
        
        for node, node_id in data.nodes_and_ids:
            node_xml.append( '                <node id="{0}" label="{1}">'.format( node_id, node.label ) )
            self.__write_attributes( node, node_attr_xml, node_attrs, node_xml )
            node_xml.append( '                </node>' )
        
        for edge, edge_id, start_id, end_id in data.edges_and_ids:
            edge_xml.append( '                <edge id="{0}" label="{1}" source="{2}" target="{3}">'.format( edge_id, edge.label, start_id, end_id ) )
            self.__write_attributes( edge, edge_attr_xml, edge_attrs, edge_xml )
            edge_xml.append( '                </edge>' )
        
        return TEMPLATE.substitute( app_name = Controller.ACTIVE.app.name,
                                    node_attributes = "\n".join( node_attr_xml ),
                                    edge_attributes = "\n".join( edge_attr_xml ),
                                    nodes = "\n".join( node_xml ),
                                    edges = "\n".join( edge_xml ) )
    
    
    @staticmethod
    def __write_attributes( entity: Union[NcEdge, NcNode], attr_xml: List[str], attrs, xml: List[str] ):
        xml.append( '                    <attvalues>' )
        for k, v in entity.properties.items():
            if k not in attrs:
                aid = len( attrs )
                attrs[k] = aid
                attr_xml.append( '                <attribute id="{0}" title="{1}" type="string"/>'.format( aid, k ) )
            else:
                aid = attrs[k]
            
            vstr = str( v )
            vstr = vstr.replace( "<", "&apos;&lt;&apos;" ).replace( ">", "&apos;&gt;&apos;" )  # causes Gephi error
            xml.append( '                        <attvalue for="{0}" value="{1}"/>'.format( aid, vstr ) )
        xml.append( '                    </attvalues>' )
