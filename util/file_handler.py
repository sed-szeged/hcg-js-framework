from datetime import datetime
import os
import re
import shutil
import sys
from pathlib import Path
from os import listdir


def get_date():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


# TODO: move folders and files (.js)
def move_folder(module, folder):
    source_dir = f"node-sources/{module['name']}/{folder}"
    target_dir = f"temp-{folder}"

    if not os.path.exists(source_dir):
        return

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    else:
        shutil.rmtree(target_dir)
        os.mkdir(target_dir)

    file_names = os.listdir(source_dir)

    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)


def restore_folder(node_module, folder):
    source_dir = f"temp-{folder}"
    target_dir = f"node-sources/{node_module['name']}/{folder}"

    if not os.path.exists(source_dir):
        return

    file_names = os.listdir(source_dir)

    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)

    shutil.rmtree(source_dir)


def move_file(node_module, file_name):
    source_file = f"node-sources/{node_module['name']}/" + file_name
    target_dir = f"temp-file/"

    if not os.path.exists(source_file):
        return

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    else:
        shutil.rmtree(target_dir)
        os.mkdir(target_dir)

    shutil.move(source_file, target_dir)


def restore_file(node_module, file_name):
    target_dir = f"node-sources/{node_module['name']}/"
    source_dir = f"temp-file/"
    source_file = f"temp-file/" + file_name

    if not os.path.exists(source_file):
        print("File not found: temp-file/" + file_name)
        print("Error: could not restore: " + file_name)
        return

    shutil.move(source_file, target_dir)
    shutil.rmtree(source_dir)


def is_completed(node_module):
    result_lines = [
        file_statistics(node_module, 'static-cg'),
        file_statistics(node_module, 'dynamic-cg'),
        file_statistics(node_module, 'static-metrics'),
        file_statistics(node_module, 'dynamic-metrics'),
    ]

    for lines in result_lines:
        if type(lines) == str or lines < 1:
            return "Error"

    return "Yes"


def create_results_folder_structure(node_module, results_path, DATE):
    # create folder for repository
    make_dir(f"{results_path}/{node_module['name']}")
    make_dir(f"{results_path}/{node_module['name']}/{DATE}/")
    make_dir(f"{results_path}/{node_module['name']}/{DATE}/metric/")
    make_dir(f"{results_path}/{node_module['name']}/{DATE}/metric/dynamic")
    make_dir(f"{results_path}/{node_module['name']}/{DATE}/callgraphs/")
    make_dir(f"{results_path}/{node_module['name']}/{DATE}/callgraphs/dynamic/")


def latest_dir(dir_path):
    #          regex       yyyy     mm   dd   hh   mm   ss
    pattern = re.compile('^\d\d\d\d-\d\d-\d\d-\d\d-\d\d-\d\d$')
    directories = []
    for f in listdir(dir_path):
        if pattern.match(f):
            directories.append(f)

    return sorted(directories, reverse=True)[0]


def delete_folder(folder):
    if os.path.isdir(folder):
        shutil.rmtree(folder)


def is_exists(path):
    return os.path.isfile(path)


def mkdir(path):
    # creates dir
    os.mkdir(path)


def isdir(directory_path):
    # checks whether the given directory is exists
    return os.path.isdir(directory_path)


def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def file_statistics(node_module, analysis):
    try:
        result_path = f"results/{node_module['name']}"
        base_path = f"{result_path}/{latest_dir(result_path)}/"

        paths = {
            "static-cg": "callgraphs/x-compared/merged.csv",
            "dynamic-cg": "callgraphs/dynamic/dyn-cg.csv",
            "static-metrics": "metric/static/Static-Function.csv",
            "dynamic-metrics": "metric/dynamic/Dynamic-Function.csv"
        }

        full_path = base_path + paths[analysis]

        return number_of_lines(full_path)
    except Exception:
        return "!FLS"


def number_of_lines(_path):
    if not os.path.isfile(_path):
        return "No"

    else:
        with open(_path, "r") as csv:
            lines = [line for line in csv.readlines()]
            return len(lines) - 1 if len(lines) - 1 != 0 else "Empty"


def delete_console_line():
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")


def create_folder(name):
    os.mkdir(name)
