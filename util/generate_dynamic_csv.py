import os
import json
import csv

from util.file_handler import *

statement_whitelist_mcc = [
    'IfStatement',
    'ForStatement',
    'ForInStatement',
    'ForOfStatement',
    'WhileStatement',
    'DoWhileStatement',
    'CatchClause',
    'SwitchCase',
    'ConditionalExpression',
    'LogicalExpression'
]

statement_whitelist_nl = [
    'IfStatement',
    'ForStatement',
    'ForInStatement',
    'ForOfStatement',
    'WhileStatement',
    'DoWhileStatement',
    'CatchClause',
    'TryStatement',
    'FinallyClause',
    'DirectBlockStatement',
    'ConditionalExpression',
    'SwitchCase'
]


def calculate_number_of_methods(classes, parent_class):
    # Class: number of methods in the class, including the inherited ones.

    return len(class_methods_with_inheritance(classes)[parent_class])


def calculate_weighted_methods_per_class(classes, parent_class):
    # Class: complexity of the class expressed as the number of independent control flow paths in it.
    # It is calculated as the sum of the McCabe’s Cyclomatic Complexity (McCC) values of its local methods.

    result = 0

    for _class in classes:
        for method in _class['methods']:
            class_name = _class['name'] if ':' not in _class['name'] else _class['name'].split(':')[1]
            if class_name == parent_class:
                result += calculate_mccabe(method['statements'])

    return result


def find_max_depth(statements):
    max = 0
    for statement in statements:
        if statement['type'] in statement_whitelist_nl and statement['depth'] > max:
            max = statement['depth']

    return max


def calculate_mccabe(statements):
    mcc_value = 0
    for statement in statements:
        if statement['type'] in statement_whitelist_mcc:
            mcc_value += 1

    return mcc_value + 1


def class_data(classes):
    result = []  # set

    for _class in classes:
        for method in _class['methods']:
            if ':' in _class['name'] and method['is_called']:  # extends another class
                child_class = _class['name'].split(':')[1]
                parent_class = _class['name'].split(':')[0]

                if child_class not in [data[0] for data in result]:
                    result.append([child_class, method['long_name'], method['path'], method['line'], method['column']])
                if parent_class not in [data[0] for data in result]:
                    result.append([parent_class, method['long_name'], method['path'], method['line'], method['column']])

            elif ':' not in _class['name'] and method['is_called']:  # no inheritance
                parent_class = _class['name']

                if parent_class not in [data[0] for data in result]:
                    result.append([parent_class, method['long_name'], method['path'], method['line'], method['column']])

    return result


def inheritance_chains(classes):
    chains = set()

    for _class in classes:
        if ':' in _class['name']:  # extends another class
            child_class = _class['name'].split(':')[1]
            parent_class = _class['name'].split(':')[0]

            chains.add((child_class, parent_class))
        else:
            parent_class = _class['name'].split(':')[0]

            chains.add((parent_class))

    return chains


def get_parents(chains, class_name):
    for chain in chains:
        if len(chain) == 1 and chain[0] == class_name:
            break
        elif chain[0] == class_name:
            yield chain[1]
            yield from get_parents(chains, chain[1])


def inheritance_graph(classes):
    chains = inheritance_chains(classes)

    result = []

    for data in class_data(classes):
        graph = [data[0]]

        for parent_class in get_parents(chains, data[0]):
            graph.append(parent_class)

        result.append(graph)

    return result


def class_methods(classes):
    result = {}

    # init dictionary with classes
    for _class in classes:
        class_name = _class['name'] if ':' not in _class['name'] else _class['name'].split(':')[1]
        result[class_name] = set()
        for method in _class['methods']:
            result[class_name].add(method['long_name'])

    # for data in class_data(functions):
    #     class_name = data[0]
    #     for function in functions:
    #         function_name = function['function_id'].split('@')[1].split(':')[0]
    #
    #         if _class['name'] and ':' in _class['name'] and function['is_called']:
    #             # extends super class
    #             if class_name == _class['name'].split(':')[1]:
    #                 result[class_name].add(function_name)
    #
    #         if _class['name'] and ':' not in _class['name'] and function['is_called']:
    #             # no inheritance
    #             if class_name == _class['name']:
    #                 result[class_name].add(function_name)

    return result


def class_methods_with_inheritance(classes):
    graph = inheritance_graph(classes)
    my_class_methods = class_methods(classes)
    result = {}

    # init result
    for chain in graph:
        child_name = chain[0]
        result[child_name] = set()

    for chain in graph:
        child_name = chain[0]
        for class_name in chain:
            for method in my_class_methods[class_name]:
                result[child_name].add(method)

    return result


# Write each row in the following format to json:
# Name | Long Name | Path | Line | Column | McCC | NL
def row_format(function):
    result = [
        function['name'], function['long_name'], function['path'], function['line'], function['column'],
        calculate_mccabe(function['statements']), find_max_depth(function['statements'])
    ]
    return result


def write_filtered_row(writer, func):
    """
    If the function path contains the word 'test' don't write to the csv
    @param writer: csv writer
    @param row: output format
    @param func: function from data
    """

    if 'test' in func['path']:
        return

    writer.writerow(row_format(func))


def generate_dynamic_function_metrics(data, node_module):
    """
    Generates Function.csv from Function.json
    ===Header===
    'Name' 'Long Name'  'Path'  'Line'  'Column'  'McCC' 'NL'

    +Filters out the functions that comes from '*test*' folder

    @param data: Function.json raw file
    @param node_module
    """
    working_dir = latest_dir(f"results/{node_module['name']}")

    with open(f"results/{node_module['name']}/{working_dir}/metric/dynamic/Dynamic-Function.csv",
              mode='w') as filtered_csv:
        writer = csv.writer(filtered_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # write header
        writer.writerow(['Name', 'Long Name', 'Path', 'Line', 'Column', 'McCC', 'NL'])

        for function in data['functions']:
            write_filtered_row(writer, function)


def generate_dynamic_method_metrics(data, node_module):
    working_dir = latest_dir(f"results/{node_module['name']}")

    with open(f"results/{node_module['name']}/{working_dir}/metric/dynamic/Dynamic-Method.csv",
              mode='w') as filtered_csv:
        writer = csv.writer(filtered_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # write header
        writer.writerow(['Name', 'Long Name', 'Path', 'Line', 'Column', 'McCC', 'NL'])

        for _class in data['classes']:
            for method in _class['methods']:
                writer.writerow(row_format(method))


# Generate dynamic metrics csv:
# metrics: Number of Methods, Weighted Methods per Class
# Format!
# Class Name | Long Name | Path | Line | Column | NM | WMC
def generate_dynamic_class_metrics(data, node_module):
    working_dir = latest_dir(f"results/{node_module['name']}")

    with open(f"results/{node_module['name']}/{working_dir}/metric/dynamic/Dynamic-Class.csv",
              mode='w') as filtered_csv:
        writer = csv.writer(filtered_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Name', 'Long Name', 'Path', 'Line', 'Column', 'NM', 'WMC'])  # 6 column

        # NM = lambda class_name: calculate_number_of_methods(data['classes'], class_name)
        # WMC = lambda class_name: calculate_weighted_methods_per_class(data['classes'], class_name)

        for _class in data['classes']:
            class_name = _class['name'] if ':' not in _class['name'] else _class['name'].split(':')[1]

            for method in _class['methods']:
                if method['is_called']:
                    break
            else:
                continue

            writer.writerow([class_name, _class['long_name'], _class['path'], _class['line'], _class['column'],
                             calculate_number_of_methods(data['classes'], class_name),
                             calculate_weighted_methods_per_class(data['classes'], class_name)])


def create_dynamic_csv(node_module):
    working_dir = latest_dir(f"results/{node_module['name']}")

    if os.path.exists(f"results/{node_module['name']}/{working_dir}/metric/dynamic"):
        function_data = json.load(open(f"results/{node_module['name']}/{working_dir}/metric/dynamic/function.json"))
        class_data = json.load(open(f"results/{node_module['name']}/{working_dir}/metric/dynamic/class.json"))

        generate_dynamic_function_metrics(function_data, node_module)
        generate_dynamic_method_metrics(class_data, node_module)

        generate_dynamic_class_metrics(class_data, node_module)

    else:
        print(f"Error: Results not found for: \'{node_module['name']}\'")
