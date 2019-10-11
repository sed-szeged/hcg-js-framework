#!/usr/bin/env python

# Compare the differences of in and out edges for the same node list
# Output: a pair list where the first number is the difference, and
#         the second number is the number of nodes with that difference

import sys
import json

def incr(count_map, diff, max_diff):
    value = count_map.get(diff, 0)
    count_map[diff] = value + 1
    return max(max_diff, diff + 1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: compare-cg-in-out.py filename1 filename2")

    with open(sys.argv[1]) as json_fp:
        json_data1 = json.load(json_fp)

    with open(sys.argv[2]) as json_fp:
        json_data2 = json.load(json_fp)

    if len(json_data1) != len(json_data2):
        raise Exception("Number of nodes in the two JSON files mismatch")

    in_count_map = {}
    out_count_map = {}
    in_max_diff = 1
    out_max_diff = 1

    for i in range(0, len(json_data1)):
        node1 = json_data1[i]
        node2 = json_data2[i]

        if node1["id"] != i or node2["id"] != i:
            raise Exception("Wrong node id")

        if node1["label"] != node2["label"] or node1["pos"] != node2["pos"]:
            raise Exception("Node data mismatch")

        diff = abs(node1["in"] - node2["in"])
        in_max_diff = incr(in_count_map, diff, in_max_diff)

        diff = abs(node1["out"] - node2["out"])
        out_max_diff = incr(out_count_map, diff, out_max_diff)

    sys.stdout.write("in")
    for i in range(0, in_max_diff):
        sys.stdout.write("; %d:%d" % (i, in_count_map.get(i, 0)))
    sys.stdout.write("\n")

    sys.stdout.write("out")
    for i in range(0, out_max_diff):
        sys.stdout.write("; %d:%d" % (i, out_count_map.get(i, 0)))
    sys.stdout.write("\n")
