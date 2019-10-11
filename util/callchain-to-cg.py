#!/usr/bin/env python

# Convert a call chain into a call graph
# Output: call graph

import sys
import json

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: callchain-filter.py filename")

    with open(sys.argv[1]) as json_fp:
        json_data = json.load(json_fp)

    known_links = set()
    known_ends = set()

    for call_chains in json_data["call_chains"]:
        if len(call_chains) == 0:
            raise Exception("Empty call chain is not allowed")

        prev = 0

        for i, item in enumerate(call_chains):
            if i == 0:
                if item != 0:
                    raise Exception("The first item of a call chain must have id:0")
                continue

            if i != 0 and item == 0:
                raise Exception("Only the first item of a call chain can have id:0")

            if item != -1 and prev != -1:
                known_links.add((prev, item))
            prev = item

        known_ends.add(prev)

    sys.stdout.write("{\n\"directed\": true,\n\"multigraph\": false,\n\"nodes\": [\n")
    sys.stdout.write("  { \"id\": 0, \"label\": \"<entry>\", \"pos\": \"<entry>\", \"entry\": true }")

    entry_found = False
    for node in json_data["nodes"]:
        node_id = node["id"]

        if node_id == 0:
            entry_found = True
            continue

        if node_id < 0:
            raise Exception("Negative node id (%d) is not allowed" % (node_id))

        final = ""
        if node_id in known_ends:
            final = ", \"final\": true"

        sys.stdout.write(",\n  { \"id\": %d, \"label\": %s, \"pos\": %s%s }"
                         % (node_id, json.dumps(node["label"]), json.dumps(node["pos"]), final))

    if not entry_found:
        raise Exception("Entry node (id:0) not found")

    sys.stdout.write("\n],\n\"links\": [")

    comma = False

    for link in known_links:
        if comma:
            sys.stdout.write(",")
        comma = True

        sys.stdout.write("\n  { \"source\": %d, \"target\": %d }" % (link[0], link[1]))

    sys.stdout.write("\n]\n}\n")
