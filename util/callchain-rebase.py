#!/usr/bin/env python

# Change node ids and update call chains with the new ids
# The new node id list is usually the ouput of collect-nodes.py
# Output: rebased call chain

import sys
import json

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: callchain-rebase.py [-i] nodes_filename callchain_filename")

    args_idx = 1
    if sys.argv[1] == "-i":
        args_idx = 2

    with open(sys.argv[args_idx]) as nodes_fp:
        nodes_data = json.load(nodes_fp)

    with open(sys.argv[args_idx + 1]) as json_fp:
        json_data = json.load(json_fp)

    out_file = sys.stdout
    if args_idx == 2:
        out_file = open(sys.argv[3], "w")

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

        if node_id < 0:
            raise Exception("Negative node id (%d) is not allowed" % (node_id))

        pos = node["pos"]

        if pos in nodes:
            raise Exception("Duplicated position info (node list): %s" % (pos))

        nodes[pos] = node_id

    if not entry_found:
        raise Exception("Entry node (id:0) not found (node list)")

    callchain_nodes = set()
    id_map = { 0:0, -1:-1 }
    entry_found = False

    for node in json_data["nodes"]:
        node_id = node["id"]

        if node_id == 0:
            if not "entry" in node or not node["entry"]:
                raise Exception("Node with id:0 must be an entry node (callchain)")
            if entry_found:
                raise Exception("Node with id:0 was found before (callchain)")
            entry_found = True
            continue

        if "entry" in node and node["entry"]:
            raise Exception("Only node with id:0 can be an entry node (node list)")

        if node_id < 0:
            raise Exception("Negative node id (%d) is not allowed" % (node_id))

        pos = node["pos"]
        if pos in callchain_nodes:
            raise Exception("Duplicated position info (callchain): %s" % (pos))

        callchain_nodes.add(pos)

        if pos in nodes:
            id_map[node_id] = nodes[pos]
        else:
            sys.stderr.write("Remove node %d label: \"%s\" pos: %s\n" % (node_id, node["label"], pos))

    if not entry_found:
        raise Exception("Entry node (id:0) not found (callchain)")

    # free memory
    nodes = None
    callchain_nodes = None

    out_file.write("{\n\"directed\": true,\n\"multigraph\": false,\n\"nodes\": [\n")
    out_file.write("  { \"id\": 0, \"label\": \"<entry>\", \"pos\": \"<entry>\", \"entry\": true }")

    for node in nodes_data:
        node_id = node["id"]

        if node_id == 0:
            continue

        out_file.write(",\n  { \"id\": %d, \"label\": %s, \"pos\": %s }"
                       % (node_id, json.dumps(node["label"]), json.dumps(node["pos"])))

    out_file.write("\n],\n\"call_chains\": [")

    comma = False
    for call_chain in json_data["call_chains"]:
        if len(call_chain) == 0:
            raise Exception("Empty call chain is not allowed")

        for i, item in enumerate(call_chain):
            if i == 0 and item != 0:
                raise Exception("The first item of a call chain must have id:0")
            if i != 0 and item == 0:
                raise Exception("Only the first item of a call chain can have id:0")

        if comma:
            out_file.write(",")
        comma = True

        # Removal is not allowed!
        new_call_chain = tuple(id_map[idx] for idx in call_chain)
        out_file.write("\n  %s" % (json.dumps(new_call_chain)))

    out_file.write("\n]\n}\n")
    if args_idx == 2:
        out_file.close()
