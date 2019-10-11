#!/usr/bin/env python

import sys
import json

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: collect-stats.py filename [node-list]")

    with open(sys.argv[1]) as json_fp:
        json_data = json.load(json_fp)

    sys.stdout.write("Number of nodes: %d\n" % (len(json_data["nodes"])))

    if "call_chains" in json_data:
        sys.stdout.write("Number of call chains: %d\n" % (len(json_data["call_chains"])))

    if "links" in json_data:
        sys.stdout.write("Number of call graph links: %d\n" % (len(json_data["links"])))

    if len(sys.argv) > 2:
        id_map = {}
        for node in json_data["nodes"]:
            id_map[node["id"]] = "label: '%s': file: '%s'" % (node["label"], node["pos"])

        node_list = json.loads(sys.argv[2])
        for idx, value in enumerate(node_list):
            info = id_map.get(value)
            if info == None:
                sys.stdout.write("%3d - id:%d not found\n" % (idx, value))
            else:
                sys.stdout.write("%3d - id:%d %s\n" % (idx, value, info))

