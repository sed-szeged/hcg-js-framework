#!/usr/bin/env python

import sys
import json

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: convert-event-log.py [-cg] filename")

    args_idx = 1
    call_graph = False
    if sys.argv[1] == "-cg":
        if len(sys.argv) < 3:
            sys.exit("Usage: convert-callchain-event-log.py [-cg] filename")
        args_idx = 2
        call_graph = True

    with open(sys.argv[args_idx]) as json_fp:
        json_data = json.load(json_fp)

    sys.stdout.write("{\n\"directed\": true,\n\"multigraph\": false,\n\"nodes\": [\n")
    sys.stdout.write("  { \"id\": 0, \"label\": \"<entry>\", \"pos\": \"<entry>\", \"entry\": true }")

    entry_found = False
    known_ids = set()

    for node in json_data:
        if not isinstance(node, dict):
            continue

        node_id = node["id"]
        if node_id == 0:
            if entry_found:
                raise Exception("Entry node was found before")
            entry_found = True
            continue

        if node_id in known_ids:
            raise Exception("Multiple definition of %s" % (node_id))

        known_ids.add(node_id)

        sys.stdout.write(",\n  { \"id\": %d, \"label\": \"\", \"pos\": %s }"
                         % (node_id, json.dumps(node["pos"])))

    if not entry_found:
        raise Exception("Entry node (id:0) not found")

    if call_graph:
        sys.stdout.write("\n],\n\"links\": [")
    else:
        sys.stdout.write("\n],\n\"call_chains\": [")

    known_ids = None
    known_chains = set()

    comma = False

    for node in json_data:
        if isinstance(node, dict):
            continue

        if comma:
            sys.stdout.write(",");
        comma = True

        chain = tuple(node)

        if call_graph:
            known_chains.add(chain)
            sys.stdout.write("\n  { \"source\": %d, \"target\": %d }" % (chain[0], chain[1]))
        else:
            if chain[0] != 0:
                raise Exception("All chains must start with 0")

            if chain in known_chains:
                raise Exception("Chain already found")

            known_chains.add(chain)
            sys.stdout.write("\n  %s" % (json.dumps(chain)))

    sys.stdout.write("\n]\n}\n")
