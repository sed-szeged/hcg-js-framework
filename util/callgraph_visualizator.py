import json
from util.path_handler import *


def generate_dynamic_cg_visualization(node_module):
    if not is_exists(get_stack_json_path(node_module)):
        return

    with open(get_stack_json_path(node_module)) as f:
        stack_file = json.load(f)

    with open(get_callgraph_visualization_path(node_module), "w") as visualization:
        for data in stack_file['stack']:
            spacing = '\t' * (data['depth'] - 1)

            if "test" in data['long_name'].split("/")[0] or "test" in data['long_name'].split("/")[0]:
                continue

            print(f"{spacing}--> {data['long_name'] + '@@' + data['name']}", file=visualization)


#  TODO generate static-cg visualization
