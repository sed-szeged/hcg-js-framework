from util.file_handler import *
from util.mapper.function_mapper_algorithm import *
from util.mapper.function_mapper_sheets import update_note, push_to_sheets
from util.mapper.output_handler import *

RESULTS_DIR = 'mapping-results'


def filter_data_from_all(p_repo_name):
    result = []

    with open('util/mapper/original.csv', 'r') as filtered_csv_file:
        data = filtered_csv_file.readlines()

        data_header = data[0].split(',')
        data_header[-1] = data_header[-1].strip()
        data_header.insert(0, 'repo_name')
        result.append(data_header)

        for row in data[1:]:
            row = row.split(',')
            row[-1] = row[-1].rstrip()
            repo_name = row[3].split('blob')[0].split('/')[-2]
            row.insert(0, repo_name)

            if repo_name == p_repo_name:
                result.append(row)

    return result


def merge_metric_csv(static_csv, dynamic_csv):
    result = []
    id = 1

    def column_indexes(header):
        result = {}

        index = 0
        for column_name in header:
            result[column_name] = index
            index += 1
        return result

    def convert_row_into_data_strut(row, column_indexes):
        result = {}

        for column_name, index in column_indexes.items():
            result[column_name] = row[index]

        return result

    print(Colors.BOLD + Colors.CVIOLET2 + "Static functions:" + Colors.ENDC)
    print_line(200, '.')
    print(
        f"{'id':<5} | {'Repo name':30} | {'Name':50} | {'Long Name':50} | {'Line':10} | {'Column':10} | {'McCC':10} | {'NL':10}")

    static_column_indexes = column_indexes(static_csv[0])
    dynamic_column_indexes = column_indexes(dynamic_csv[0])

    static_count = len(static_csv[1:])
    dynamic_count = 0

    for static_row in static_csv[1:]:
        static = convert_row_into_data_strut(static_row, static_column_indexes)

        result.append(static)

        print(
            f"{str(id) + '.':<5} | {static['repo_name']:30} | {static['name']:50} | {static['longname']:50} | {static['line']:10} | "
            f"{static['column']:10} | {static['McCC']:10} | {static['NL']:10}")
        id += 1


        # dynamic_csv contains header
        for dynamic_row in dynamic_csv[1:]:
            # Name | Long Name | Path | Line | Column | McCC | NL
            dynamic = convert_row_into_data_strut(dynamic_row, dynamic_column_indexes)

            # Dynamic McCC and NL can't be larger than Static
            if int(dynamic['McCC']) > int(static['McCC']) or int(dynamic['NL']) > int(static['NL']):
                continue

            # if function in different lib -> skip
            # if static['longname'].split('.')[1] != dynamic['Long Name'].split('.')[1]:
            #     continue

            if static['name'] == dynamic['Name']:
                print_dynamic_row(dynamic)
                result.append(dynamic)
                dynamic_count += 1
                break

            if static['line'] == dynamic['Line'] and static['column'] == dynamic['Column']:
                print_dynamic_row(dynamic)
                result.append(dynamic)
                dynamic_count += 1
                break

            if static_name_in_dynamic(dynamic, static, line_threshold=0, column_threshold=5):
                print_dynamic_row(dynamic)
                result.append(dynamic)
                dynamic_count += 1
                break

            if static_name_in_dynamic(dynamic, static, line_threshold=0, column_threshold=100):
                print_dynamic_row(dynamic)
                result.append(dynamic)
                dynamic_count += 1
                break

            if line_column_threshold(dynamic, static, line_threshold=1, column_threshold=5):
                print_dynamic_row(dynamic)
                result.append(dynamic)
                dynamic_count += 1
                break

            if line_column_threshold(dynamic, static, line_threshold=1, column_threshold=100):
                print_dynamic_row(dynamic)
                result.append(dynamic)
                dynamic_count += 1
                break

        print_line(200, '.')

    result_count = {
        'static_count': static_count,
        'dynamic_count': dynamic_count,
    }

    print()
    print_line(200, '=')

    return [result, result_count]


def merge_metric_csv2(static_csv, dynamic_csv):
    result = []
    id = 1

    def column_indexes(header):
        result = {}

        index = 0
        for column_name in header:
            result[column_name] = index
            index += 1
        return result

    def convert_row_into_data_strut(row, column_indexes):
        result = {}

        for column_name, index in column_indexes.items():
            result[column_name] = row[index]

        return result

    def append_dynamic_metric_to_static(dynamic_row, metric):
        result[-1]['D_' + metric] = dynamic_row[metric]

    def append_dynamic_colom_to_static(metric):
        result[-1]['D_' + metric] = None

    print(Colors.BOLD + Colors.CVIOLET2 + "Static functions:" + Colors.ENDC)
    print_line(200, '.')
    print(
        f"{'id':<5} | {'Repo name':30} | {'Name':50} | {'Long Name':50} | {'Line':10} | {'Column':10} | {'McCC':10} | {'NL':10}")

    static_column_indexes = column_indexes(static_csv[0])
    dynamic_column_indexes = column_indexes(dynamic_csv[0])

    for static_row in static_csv[1:]:
        static = convert_row_into_data_strut(static_row, static_column_indexes)

        result.append(static)

        print(
            f"{str(id) + '.':<5} | {static['repo_name']:30} | {static['name']:50} | {static['longname']:50} | {static['line']:10} | "
            f"{static['column']:10} | {static['McCC']:10} | {static['NL']:10}")
        id += 1

        # dynamic_csv contains header
        for dynamic_row in dynamic_csv[1:]:
            # Name | Long Name | Path | Line | Column | McCC | NL
            dynamic = convert_row_into_data_strut(dynamic_row, dynamic_column_indexes)

            # Dynamic McCC and NL can't be larger than Static
            if int(dynamic['McCC']) > int(static['McCC']) or int(dynamic['NL']) > int(static['NL']):
                continue

            # if function in different lib -> skip
            # if static['longname'].split('.')[1] != dynamic['Long Name'].split('.')[1]:
            #     continue

            if static['name'] == dynamic['Name']:
                print_dynamic_row(dynamic)
                append_dynamic_metric_to_static(dynamic, 'McCC')
                append_dynamic_metric_to_static(dynamic, 'NL')
                break

            if static['line'] == dynamic['Line'] and static['column'] == dynamic['Column']:
                print_dynamic_row(dynamic)
                append_dynamic_metric_to_static(dynamic, 'McCC')
                append_dynamic_metric_to_static(dynamic, 'NL')
                break

            if static_name_in_dynamic(dynamic, static, line_threshold=0, column_threshold=5):
                print_dynamic_row(dynamic)
                append_dynamic_metric_to_static(dynamic, 'McCC')
                append_dynamic_metric_to_static(dynamic, 'NL')
                break

            if static_name_in_dynamic(dynamic, static, line_threshold=0, column_threshold=100):
                print_dynamic_row(dynamic)
                append_dynamic_metric_to_static(dynamic, 'McCC')
                append_dynamic_metric_to_static(dynamic, 'NL')
                break

            if line_column_threshold(dynamic, static, line_threshold=1, column_threshold=5):
                print_dynamic_row(dynamic)
                append_dynamic_metric_to_static(dynamic, 'McCC')
                append_dynamic_metric_to_static(dynamic, 'NL')
                break

            if line_column_threshold(dynamic, static, line_threshold=1, column_threshold=100):
                print_dynamic_row(dynamic)
                append_dynamic_metric_to_static(dynamic, 'McCC')
                append_dynamic_metric_to_static(dynamic, 'NL')
                break

            append_dynamic_colom_to_static('McCC')
            append_dynamic_colom_to_static('NL')

        # i = 0
        # print(result[i])
        # i += 1

        print_line(200, '.')

    print()
    print_line(200, '=')

    return result


def calculate_map_coverage(sheet_data):
    repo_name = sheet_data['name']

    dyn_functions_path = f'results/{repo_name}/{latest_dir(f"results/{repo_name}")}/metric/dynamic/' + 'Dynamic-Function.csv'
    if not is_exists(dyn_functions_path):
        update_note(sheet_data, 'Dynamic-Functions not found!')
        return '0%'

    dynamic_csv = read_dynamic_csv(dyn_functions_path)
    static_csv = filter_data_from_all(repo_name)

    results = merge_metric_csv(static_csv, dynamic_csv)[1]

    coverage = results['dynamic_count'] / results['static_count'] * 100

    if (results['static_count'] - results['dynamic_count']) != 0:
        update_note(sheet_data, f"Not found: {results['static_count'] - results['dynamic_count']}")
    else:
        update_note(sheet_data, "Done")
    return str(int(coverage)) + '%'


def read_dynamic_csv(dyn_functions_path):
    result = []

    with open(dyn_functions_path, 'r') as hca_dyn_func_file:
        hca_functions = hca_dyn_func_file.readlines()
        for data in hca_functions:
            row = data.split(',')
            row[-1] = row[-1].strip()
            result.append(row)

    return result


def get_date():
    return datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
