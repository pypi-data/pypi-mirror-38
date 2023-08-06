"""
This module just exposes the `mgraph` functions to a GUI/CLI user.
"""

import intermake

import mgraph.exporting as exp
import mgraph.importing as imp

from neocommand.application import app


__vis = intermake.Visibility( name = "mgraph",
                       comment = "The `mgraph` functions for graph import/export, for use through the CLI.",
                       is_visible = False )

__register = app.command( visibility = __vis, folder = "MGraph" )

export_ancestry = __register( command = exp.export_ancestry, names = ["mg_export_ancestry", "export_ancestry"] )
export_ascii = __register( command = exp.export_ascii, names = ["mg_export_ascii", "export_ascii"] )
export_binary = __register( command = exp.export_binary, names = ["mg_export_binary", "export_binary"] )
export_compact = __register( command = exp.export_compact, names = ["mg_export_compact", "export_compact"] )
export_cytoscape_js = __register( command = exp.export_cytoscape_js, names = ["mg_export_cytoscape_js", "export_cytoscape_js"] )
export_edgelist = __register( command = exp.export_edgelist, names = ["mg_export_edgelist", "export_edgelist"] )
export_ete = __register( command = exp.export_ete, names = ["mg_export_ete", "export_ete"] )
export_newick = __register( command = exp.export_newick, names = ["mg_export_newick", "export_newick"] )
export_nodelist = __register( command = exp.export_nodelist, names = ["mg_export_nodelist", "export_nodelist"] )
export_splits = __register( command = exp.export_splits, names = ["mg_export_splits", "export_splits"] )
export_string = __register( command = exp.export_string, names = ["mg_export_string", "export_string"] )
export_svg = __register( command = exp.export_svg, names = ["mg_export_svg", "export_svg"] )
export_js = __register( command = exp.export_js, names = ["mg_export_js", "export_js"] )
export_vis_js = __register( command = exp.export_vis_js, names = ["mg_export_vis_js", "export_vis_js"] )
import_binary = __register( command = imp.import_binary, names = ["mg_import_binary", "import_binary"] )
import_compact = __register( command = imp.import_compact, names = ["mg_import_compact", "import_compact"] )
import_edgelist = __register( command = imp.import_edgelist, names = ["mg_import_edgelist", "import_edgelist"] )
import_ete = __register( command = imp.import_ete, names = ["mg_import_ete", "import_ete"] )
import_newick = __register( command = imp.import_newick, names = ["mg_import_newick", "import_newick"] )
import_splits = __register( command = imp.import_splits, names = ["mg_import_splits", "import_splits"] )
