import csv, os

from util.file_handler import *
from util.color import Colors

# TODO !important : calculate column index dynamically
# Specifies in which column the metric is located in the csv file
metric_index = {
    # Function
    'McCC': 5,
    'NL': 6,

    # Class
    'NM': 5,
    'WMC': 6
}


# TODO : !important : calculate headers dynamically
def row_data(row, index):
    result = dict(
        name=row[0],
        long_name=row[1],
        metric=row[index],
        path=row[2],
        line=row[3],
        column=row[4],
        id=row[2] + ":" + row[3]  # path + line
    )

    return result


# Row format should match with the csv header:
# Name | Long Name | Path | Line | Column | Dynamic Metric | Static Metric | Static Long Name | Static Path
def row_format(dynamic, static, _type):
    result = []
    if _type == "shared":
        result = [
            dynamic['name'], dynamic['long_name'], dynamic['path'], dynamic['line'], dynamic['column'],
            dynamic['metric'], static['metric'],
            static['long_name'], static['path']
        ]

    if _type == "dynamic_only":
        result = [
            dynamic['name'], dynamic['long_name'], dynamic['path'], dynamic['line'], dynamic['column'],
            dynamic['metric'], ' ',
            ' ', ' '
        ]

    if _type == "static_only":
        result = [
            static['name'], static['long_name'], static['path'], static['line'], static['column'],
            ' ', static['metric'],
            ' ', ' '
        ]

    return result


def read_csv(path):
    if not is_exists(path):
        return []

    with open(path, newline='') as csv_file:
        csv_list = []
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            csv_list.append(row)
        return csv_list


def merge_metric_csv(static_csv, dynamic_csv, metric, is_class=False):
    merged_csv = []

    index = metric_index[metric]

    # remove headers [Name, Long Name, Path, Column, Line, McCC, NL]
    static_csv.pop(0)
    dynamic_csv.pop(0)

    # sort by name
    static_csv.sort(key=lambda x: x[0], reverse=True)
    dynamic_csv.sort(key=lambda x: x[0], reverse=True)

    # d = dynamic
    # s = static
    dynamic_id_set = set()
    static_id_set = set()

    # append shared functions; comparing by path+line
    for d_row in dynamic_csv:
        dynamic_row = row_data(d_row, index)

        for s_row in static_csv:
            static_row = row_data(s_row, index)
            if dynamic_row['id'] == static_row['id']:
                merged_csv.append(row_format(dynamic_row, static_row, "shared"))
                dynamic_id_set.add(dynamic_row['id'])
                static_id_set.add(static_row['id'])

    # append functions only found by dynamic
    for d_row in dynamic_csv:
        dynamic_row = row_data(d_row, index)

        if dynamic_row['id'] not in dynamic_id_set:
            merged_csv.append(row_format(dynamic_row, None, "dynamic_only"))

    # append functions only found by static
    for static_row in static_csv:
        static_row = row_data(static_row, index)
        if static_row['id'] not in static_id_set:
            merged_csv.append(row_format(None, static_row, "static_only"))

    return merged_csv


def create_compared_csv(node_module, metric, metric_type):
    working_dir = latest_dir(f"results/{node_module['name']}")

    # compared relative path: results/repository/compared
    cmp_path = f"results/{node_module['name']}/"

    static_csv = read_csv(cmp_path + f"{working_dir}/metric/static/Static-{metric_type}-Filtered.csv")
    dynamic_csv = read_csv(cmp_path + f"{working_dir}/metric/dynamic/Dynamic-{metric_type}.csv")

    if not os.path.exists(f"results/{node_module['name']}/{working_dir}/metric/compared"):
        os.mkdir(f"results/{node_module['name']}/{working_dir}/metric/compared")

    with open(f"{cmp_path}/{working_dir}/metric/compared/{metric}-{metric_type}-compared.csv", mode='w') as merged_csv:
        writer = csv.writer(merged_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        is_class = True if metric_type == 'Class' else False
        merged_csv = merge_metric_csv(static_csv, dynamic_csv, metric, is_class=is_class)

        writer.writerow(['Name', 'Long Name', 'Path', 'Line', 'Column', f"Dynamic {metric}", f"Static {metric}",
                         f'Static Long Name', 'Static Path'])

        for row in merged_csv:
            writer.writerow(row)


def create_all_compared_csv(node_module):
    create_compared_csv(node_module, 'McCC', "Function")
    create_compared_csv(node_module, 'NL', "Function")

    create_compared_csv(node_module, 'McCC', "Method")
    create_compared_csv(node_module, 'NL', "Method")

    create_compared_csv(node_module, 'NM', "Class")
    create_compared_csv(node_module, 'WMC', "Class")


def convert_to_relative(path):
    return path.split('node-sources/')[1]


def merge_static_with_dynamic_callgraphs(node_module):
    results_path = f"results/{node_module['name']}"
    working_dir = f"{results_path}/{latest_dir(results_path)}/callgraphs/"

    merged_csv = read_csv(working_dir + "x-compared/merged.csv")
    dynamic_csv = read_csv(working_dir + "dynamic/dyn-cg.csv")

    # remove absolute path from merged_csv
    for i in range(len(merged_csv)):
        if i == 0:
            continue
        # 'acg-demand'  'acg-oneshot'
        demand_source = merged_csv[i][0].split('->')[0]
        demand_target = merged_csv[i][0].split('->')[1]
        demand_edge = convert_to_relative(demand_source) + "->" + convert_to_relative(demand_target)

        oneshot_source = merged_csv[i][1].split('->')[0]
        oneshot_target = merged_csv[i][1].split('->')[1]
        oneshot_edge = convert_to_relative(oneshot_source) + "->" + convert_to_relative(oneshot_target)

        merged_csv[i] = [demand_edge, oneshot_edge]

    merged_csv.sort(key=lambda x: int(x[0].split(":")[1]) if ":" in x[0] else 0)
    dynamic_csv.sort(key=lambda x: int(x[0].split(":")[1]) if ":" in x[0] else 0)

    # merged is longer
    if len(merged_csv) > len(dynamic_csv):
        for i in range(len(merged_csv)):
            try:
                merged_csv[i].append(dynamic_csv[i][0])
            except IndexError:
                merged_csv[i].append(" ")
    else:
        for i in range(len(dynamic_csv)):
            try:
                merged_csv[i].append(dynamic_csv[i][0])
            except IndexError:
                merged_csv.append([" ", " ", dynamic_csv[i][0]])

    with open(working_dir + "x-compared/result.csv", mode='w') as result_csv:
        writer = csv.writer(result_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in merged_csv:
            writer.writerow(row)
