#!/usr/bin/env python

# Count the number of in and out edges for each node
# Output: node list with in and out values

import sys
import json

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: collect-cg-in-out.py nodes_filename cg_filename")

    with open(sys.argv[1]) as nodes_fp:
        nodes_data = json.load(nodes_fp)

    with open(sys.argv[2]) as json_fp:
        json_data = json.load(json_fp)

    node_id_map = {}
    node_pos_map = {}
    for node in json_data["nodes"]:
        pos = node["pos"]
        obj = {"label": node["label"],
               "pos": pos,
               "in": 0,
               "out": 0}

        node_id_map[node["id"]] = obj
        node_pos_map[pos] = obj

    for link in json_data["links"]:
        node_id_map[link["target"]]["in"] += 1
        node_id_map[link["source"]]["out"] += 1

    sys.stdout.write("[")
    comma = False

    for node_id, node in enumerate(nodes_data):
        if node_id != node["id"]:
            raise Exception("wrong node:id")

        if comma:
            sys.stdout.write(",")
        comma = True

        node_in = 0
        node_out = 0

        node_data = node_pos_map.get(node["pos"], None)
        if node_data:
            node_in = node_data["in"]
            node_out = node_data["out"]

        sys.stdout.write("\n  { \"id\": %d, \"label\": %s, \"pos\": %s, \"in\": %d, \"out\": %d }" %
            (node_id, json.dumps(node["label"]), json.dumps(node["pos"]), node_in, node_out))

    sys.stdout.write("\n]\n")
