from util.mapper.function_mapper_handler import *

RESULTS_DIR = 'mapping-results'


def generate_dynamic_csv(repo_name, current_date):
    """ Filter rows from Mapped-Function.csv where has dynamic McCC / NL """
    source = os.path.join(RESULTS_DIR, repo_name, current_date) + '/' + 'Mapped-Function.csv'
    destination = os.path.join(RESULTS_DIR, repo_name, current_date) + '/' + 'Mapped_Dynamic_Function.csv'

    with open(source, 'r') as mapped_function_csv:
        with open(destination, 'w') as dynamic_function_csv:
            data = mapped_function_csv.readlines()

            data[0] = data[0].rstrip()
            print(data[0], file=dynamic_function_csv)

            for row in data[1:]:
                row = row.rstrip()

                if row[-1].isnumeric():
                    print(row, file=dynamic_function_csv)


def generate_static_csv(repo_name, current_date):
    """ Filter rows from Dynamic-Function.csv where don't have dynamic McCC / NL """
    source = os.path.join(RESULTS_DIR, repo_name, current_date) + '/' + 'Mapped-Function.csv'
    destination = os.path.join(RESULTS_DIR, repo_name, current_date) + '/' + 'Mapped_Static_Function.csv'

    with open(source, 'r') as mapped_function_csv:
        with open(destination, 'w') as static_function_csv:
            data = mapped_function_csv.readlines()

            data[0] = data[0].rstrip()
            print(data[0], file=static_function_csv)

            for row in data[1:]:
                row = row.rstrip()

                if not row[-1].isnumeric():
                    print(row, file=static_function_csv)


def map_rows(repo_name):
    dyn_functions_path = f'results/{repo_name}/{latest_dir(f"results/{repo_name}")}/metric/dynamic/' + 'Dynamic-Function.csv'

    dynamic_csv = read_dynamic_csv(dyn_functions_path)
    static_csv = filter_data_from_all(repo_name)

    return merge_metric_csv2(static_csv, dynamic_csv)


def generate_mapped_csv(repo_name, current_date):
    """ Write mapped results to csv """
    destination = os.path.join(RESULTS_DIR, repo_name, current_date) + '/Mapped-Function.csv'

    with open(destination, 'w') as out:
        mapped_rows = map_rows(repo_name)
        print(",".join(mapped_rows[0]), file=out)  # Header

        for row in mapped_rows[1:]:
            raw_row = row.values()
            raw_row = ['' if v is None else v for v in raw_row]

            print(",".join(raw_row), file=out)  # Header



