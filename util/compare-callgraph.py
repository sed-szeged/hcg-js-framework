#!/usr/bin/env python

# Compare two call graphs with the same node list
# Output: list of unique edges

import sys
import json

def desc(nodes, node_id):
    return "id:%d label:\"%s\" (%s)" % (node_id, nodes[node_id]["label"], nodes[node_id]["pos"])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: compare-callgraph.py [-s] filename1 filename2")

    details = True
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    if sys.argv[1] == "-s":
        details = False
        file1 = sys.argv[2]
        file2 = sys.argv[3]

    with open(file1) as json_fp:
        json_data1 = json.load(json_fp)

    with open(file2) as json_fp:
        json_data2 = json.load(json_fp)

    nodes1 = json_data1["nodes"]
    nodes2 = json_data2["nodes"]

    if len(nodes1) != len(nodes2):
        raise Exception("Number of nodes in the two JSON files mismatch")

    nodes = {}

    for i in range(0, len(nodes1)):
        node1 = nodes1[i]
        node2 = nodes2[i]

        if node1["id"] != node2["id"]:
            raise Exception("Id mismatch for node %d" % (i))

        if node1["label"] != node2["label"]:
            raise Exception("Label mismatch for node %d" % (i))

        if node1["pos"] != node2["pos"]:
            raise Exception("Pos mismatch for node %d" % (i))

        nodes[node1["id"]] = node1

    links2 = set()
    for link in json_data2["links"]:
        links2.add((link["source"], link["target"]))

    if details:
        print("Unique links in %s" % (file1))

    links1 = set()
    unique_cntr1 = 0
    for link in json_data1["links"]:
        source = link["source"]
        target = link["target"]
        link_tuple = (source, target)

        links1.add(link_tuple)

        if not link_tuple in links2:
            if details:
                print("source: %s -> target: %s" % (desc(nodes, source), desc(nodes, target)))
            unique_cntr1 += 1

    length1 = len(json_data1["links"])
    print("Found %d unique and %d non-unique links from %d in %s" %
          (unique_cntr1, length1 - unique_cntr1, length1, file1))

    if details:
        print("Unique links in %s" % (file2))

    unique_cntr2 = 0
    for link in json_data2["links"]:
        source = link["source"]
        target = link["target"]
        link_tuple = (source, target)

        if not link_tuple in links1:
            if details:
                print("source: %s -> target: %s" % (desc(nodes, source), desc(nodes, target)))
            unique_cntr2 += 1

    length2 = len(json_data2["links"])
    print("Found %d unique and %d non-unique links from %d in %s" %
          (unique_cntr2, length2 - unique_cntr2, length2, file2))

    length = length1 + unique_cntr2
    print("Stats: unique1: %d (%.2f%%) common: %d (%.2f%%) unique2: %d (%.2f%%) total: %d (100%%)" %
          (unique_cntr1, unique_cntr1 * 100.0 / length, length1 - unique_cntr1,
           (length1 - unique_cntr1) * 100.0 / length, unique_cntr2, unique_cntr2 * 100.0 / length, length))

