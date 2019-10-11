#!/usr/bin/env python

# Change node ids and update call graph with the new ids
# The new node id list is usually the ouput of collect-nodes.py
# Output: rebased call graph

import sys
import json

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: callgraph-rebase.py nodes_filename callchain_filename")

    with open(sys.argv[1]) as nodes_fp:
        nodes_data = json.load(nodes_fp)

    with open(sys.argv[2]) as json_fp:
        json_data = json.load(json_fp)

    nodes = {}
    entry_found = False

    for node in nodes_data:
        node_id = node["id"]

        if node_id == 0:
            if not "entry" in node or not node["entry"]:
                raise Exception("Node with id:0 must be an entry node (node list)")
            if entry_found:
                raise Exception("Node with id:0 was found before (node list)")
            entry_found = True
            continue

        if "entry" in node and node["entry"]:
            raise Exception("Only node with id:0 can be an entry node (node list)")

        pos = node["pos"]

        if pos in nodes:
            raise Exception("Duplicated position info (node list): %s" % (pos))

        nodes[pos] = node_id

    if not entry_found:
        raise Exception("Entry node (id:0) not found (node list)")

    callgraph_nodes = set()
    id_map = { 0:0 }
    entry_found = False

    for node in json_data["nodes"]:
        node_id = node["id"]

        if node_id == 0:
            if not "entry" in node or not node["entry"]:
                raise Exception("Node with id:0 must be an entry node (callgraph)")
            if entry_found:
                raise Exception("Node with id:0 was found before (callgraph)")
            entry_found = True
            continue

        if "entry" in node and node["entry"]:
            raise Exception("Only node with id:0 can be an entry node (node list)")

        pos = node["pos"]
        if pos in callgraph_nodes:
            raise Exception("Duplicated position info(callgraph): %s" % (pos))

        callgraph_nodes.add(pos)

        if pos in nodes:
            id_map[node_id] = nodes[pos]
        else:
            sys.stderr.write("Remove node %d label: \"%s\" pos: %s\n" % (node_id, node["label"], pos))

    if not entry_found:
        raise Exception("Entry node (id:0) not found (callgraph)")

    # free memory
    nodes = None
    callgraph_nodes = None

    sys.stdout.write("{\n\"directed\": true,\n\"multigraph\": false,\n\"nodes\": [\n")
    sys.stdout.write("  { \"id\": 0, \"label\": \"<entry>\", \"pos\": \"<entry>\", \"entry\": true }")

    for node in nodes_data:
        node_id = node["id"]

        if node_id == 0:
            continue

        sys.stdout.write(",\n  { \"id\": %d, \"label\": %s, \"pos\": %s }"
                         % (node_id, json.dumps(node["label"]), json.dumps(node["pos"])))

    sys.stdout.write("\n],\n\"links\": [")

    comma = False
    for link in json_data["links"]:
        source = id_map.get(link["source"], None)
        target = id_map.get(link["target"], None)

        if source != None and target != None:
            if comma:
                sys.stdout.write(",")
            comma = True

            sys.stdout.write("\n  { \"source\": %d, \"target\": %d }" % (source, target))

    sys.stdout.write("\n]\n}\n")
