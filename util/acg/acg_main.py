import glob
import subprocess
import json
from datetime import datetime

import util.acg.jscg_convert2json as converter
import util.acg.jscg_compare_json as comparator
import util.acg.jscg_generate_venny_csv as generator
from util.file_handler import *

NODE_SOURCES_PATH = "./node-sources"
CG_DIR = 'callgraphs'
TOOLS_PATH = './util/acg/util'
RESULTS_PATH = './results/'

blacklist = ['node_modules', 'test', 'tests', 'traces']


def sort_folders_by_datetime(path, datetime_format='%Y-%m-%d-%H-%M-%S'):
    dates = []

    for folder in next(os.walk(path))[1]:
        try:
            date = datetime.strptime(folder, datetime_format)
            dates.append([date, folder])
        except ValueError:
            # Not a date
            continue

    # Sort by datetime
    return sorted(dates, key=lambda x: x[0], reverse=True)


def get_latest_result(repo_path):
    return sort_folders_by_datetime(repo_path)[0]


# Legacy
def get_module_filter(module):
    path = os.path.join(NODE_SOURCES_PATH, module['name'])

    files = os.listdir(path)

    for file in files:
        if os.path.isdir(f"{path}/{file}"):
            sub_files = glob.glob(f"{path}/{file}/*", recursive=True)

            for sub_file in sub_files:
                if os.path.isfile(sub_file) and sub_file.endswith('.js'):
                    break
            else:
                blacklist.append(file)

    module_filter = []

    for file in files:
        short_path = os.path.join(module['name'], file)
        full_path = os.path.join(NODE_SOURCES_PATH, short_path)
        extension = file.split(".")[-1]

        if file in blacklist:
            continue
        if extension != 'js' and not os.path.isdir(full_path):
            continue
        if file.startswith('.'):
            continue

        module_filter.append(short_path)

    # Sort js files to top
    module_filter.sort(key=lambda x: 1 if x.endswith('.js') and os.path.isfile(x) else 0)

    return module_filter


def _run_static(module):
    cgtxt_path = os.path.join(module['path'], module['name']+".cgtxt")
    json_path = os.path.join(module['path'], module['name']+".json")

    def _run_with_strategy(strategy):
        print('     Running ACG analysis with %s strategy' % strategy)
        with open(cgtxt_path, 'w') as cg_out:
            subprocess.run(
                ['node', os.path.join(TOOLS_PATH, 'js-callgraph', 'js-callgraph.js'), '--cg', '--v8', '--strategy',
                 strategy, '--baseDirToCut', NODE_SOURCES_PATH, module['path']], stdout=cg_out)
        converter.convert_acg_js(module['path'])
        if not os.path.exists(os.path.join(module['cg-path'], "acg-" + strategy)):
            os.mkdir(os.path.join(module['cg-path'], "acg-" + strategy))
        shutil.move(json_path, os.path.join(module['cg-path'], "acg-" + strategy, module['name'] + ".json"))

    _run_with_strategy('ONESHOT')
    _run_with_strategy('DEMAND')


def _create_final_cg(cg_path):
    def _get_conf(foundBy):
        if 'dyn-v8' in foundBy:
            return 1
        elif 'acg-demand' in foundBy and 'acg-oneshot' in foundBy:
            return 0.19
        elif 'acg-oneshot' in foundBy:
            return 0.27
        else:
            return 0.03
    for merged_cg in os.listdir(os.path.join(cg_path, 'x-compared')):
        mcg = json.load(open(os.path.join(cg_path, 'x-compared', merged_cg), 'r'))
        for node in mcg['nodes']:
            node.pop('foundBy', None)
        for link in mcg['links']:
            link['confidence'] = _get_conf(link['foundBy'])
            link.pop('foundBy', None)
        json.dump(mcg, open(os.path.join(cg_path, merged_cg), 'w'), indent = 2)


def run(module):
    try:
        for blacklisted_file in blacklist:
            move_folder(module, blacklisted_file)

        module['path'] = os.path.join(NODE_SOURCES_PATH, module['name'])
        result_path = os.path.join(RESULTS_PATH, module['name'])
        latest_result = os.path.join(result_path, get_latest_result(result_path)[1])

        module['cg-path'] = os.path.join(latest_result, 'callgraphs')

        _run_static(module)
        comparator.compare(module['cg-path'], filter_entry=True, filter_wrapper=True)
        _create_final_cg(module['cg-path'])
        generator.generate_csv(module['cg-path'])
    finally:
        for blacklisted_file in blacklist:
            restore_folder(module, blacklisted_file)
