#!/usr/bin/env python

# Merge multiple call graphs into a single call graph
# New "ids" assigned to each unique node
# Call links are updated and only unique call links kept
# Output: merged call graph

import sys
import json

global_pos_map = {}
global_next_id = 1
global_links = set()

def process_file(filename):
    global global_next_id

    with open(filename) as json_fp:
        json_data = json.load(json_fp)

    id_map = { 0:0, -1:-1 }

    for node in json_data["nodes"]:
        pos = node["pos"]
        map_id = node["id"]

        if map_id == 0:
            continue

        if map_id < 0:
            raise Exception("Negative node id (%d) is not allowed" % (map_id))

        if pos[0:8] == "<unknown" or pos[0:5] == "*eval":
            node_id = global_next_id
            global_next_id += 1
        else:
            node_id = global_pos_map.get(pos, None)
            if node_id != None:
                id_map[map_id] = node_id
                continue

            global_pos_map[pos] = global_next_id
            node_id = global_next_id
            global_next_id += 1

        id_map[map_id] = node_id

        sys.stdout.write(",\n  { \"id\": %d, \"label\": %s, \"pos\": %s }"
                         % (node_id, json.dumps(node["label"]), json.dumps(pos)))

    for link in json_data["links"]:
        global_links.add((id_map[link["source"]], id_map[link["target"]]))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: callgraph-merge.py -l filename or filenames")

    sys.stdout.write("{\n\"directed\": true,\n\"multigraph\": false,\n\"nodes\": [\n")
    sys.stdout.write("  { \"id\": 0, \"label\": \"<entry>\", \"pos\": \"<entry>\", \"entry\": true }")

    if sys.argv[1] == "-l":
        with open(sys.argv[2]) as fp:
            for filename in fp:
                process_file(filename.strip())
    else:
        for i in range(1, len(sys.argv)):
            process_file(sys.argv[i])

    sys.stdout.write("\n],\n\"links\": [")

    comma = False

    for link in global_links:
        if comma:
            sys.stdout.write(",")
        comma = True

        sys.stdout.write("\n  { \"source\": %d, \"target\": %d }" % (link[0], link[1]))

    sys.stdout.write("\n]\n}\n")
