#!/usr/bin/env python

# Compare two call chains with the same node list
# Output: list of unique call chains

import sys
import json

def find_common_chains(json_data1, json_data2, json_data3):
    call_chains1 = set()
    for call_chain in json_data1["call_chains"]:
        call_chains1.add(tuple(call_chain))

    call_chains2 = set()
    for call_chain in json_data2["call_chains"]:
        call_chain_tuple = tuple(call_chain)
        if call_chain_tuple in call_chains1:
            call_chains2.add(call_chain_tuple)

    call_chains1 = set()
    for call_chain in json_data3["call_chains"]:
        call_chain_tuple = tuple(call_chain)
        if call_chain_tuple in call_chains2:
            call_chains1.add(call_chain_tuple)

    return call_chains1


def find_unique_chains(json_data, json_other_data1, json_other_data2, silent):
    call_chains = set()

    for call_chain in json_other_data1["call_chains"]:
        call_chains.add(tuple(call_chain))

    for call_chain in json_other_data2["call_chains"]:
        call_chains.add(tuple(call_chain))

    counter = 0
    for call_chain in json_data["call_chains"]:
        call_chain_tuple = tuple(call_chain)
        if call_chain_tuple in call_chains:
            continue

        counter += 1
        if not silent:
            print(call_chain_tuple)

    return counter


def find_common_duo_chains(json_data1, json_data2, json_other_data, silent):
    other_call_chains = set()

    for call_chain in json_other_data["call_chains"]:
        other_call_chains.add(tuple(call_chain))

    call_chains = set()

    for call_chain in json_data1["call_chains"]:
        call_chain_tuple = tuple(call_chain)
        if call_chain_tuple not in other_call_chains:
            call_chains.add(call_chain_tuple)

    counter = 0
    for call_chain in json_data2["call_chains"]:
        call_chain_tuple = tuple(call_chain)
        if call_chain_tuple not in call_chains:
            continue

        counter += 1
        if not silent:
            print(call_chain_tuple)

    return counter


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit("Usage: compare-callchain3.py [-s] filename1 filename2 filename3")

    silent = False
    args_idx = 1
    if sys.argv[1] == "-s":
        if len(sys.argv) < 5:
            sys.exit("Usage: compare-callchain.py [-s] filename1 filename2 filename3")
        args_idx = 2
        silent = True

    with open(sys.argv[args_idx]) as json_fp:
        json_data1 = json.load(json_fp)

    with open(sys.argv[args_idx + 1]) as json_fp:
        json_data2 = json.load(json_fp)

    with open(sys.argv[args_idx + 2]) as json_fp:
        json_data3 = json.load(json_fp)

    nodes1 = json_data1["nodes"]
    nodes2 = json_data2["nodes"]
    nodes3 = json_data2["nodes"]

    if len(nodes1) != len(nodes2) or len(nodes1) != len(nodes3):
        raise Exception("Number of nodes in the three JSON files mismatch")

    for i in range(0, len(nodes1)):
        node1 = nodes1[i]
        node2 = nodes2[i]
        node3 = nodes3[i]

        if node1["id"] != node2["id"] or node1["id"] != node3["id"]:
            raise Exception("Id mismatch for node %d" % (i))

        if node1["label"] != node2["label"] or node1["label"] != node3["label"]:
            raise Exception("Label mismatch for node %d" % (i))

        if node1["pos"] != node2["pos"] or node1["pos"] != node3["pos"]:
            raise Exception("Pos mismatch for node %d" % (i))


    common_chains = find_common_chains(json_data1, json_data2, json_data3)

    print("Number of common call chains %s" % (len(common_chains)))

    unique_chains1 = find_unique_chains(json_data1, json_data2, json_data3, silent)
    print("Number of unique chains in %s : %d" % (sys.argv[args_idx], unique_chains1))

    unique_chains2 = find_unique_chains(json_data2, json_data1, json_data3, silent)
    print("Number of unique chains in %s : %d" % (sys.argv[args_idx + 1], unique_chains2))

    unique_chains3 = find_unique_chains(json_data3, json_data1, json_data2, silent)
    print("Number of unique chains in %s : %d" % (sys.argv[args_idx + 2], unique_chains3))

    common12 = find_common_duo_chains(json_data1, json_data2, json_data3, silent)
    print("Number of common chains in %s and %s : %d" % (sys.argv[args_idx], sys.argv[args_idx + 1], common12))

    common13 = find_common_duo_chains(json_data1, json_data3, json_data2, silent)
    print("Number of common chains in %s and %s : %d" % (sys.argv[args_idx], sys.argv[args_idx + 2], common13))

    common23 = find_common_duo_chains(json_data2, json_data3, json_data1, silent)
    print("Number of common chains in %s and %s : %d" % (sys.argv[args_idx + 1], sys.argv[args_idx + 2], common23))

    common = len(common_chains)
    if len(json_data1["call_chains"]) != common + unique_chains1 + common12 + common13:
        raise Exception("Sanity error: data set 1")
    if len(json_data2["call_chains"]) != common + unique_chains2 + common12 + common23:
        raise Exception("Sanity error: data set 2")
    if len(json_data3["call_chains"]) != common + unique_chains3 + common13 + common23:
        raise Exception("Sanity error: data set 3")

