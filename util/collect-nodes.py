#!/usr/bin/env python

import sys
import json

global_nodes_map = set()
global_next_id = 1

def process_file(filename):
    global global_next_id

    with open(filename) as json_fp:
        json_data = json.load(json_fp)

    entry_found = False
    for node in json_data["nodes"]:
        node_id = node["id"]

        if node_id == 0:
            if not "entry" in node or not node["entry"]:
                raise Exception("Node with id:0 must be an entry node")
            if entry_found:
                raise Exception("Node with id:0 was found before")
            entry_found = True
            continue

        if "entry" in node and node["entry"]:
            raise Exception("Only node with id:0 can be an entry node")

        if node_id < 0:
            raise Exception("Negative node id (%d) is not allowed" % (node_id))

        pos = node["pos"]

        # exclude functions coming from evals
        if pos[0:8] != "<unknown" and not pos in global_nodes_map:
            global_nodes_map.add(pos)

            sys.stdout.write(",\n  { \"id\": %d, \"label\": %s, \"pos\": %s }" % 
                             (global_next_id, json.dumps(node["label"]), json.dumps(pos)))

            global_next_id += 1

    if not entry_found:
        raise Exception("Entry node (id:0) not found")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: collect-nodes.py filename[s] or -l filename")

    sys.stdout.write("[\n")
    sys.stdout.write("  { \"id\": 0, \"label\": \"<entry>\", \"pos\": \"<entry>\", \"entry\": true }")

    if len(sys.argv) >= 3 and sys.argv[1] == "-l":
        with open(sys.argv[2]) as fp:
            for filename in fp:
                process_file(filename.strip())
    else:
        for i in range(1, len(sys.argv)):
            process_file(sys.argv[i])

    sys.stdout.write("\n]\n")
