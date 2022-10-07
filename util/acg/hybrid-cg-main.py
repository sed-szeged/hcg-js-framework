import sys
import os
import subprocess
import shutil
import json
import jscg_convert2json as converter
import jscg_compare_json as comparator
import jscg_generate_venny_csv as generator
from CONFIG import CONF

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
    subprocess.run(['npm', 'install'])
    
def _change_path(json_file, path_part):
    jf = json.load(open(json_file, 'r'))
    for node in jf['nodes']:
        node['pos'] = node['pos'].replace(path_part + '/', '')        
    json.dump(jf, open(json_file, 'w'), indent = 2)
    
def _run_static(tools_dir, filter, cg_path, module_name, wd):
    def _run_with_strategy(strategy):
        print('     Running ACG analysis with %s strategy' % strategy)
        with open(module_name + '.cgtxt', 'w') as cg_out:
            subprocess.run(['node', os.path.join(tools_dir, 'js-callgraph', 'js-callgraph.js'), '--cg', '--v8', '--strategy', strategy, '--baseDirToCut', wd, os.path.join(wd, filter[0])], stdout=cg_out)
        converter.convert_acg_js(os.path.join(wd, module_name))
        if not os.path.exists(os.path.join(cg_path, "acg-" + strategy)):
            os.mkdir(os.path.join(cg_path, "acg-" + strategy))
        shutil.move(module_name + ".json", os.path.join(cg_path, "acg-" + strategy, module_name + ".json"))        
        
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

def main(skip_clone=False):
    wd = os.path.abspath(CONF['working-dir'])
    td = os.path.abspath(CONF['js-tools'])
    node_cg = os.path.dirname(os.path.join(td, 'node'))
    node_bin = os.path.abspath(CONF['node-orig'])
    cg_path = os.path.abspath(CONF['cg-path'])
    cwd = os.getcwd()
    diff_file = None
    for node_module in CONF['modules']:
        if not skip_clone:
            if node_module['patch']:
                diff_file = os.path.abspath(os.path.join(cwd, node_module['patch']))
            _clone(node_module['repo'], node_module['hash'], diff_file, wd)
            diff_file = None
            _install_dep(node_module['name'])
        else:
            os.chdir(os.path.join(wd, node_module['name']))
        _run_static(td, node_module['filter'], cg_path, node_module['name'], wd)
        os.chdir(cwd)
    comparator.compare(filter_entry=True, filter_wrapper=True)
    _create_final_cg(cg_path)
    generator.generate_csv()

if __name__ == '__main__':
    main('skip-clone' in sys.argv)
