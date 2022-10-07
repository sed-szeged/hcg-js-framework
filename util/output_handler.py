from datetime import datetime
from util.color import Colors
from CONFIG import CONF


def get_date():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def show_introduction():
    """
    Title: ----Hybrid Code Analyser----

    Version: Alpha x.xx.xx
    Starting time: yyyy-mm-dd-hh-mm-ss
    Repositories: x

    Name                 | Inject
    ----------------------------------------
    1_module-name        | 1_module-file.js, 1_module-test-folder
    2_module-name        | 2_module-file.js, 2_module-test-folder
    ...
    """

    show_title()
    show_version_number()
    show_starting_time()
    show_number_of_repositories(CONF['modules'])
    show_all_repository_name(CONF['modules'])
    print()


def show_module_info(node_module):
    """
    ─────────────────────────────
    Analysing: module-name
    """
    show_line(40)
    show_analysing_module(node_module)


def print_smile():
    print(f"\n    {Colors.CGREEN}\(• ◡ •)/{Colors.ENDC}\n")


def print_check_log():
    print(f"\n{Colors.CREDBG}Check log.txt for more information!{Colors.ENDC}\n")


def print_done(trace_type):
    print(f" {Colors.OKGREEN}✔{Colors.ENDC}{Colors.CBEIGE2} {trace_type} trace files are done! {Colors.ENDC}")


def print_error(trace_type):
    print(f" {Colors.CRED2}✘ Error in {trace_type} analysis.{Colors.ENDC}\n\n")


def show_all_repository_name(modules):
    print(f"{'Name':20} | Inject")
    [print("-", end="") for _ in range(40)]
    print()
    for module in modules:
        print(f"{module['name']:20} | {', '.join(module['inject'])}")
    print()


def show_title():
    print(Colors.BOLD + "\n----Hybrid Code Analyser----\n" + Colors.ENDC)


def show_number_of_repositories(modules):
    print(Colors.CITALIC + f"Repositories: {len(modules)}\n" + Colors.ENDC)


def show_line(length):
    [print("─", end="") for _ in range(length)]
    print()


def show_analysing_module(module):
    print(Colors.BOLD + Colors.CBLUE2 + "Analysing: ", module['name'], "\n" + Colors.ENDC)


def show_starting_time():
    now = datetime.now()

    current_time = now.strftime("%H-%M-%S")
    print(Colors.CITALIC + f"Starting at: {datetime.today().strftime('%Y-%m-%d')}-{current_time}" + Colors.ENDC)


def show_version_number():
    print(Colors.CITALIC + f"Version: {CONF['version']}" + Colors.ENDC)


def show_inited_module_info(node_module):
    print('\n' + Colors.BOLD + Colors.OKBLUE + node_module['name'] + " cloned + npm install finished!" + Colors.ENDC + "\n")


def show_standardizing_module():
    print('\n' + Colors.CBEIGE + "Running \'standard --fix\'" + Colors.ENDC + "\n")
