"""
Functions for importing data into an MGraph.

These functions:
* take the data to be imported as the first argument
* specify further import parameters as keyword arguments.
* have a `graph` parameter, allowing data to be imported into an existing graph.
* return the created graph (same as the `graph` parameter if provided).
"""
from typing import Iterable, Dict
from mhelper import Logger, array_helper, ByRef, io_helper, file_helper

import re
import os.path

from mgraph import analysing
from mgraph.graphing import MGraph, MNode, MEdge, DConverter, MSplit


__LOG_MAKE = Logger( "import_splits", False )


def import_binary( file_name: str, *, graph: MGraph = None ) -> MGraph:
    """
    Imports a binary file.
    
    :param file_name:   File to import 
    :param graph:       Graph to copy into 
    :return:            Resulting graph 
    """
    g: MGraph = io_helper.load_binary( file_name )
    
    if graph is None:
        return g
    else:
        g.copy( target = graph )
        return graph


def import_splits( splits: Iterable[MSplit], *, graph: MGraph = None ) -> MGraph:
    """
    Creates a graph from a set of splits.
    :param graph:       Target graph.
    :param splits:  Iterable over splits 
    :return:        Constructed graph. 
    """
    if graph is None:
        graph = MGraph()
    
    # Nb. treemodel.Tree.from_split_bitmasks just skips dud splits, not sure we should do that here
    
    to_use = sorted( splits, key = lambda x: str( x ) )
    to_use = sorted( to_use, key = lambda x: len( x ) )
    root: MNode = graph.add_node( data = "root" )
    
    for i, split in enumerate( to_use ):
        split_str = str( split )
        
        if len( split ) == 1:
            __LOG_MAKE( "DEFINING SPLIT {} OF {} = {}", i, len( to_use ), split_str )
            sequence = array_helper.single_or_error( split.inside )
            
            if not any( x.data is sequence for x in graph.nodes ):
                root.add_child( data = sequence )
            
            continue
        
        # Find the most recent common ancestor of all sequences in our split
        paths = analysing.find_common_ancestor_paths( graph, query = lambda x: x.data in split.inside )
        mrca: MNode = paths[0][0]
        # __LOGUS( "MRCA = {}".format( mrca ) )
        
        # Some nodes will be attached by the same clade, reduce this to the final set
        destinations = set( path[1] for path in paths )
        
        if len( destinations ) == len( mrca.edges.outgoing_dict ):
            # Already a self-contained clade, nothing to do
            __LOG_MAKE( "EXISTING SPLIT {} OF {} = {} (@{})", i, len( to_use ), split_str, mrca )
            continue
        
        __LOG_MAKE( "NEW      SPLIT {} OF {} = {} (@{})", i, len( to_use ), split_str, mrca )
        
        new_node = mrca.add_child()
        # new_node.data = "split: " + split_str
        # __LOGUS( "NEW CHILD = {}".format( new_node ) )
        
        for destination in destinations:
            # __LOGUS( "MRCA DESTINATION #n = {}", destination )
            mrca.remove_edge_to( destination )
            new_node.add_edge_to( destination )
        
        __LOG_MAKE( graph.to_ascii() )
        
        __LOG_MAKE.pause()
        
        # __LOGUS( "========================================" )
    
    # __LOGUS( "FINAL STATUS" )
    # __LOGUS( g.to_ascii() )
    return graph


def import_compact( text: str, *, graph: MGraph = None ):
    """
    Imports a string created with `to_compact`.
    """
    return import_edgelist( text, delimiter = ",", line_break = "|", graph = graph )


def import_edgelist( text: str, *, delimiter: str = ",", line_break: str = "\n", strip: bool = True, graph: MGraph = None ) -> MGraph:
    """
    Imports an edgelist.
    
    :param graph:           Graph to import into.
    :param text:            Edgelist 
    :param delimiter:       Node delimiter 
    :param line_break:      Line (edge) delimiter
    :param strip:           Strips spaces 
    """
    if graph is None:
        graph = MGraph()
    
    mapping: Dict[object, MNode] = { }
    
    for line in text.split( line_break ):
        if not line:
            continue
        
        if not delimiter in line:
            raise ValueError( "Cannot import the edgelist because the data is not in the correct format. The delimiter «{}» does not exist in the line «{}».".format( delimiter, line ) )
        
        left_text, right_text = line.split( delimiter, 1 )
        if strip:
            left_text = left_text.strip()
            right_text = right_text.strip()
        
        left_node = mapping.get( left_text )
        right_node = mapping.get( right_text )
        
        if left_node is None:
            left_node = MNode( graph, left_text )
            mapping[left_text] = left_node
        
        if right_node is None:
            right_node = MNode( graph, right_text )
            mapping[right_text] = right_node
        
        MEdge( left_node, right_node )
    
    return graph


def import_newick( newick_tree: str = "",
                   *,
                   file_name: str = "",
                   root_name: str = "root",
                   converter: DConverter = str,
                   edge_converter: DConverter = float,
                   clade_name: str = "clade",
                   root_ref: ByRef["MNode"] = None,
                   graph: MGraph = None
                   ) -> MGraph:
    """
    Imports a single newick tree or multiple ";" delimited trees.
    Node data is set to the newick node labels (str), a `converter` argument may be specified to convert them.
    Edge data is set to the newick edge lengths, as a `float`. an `edge_converter` argument may be specified to override this behaviour.
    Requires library: `ete`.
    
    :param file_name:       May be used to load the `newick_tree` from a file.
    :param edge_converter:  How to assign edge data
    :param graph:           Target graph.
    :param newick_tree:     Newick format tree (ETE format #1)
    :param root_name:       Name of the root
    :param converter:       How to assign node data
    :param clade_name:      Name of clades
    :param root_ref:        Receiver for the root node (if none the reference is not set)
    :returns: All imported nodes
    """
    if file_name:
        if newick_tree:
            raise ValueError( "Cannot specify both the `newick_tree` and `file_name` arguments." )
        
        newick_tree = file_helper.read_all_text( file_name )
    
    if graph is None:
        graph = MGraph()
    
    newick_tree = newick_tree.strip()
    
    if newick_tree.endswith( ";" ):
        newick_tree = newick_tree[:-1]
    
    if ";" in newick_tree:
        for x in newick_tree.split( ";" ):
            import_newick( x, root_name = root_name, converter = converter, clade_name = clade_name, graph = graph )
        
        return graph
    
    if not newick_tree:
        return graph
    
    all = []
    last = graph.add_node( data = root_name )
    all.append( last )
    stack = [last]
    elements = re.split( "([:,()])", newick_tree )
    clade = 0
    next_is_length = False
    
    if elements[0] == "":
        del elements[0]
    
    if elements[-1] == "":
        del elements[-1]
    
    last_close = False
    
    for element in elements:
        if next_is_length:
            next_is_length = False
            if len( last.edges.incoming_dict ) != 1:
                # Edges on the root don't make sense
                # (these might be specified by some applications, they should be 0 in these cases)
                continue
            
            last_edge = array_helper.single_or_error( last.edges.incoming )
            last_edge.data = edge_converter( element )
            continue
        
        if element == "":
            if last_close:
                continue
            
            clade += 1
            element = clade_name + str( clade )
        
        new_last_close = False
        
        if element == "(":
            stack.append( last )
        elif element == ")":
            last = stack.pop()
            new_last_close = True
        elif element == ",":
            pass
        elif element == ":":
            next_is_length = True
        else:
            if last_close:
                last.data = converter( element )
            else:
                last = stack[-1].add_child( data = converter( element ) )
                all.append( last )
        
        last_close = new_last_close
    
    if root_ref is not None:
        root_ref.value = all[0]
    
    return graph


def import_ete( ete_tree: object, *, graph: MGraph = None ):
    """
    Imports an Ete tree
    Node data is set to the ete node names.
    Requires library: `ete`.
    
    :param graph:        Target graph
    :param ete_tree:    Ete tree 
    :returns: Tree root
    """
    if graph is None:
        graph = MGraph()
    
    from ete3 import TreeNode
    assert isinstance( ete_tree, TreeNode )
    
    # Zoom to the root
    while ete_tree.up is not None:
        ete_tree = ete_tree.up
    
    root = MNode( graph, ete_tree.name )
    
    
    def ___recurse( m_node, ete_node, depth ) -> None:
        for ete_child in ete_node.get_children():
            m_node_next = MNode( graph, ete_child.name )
            
            MEdge( m_node, m_node_next )
            
            ___recurse( m_node_next, ete_child, depth + 1 )
    
    
    ___recurse( root, ete_tree, 0 )
    
    return graph


def import_string( text: str ) -> MGraph:
    """
    Imports arbitrary text, which may be a file name or raw data.
    
        [prefix: ][filename.extension|data]
        
    * A file is assumed, if such a file exists on disk.
    * An optional prefix explicitly specifies the data format.
    * If no prefix is specified:
        * If a filename is specified, and the filename contains an extension, the extension is used
        * Otherwise the characters listed below are used to determine the data format.
    
    ================ ============== ============= =========
    What             Internal       Characters    Extension
    ================ ============== ============= =========
    Compact edgelist str            |             .compact
    TSV              str            newline, tab  .tsv
    CSV              str            newline       .csv
    Newick           str            (none above)  .nwk
    ================ ============== ============= =========
    """
    prefixes = "newick", "compact", "csv", "tsv", "file", "file-newick", "file-compact", "file-csv", "file-tsv"
    prefix, filename = text.split( ":", 1 )
    is_file = None
    
    for prefix_ in prefixes:
        if text.startswith( prefix_ + ":" ):
            prefix = prefix_
            text = text[len( prefix_ ) + 1:]
            
            if prefix == "file":
                is_file = True
                prefix = None
            elif prefix.startswith( "file-" ):
                is_file = True
                prefix = prefix[5:]
            
            break
    
    if is_file is True or (is_file is None and os.path.isfile( text )):
        if prefix is None:
            ext = file_helper.get_extension( text )
            if ext in (".nwk", ".new", ".newick"):
                prefix = "newick"
            elif ext == ".tsv":
                prefix = "tsv"
            elif ext in (".edg", ".compact"):
                prefix = "compact"
            elif ext == ".csv":
                prefix = "csv"
        
        text = file_helper.read_all_text( text )
    
    if prefix == "compact" or (prefix is None and "|" in text):
        r = import_compact( text )
    elif prefix in ("csv", "tsv") or (prefix is None and "\n" in text):
        if prefix == "tsv" or (prefix is None and "\t" in text):
            r = import_edgelist( text, delimiter = "\t" )
        else:
            assert prefix is None or prefix == "csv"
            r = import_edgelist( text )
    else:
        assert prefix is None or prefix == "newick"
        r = import_newick( text )
    
    return r
