#!/usr/bin/env python

import sys
import json

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: compare-nodes.py [-s|-c] filename1 filename2")

    details = True
    common = False
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    if sys.argv[1] == "-s":
        details = False
        file1 = sys.argv[2]
        file2 = sys.argv[3]
    elif sys.argv[1] == "-c":
        details = False
        common = True
        file1 = sys.argv[2]
        file2 = sys.argv[3]

    with open(file1) as json_fp:
        json_data1 = json.load(json_fp)

    with open(file2) as json_fp:
        json_data2 = json.load(json_fp)

    nodes1 = json_data1["nodes"]
    nodes2 = json_data2["nodes"]
    nodes1_pos = set()
    nodes2_pos = set()

    for node in nodes1:
        nodes1_pos.add(node["pos"])

    for node in nodes2:
        nodes2_pos.add(node["pos"])

    if details:
        print("Unique nodes in %s" % (file1))

    unique_cntr1 = 0
    for node in nodes1:
        pos = node["pos"]
        if pos not in nodes2_pos:
            unique_cntr1 += 1
            if details:
                print("id:%d label:\"%s\" (%s)" % (node["id"], node["label"], pos))
        elif common:
            print("pos: %s" % (pos))

    length1 = len(nodes1)
    print("Found %d unique and %d non-unique nodes from %d in %s" %
          (unique_cntr1, length1 - unique_cntr1, length1, file1))

    if details:
        print("Unique nodes in %s" % (file2))

    unique_cntr2 = 0
    for node in nodes2:
        pos = node["pos"]
        if pos not in nodes1_pos:
            unique_cntr2 += 1
            if details:
                print("id:%d label:\"%s\" (%s)" % (node["id"], node["label"], pos))

    length2 = len(nodes2)
    print("Found %d unique and %d non-unique nodes from %d in %s" %
          (unique_cntr2, length2 - unique_cntr2, length2, file2))

    length = length1 + unique_cntr2
    print("Stats: unique1: %d (%.2f%%) common: %d (%.2f%%) unique2: %d (%.2f%%) total: %d (100%%)" %
          (unique_cntr1, unique_cntr1 * 100.0 / length, length1 - unique_cntr1,
           (length1 - unique_cntr1) * 100.0 / length, unique_cntr2, unique_cntr2 * 100.0 / length, length))
