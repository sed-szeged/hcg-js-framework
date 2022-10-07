import os.path

import generate_merged_csv as generator

from util.sys_arg_handler import *
from util.injector import *
from util.merge_json import run_merge
from util.debug_handler import log_error
from util.generate_dynamic_csv import create_dynamic_csv
from util.generate_static_csv import *
from util.generate_dynamic_callgraph_csv import *
from util.sheets import *
from util.output_handler import *
import util.acg.acg_main as acg
from util.file_handler import *
from util.callgraph_visualizator import generate_dynamic_cg_visualization
from util.path_handler import *
from util.mapper.function_mapper import map_repos

DATE = get_date()
REPO_START_TIME = 0
sheets_column = 1

try:
    sheets = Sheets('keys.json', '1eS2sJBlqjJbugbETjsD3oTYmMwLaUmJ6Y7VXxluxfVE', 'Repo with Hash', 'Hca-results-ssh')
except SheetException as e:
    sheets = None
    print(f"[SHEETS] {e}")

def _clone(repo, hash, diff_file, wd):
    print('Started checking out', repo)
    os.chdir(wd)
    cp = subprocess.call(['git', 'clone', repo])
    if cp == 0:
        os.chdir(os.path.basename(repo).replace('.git', ''))
        print('Checking out #', hash)
        subprocess.run(['git', 'checkout', '-f', hash])
        if diff_file:
            print('Applying patches...')
            subprocess.run(['git', 'apply', diff_file])


def _install_dep(module_name):
    print('Installing node dependencies for ' + module_name)
    subprocess.run(['npm', 'install', '--force'])


def run_npm_test():
    print(Colors.HEADER + Colors.OKGREEN + 'Running npm test' + Colors.ENDC)

    try:
        subprocess.check_call("npm test", shell=True)
    except Exception:
        pass


def run_static_analysis(node_module, skip_static=False):
    if skip_static:
        return

    try:
        create_static_csv(node_module)
        generator.create_all_compared_csv(node_module)
        print_done("Static")
    except Exception:
        print_check_log()
        log_error()


def run_dynamic_analysis(node_module, skip_metric=False):
    if skip_metric:
        return

    try:
        create_dynamic_csv(node_module)
        print_done("Dynamic")
    except Exception:
        print_error("Dynamic")
        print_check_log()
        log_error()


def run_dynamic_callgraph(node_module, skip_cg=False):
    if skip_cg:
        return

    try:
        if not is_exists(get_stack_json_path(node_module)):
            raise Exception("Stack json doesn't exist!")

        generate_dynamic_cg_visualization(node_module)
        generate_dyn_cg_csv(node_module)
        print_done("Callgraph")
    except Exception:
        print_error("Callgraph")
        print_check_log()
        log_error()


def run_static_callgraph(node_module, skip_static_cg=False):
    if skip_static_cg:
        return

    try:
        print(" " + Colors.CYELLOW2, end="")
        print("  Running static callgraphs...")
        print(Colors.ENDC, end="")

        acg.run(node_module)
        generator.merge_static_with_dynamic_callgraphs(node_module)
        time.sleep(1)

        delete_console_line()
        delete_console_line()
        delete_console_line()

    except Exception as e:
        print(e)

    print_done("Static Callgraph")


def get_elapsed_time(start_time, end_time):
    return end_time - start_time


def setup_repository(node_module, working_dir):
    # Clone repository & and install dependencies

    if not get_sys_args()['skip-clone']:
        _clone(node_module['repo'], node_module['hash'], None, working_dir)

    os.chdir(os.path.join(working_dir, node_module['name']))

    if not get_sys_args()['skip-npm']:
        _install_dep(node_module['name'])


def run_analyzers(node_module):
    try:
        run_dynamic_analysis(node_module, get_sys_args()['skip-metric'])
        run_dynamic_callgraph(node_module, get_sys_args()['skip-cg'])
        run_static_callgraph(node_module, get_sys_args()['skip-static-cg'])
        run_static_analysis(node_module, get_sys_args()['skip-static'])
        print_smile()
    except Exception:
        print_check_log()


def update_module_result_to_sheets(node_module, sheets_column, start_time):
    if get_sys_args()['sheets'] and sheets is not None:
        # Repository Name | Unit Testing Framework | Completed | Static cg | Dynamic cg | Where to inject | Note
        result = list(sheet_data(node_module, get_elapsed_time(start_time, time.time())).values())
        sheets.push([result], sheets_column)


def sheet_data(node_module, elapsed_time):
    _result = {
        'repo-name': ".".join(node_module['repo'].split('.')[:-1]),
        'u-framework': node_module['testing-framework'],
        'completed': is_completed(node_module),
        'time': elapsed_time,
        'static-cg': file_statistics(node_module, 'static-cg'),
        'dynamic-cg': file_statistics(node_module, 'dynamic-cg'),
        'static-metrics': file_statistics(node_module, 'static-metrics'),
        'dynamic-metrics': file_statistics(node_module, 'dynamic-metrics'),
        'inject': ', '.join(node_module['inject']),
        'note': '',
    }

    return _result


def sheet_data_running(node_module):
    _result = {
        'repo-name': ".".join(node_module['repo'].split('.')[:-1]),
        'u-framework': node_module['testing-framework'],
        'completed': "Running...",
        'time': "",
        'static-cg': "",
        'dynamic-cg': "",
        'static-metric': "",
        'dynamic-metric': "",
        'inject': ', '.join(node_module['inject']),
        'note': '',
    }

    return _result


def init_modules():
    if get_sys_args()['sheets'] and sheets is not None:
        CONF['modules'] = sheets.get_modules()


def init_sheets():
    if get_sys_args()['sheets'] and sheets is not None:
        sheets.clear("A2:J100")


def standardize_module():
    show_standardizing_module()
    subprocess.run(['standard', '--fix'])


def analyse_module(node_module, results_path, working_dir):
    # Clone & npm install
    setup_repository(node_module, working_dir)

    if get_sys_args()['init']:
        show_inited_module_info(node_module)
        return

    # Create folders to separate callgraphs and metrics
    create_results_folder_structure(node_module, results_path, DATE)

    # Start timer after clone & npm install
    global REPO_START_TIME
    REPO_START_TIME = time.time()

    # Insert a line of code to inject our njsTrace utility
    inject_njstrace(node_module['inject'], get_sys_args()['abs-path'])

    if not get_sys_args()['skip-npm-test']:
        # Delete old results
        delete_folder("traces")
        delete_file("cg-visualization.txt")

    # Standard --fix issues
    if get_sys_args()['standard']:
        standardize_module()

    # We run the program dynamically in order to generate traces
    if not get_sys_args()['skip-npm-test']:
        run_npm_test()

    # Merge trace files
    run_merge('./traces/', f"{MAIN_DIR}/results/{node_module['name']}/{DATE}/")

    # Remove the injected first line of code
    remove_njstrace(node_module['inject'])

    # Go back to root directory
    os.chdir('../../')

    # Generate callgraphs & metric results
    run_analyzers(node_module)


def process_module(node_module, results_path, sys_args, working_dir):
    show_module_info(node_module)

    if sys_args['sheets'] and sheets is not None:
        sheets.push_running([list(sheet_data_running(node_module).values())])
        global sheets_column
        sheets_column += 1
    try:
        analyse_module(node_module, results_path, working_dir)
    finally:
        update_module_result_to_sheets(node_module, sheets_column, REPO_START_TIME)


def run_hca_for_modules(sys_args):
    working_dir = os.path.abspath(CONF['working-dir'])
    results_path = os.path.abspath(CONF['results-path'])

    make_dir(results_path)

    for node_module in CONF['modules']:
        process_module(node_module, results_path, sys_args, working_dir)
