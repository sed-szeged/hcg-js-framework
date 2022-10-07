import json
import csv
from util.path_handler import *


def get_source(stack, depth, target_id):
    for _id in range(target_id - 1, -1, -1):
        source = stack[_id]
        if source['depth'] == depth - 1:
            return source

    return {'long_name': 'entry', 'name': 'entry', 'depth': 0}


def get_edges(node_module):
    edges = set()

    with open(get_stack_json_path(node_module)) as f:
        stack_json = json.load(f)

    target_id = 0
    for target in stack_json['stack']:
        source = get_source(stack_json['stack'], target['depth'], target_id)

        if source['name'] == 'entry':
            target_id += 1
            continue

        if "test" in source['long_name'].split("/")[0] or "test" in target['long_name'].split("/")[0]:
            target_id += 1
            continue

        edge = source['long_name'] + "@@" + source['name'] + "->" + target['long_name'] + "@@" + target['name']

        edges.add(edge)
        target_id += 1

    return edges


def generate_dyn_cg_csv(node_module):
    with open(get_dyn_cg_csv_path(node_module), "w") as dyn_cg:
        writer = csv.writer(dyn_cg, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["dyn-cg"])  # Header

        for edge in get_edges(node_module):
            writer.writerow([edge])
