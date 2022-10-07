import json
import requests
from util.sheets import *


def write_to_json(path, values):
    with open(path, "w") as _file:
        json.dump(values, _file, indent=4)


def make_config_from_file(path):
    with open("repositories.txt") as _file:
        repos = [repo.split("\t") for repo in _file.read().splitlines()]

    CONFIG = {
        "modules": [

        ]
    }

    def exists(file):
        return requests.get(f'{repo[0]}/blob/master/{file}').status_code == 200

    for repo in repos:
        name = repo[0].split("/")[-2]

        if exists("test"):
            test_folder = "test/**"
        elif exists("tests"):
            test_folder = "tests/**"
        else:
            test_folder = "no-test-folder"

        module = {
            "name": name,
            "test-framework": repo[1],
            "repo": repo[0][:-1] + ".git",
            "hash": "-",
            "inject": [
                "index.js" if exists("index.js") else "no-index.js",
                test_folder
            ]
        }
        CONFIG['modules'].append(module)

        print(f"{name:10}", f"{repo[0]:40}", "generated :)")

    with open("../config/ALL-CONFIG-UTEST.json", "w") as _file:
        json.dump(CONFIG, _file, indent=4)


def get_config_from_sheets():
    modules = get_modules_from_sheets()

    return modules
    # write_to_json("sheets-config.json", modules)
