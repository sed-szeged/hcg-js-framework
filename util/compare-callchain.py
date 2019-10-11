#!/usr/bin/env python

# Compare two call chains with the same node list
# Output: list of unique call chains

import sys
import json

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: compare-callchain.py [-s] filename1 filename2")

    silent = False
    args_idx = 1
    if sys.argv[1] == "-s":
        if len(sys.argv) < 4:
            sys.exit("Usage: compare-callchain.py [-s] filename1 filename2")
        args_idx = 2
        silent = True

    with open(sys.argv[args_idx]) as json_fp:
        json_data1 = json.load(json_fp)

    with open(sys.argv[args_idx + 1]) as json_fp:
        json_data2 = json.load(json_fp)

    nodes1 = json_data1["nodes"]
    nodes2 = json_data2["nodes"]

    if len(nodes1) != len(nodes2):
        raise Exception("Number of nodes in the two JSON files mismatch")

    for i in range(0, len(nodes1)):
        node1 = nodes1[i]
        node2 = nodes2[i]

        if node1["id"] != node2["id"]:
            raise Exception("Id mismatch for node %d" % (i))

        if node1["label"] != node2["label"]:
            raise Exception("Label mismatch for node %d" % (i))

        if node1["pos"] != node2["pos"]:
            raise Exception("Pos mismatch for node %d" % (i))

    call_chains2 = set()
    for call_chain in json_data2["call_chains"]:
        call_chains2.add(tuple(call_chain))

    print("Unique call chains in %s" % (sys.argv[1]))

    call_chains1 = set()
    unique_cntr = 0
    for call_chain in json_data1["call_chains"]:
        call_chain_tuple = tuple(call_chain)

        call_chains1.add(call_chain_tuple)

        if not call_chain_tuple in call_chains2:
            if not silent:
                print(call_chain_tuple)
            unique_cntr += 1

    print("Found %d unique call chains from %d in %s" %
          (unique_cntr, len(json_data1["call_chains"]), sys.argv[1]))

    print("Unique call chains in %s" % (sys.argv[2]))

    unique_cntr = 0
    for call_chain in json_data2["call_chains"]:
        call_chain_tuple = tuple(call_chain)

        if not call_chain_tuple in call_chains1:
            if not silent:
                print(call_chain_tuple)
            unique_cntr += 1

    print("Found %d unique call chains from %d in %s" %
          (unique_cntr, len(json_data2["call_chains"]), sys.argv[2]))
