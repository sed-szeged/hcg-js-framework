from util.file_handler import *


def get_stack_json_path(node_module):
    return f"node-sources/{node_module['name']}/" + "stack.json"


def get_callgraph_visualization_path(node_module):
    module_path = f"results/{node_module['name']}"

    return f"{module_path}/{latest_dir(module_path)}/callgraphs/dynamic/" + "visualization.txt"


def get_dyn_cg_csv_path(node_module):
    module_path = f"results/{node_module['name']}"

    return f"{module_path}/{latest_dir(module_path)}/callgraphs/dynamic/" + "dyn-cg.csv"






