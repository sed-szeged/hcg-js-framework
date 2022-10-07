from util.mapper.function_mapper_sheets import *
from util.mapper.result_generator import *
from util.mapper.function_mapper_handler import *
from util.file_handler import *


def init_result_dir():
    if not isdir(RESULTS_DIR):
        mkdir(RESULTS_DIR)


def init_repo_dir(repo_name, current_date):
    """
    Create directory with current date for the repository to be analysed
    eg: repo_name = 'mathjs'
    folder structure:
        .mapping-results
            ├──mathjs
                ├──2021-12-01-10-30-59
                ├──2021-12-02-10-31-20
                ├──2021-12-03-11-05-10
    """

    repo_path = os.path.join(RESULTS_DIR, repo_name)

    if not isdir(repo_path):
        mkdir(repo_path)

    repo_path_with_date = os.path.join(RESULTS_DIR, repo_name, current_date)
    mkdir(repo_path_with_date)


def map_repos():
    init_result_dir()

    for sheet_data in sheet_repos_data():
        current_date = get_date()

        init_repo_dir(sheet_data['name'], current_date)

        print_repo_name(sheet_data)

        generate_mapped_csv(sheet_data['name'], current_date)
        generate_dynamic_csv(sheet_data['name'], current_date)
        generate_static_csv(sheet_data['name'], current_date)

        push_to_sheets(sheet_data, calculate_map_coverage(sheet_data), current_date)
        # push_to_sheets(sheet_data, '7', current_date)


if __name__ == '__main__':
    map_repos()
