#!/usr/bin/env python

# Remove user specified nodes from the "nodes" list.
# Remove (-) or keep (+) nodes matching for a regular expression
# Call chains are also updated to contain only unique chains
# If S is specified, the removed parts of a chain are replaced by a single -1
# Output: filtered call chain

import sys
import json
import re

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit("Usage: callchain-filter.py filename [+|-] pattern")

    pattern = re.compile(sys.argv[3])

    if sys.argv[2] == "+":
        include = True
    elif sys.argv[2] == "-":
        include = False
    else:
        sys.exit("Error: second argument must be + or -")

    with open(sys.argv[1]) as json_fp:
        json_data = json.load(json_fp)

    sys.stdout.write("{\n\"directed\": true,\n\"multigraph\": false,\n\"nodes\": [\n")
    sys.stdout.write("  { \"id\": 0, \"label\": \"<entry>\", \"pos\": \"<entry>\", \"entry\": true }")

    id_map = { 0:0, -1:-1 }

    next_id = 1
    entry_found = False
    for node in json_data["nodes"]:
        if node["id"] == 0:
            if not "entry" in node or not node["entry"]:
                raise Exception("Node with id:0 must be an entry node")
            if entry_found:
                raise Exception("Node with id:0 was found before")
            entry_found = True
            continue

        if "entry" in node and node["entry"]:
            raise Exception("Only node with id:0 can be an entry node")

        found = pattern.search(node["pos"]) != None
        if (include and found) or (not include and not found):
            sys.stdout.write(",\n  { \"id\": %d, \"label\": %s, \"pos\": %s }"
                             % (next_id, json.dumps(node["label"]), json.dumps(node["pos"])))

            id_map[node["id"]] = next_id
            next_id += 1

    if not entry_found:
        raise Exception("Entry node (id:0) not found")

    sys.stdout.write("\n],\n\"call_chains\": [")

    known_chains = set()

    for call_chain in json_data["call_chains"]:
        if len(call_chain) < 1:
            raise Exception("Empty call chain is not allowed")

        if call_chain[0] != 0:
             raise Exception("The first item of a call chain must have id:0")

        for i, item in enumerate(call_chain):
            if i != 0 and item == 0:
                raise Exception("Only the first item of a call chain can have id:0")

        new_call_chain = []
        separator_seen = False
        for value in tuple(id_map.get(idx, -1) for idx in call_chain):
            if value == -1:
                if not separator_seen:
                    new_call_chain.append(-1)
                    separator_seen = True
                continue

            new_call_chain.append(value)
            separator_seen = False

        known_chains.add(tuple(new_call_chain))

    comma = False

    for chain in known_chains:
        if comma:
            sys.stdout.write(",")
        comma = True

        sys.stdout.write("\n  %s" % (json.dumps(chain)))

    sys.stdout.write("\n]\n}\n")
