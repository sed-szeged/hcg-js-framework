import csv
import os.path
import re
from os import listdir

RESULTS_DIR = 'mapping-results'


def latest_dir(dir_path):
    #          regex       yyyy     mm   dd   hh   mm   ss
    pattern = re.compile('^\d\d\d\d-\d\d-\d\d-\d\d-\d\d-\d\d$')
    directories = []
    for f in listdir(dir_path):
        if pattern.match(f):
            directories.append(f)

    return sorted(directories, reverse=True)[0]


def read_dynamic_csv(dyn_functions_path):
    result = []

    with open(dyn_functions_path, 'r') as hca_dyn_func_file:
        hca_functions = hca_dyn_func_file.readlines()
        for data in hca_functions:
            row = data.split(',')
            row[-1] = row[-1].strip()
            result.append(row)

    return result


def merge_dynamic_results():
    directory_contents = listdir('mapping-results')

    result_path = 'machine_learning_data/dynamic-function-merged.csv'

    all_lines = 0
    print(f"{'repo_name':20}{''}")

    with open(result_path, 'w') as all_dynamic_function_merged:
        header = 'repo_name,name,longname,path,full_repo_path,line,column,endline,endcolumn,CC,CCL,CCO,CI,CLC,CLLC,' \
               'McCC,NL,NLE,CD,CLOC,DLOC,TCD,TCLOC,LLOC,LOC,NOS,NUMPAR,TLLOC,TLOC,TNOS,HOR_D,HOR_T,HON_D,HON_T,HLEN,' \
               'HVOC,HDIFF,HVOL,HEFF,HBUGS,HTIME,CYCL,PARAMS,CYCL_DENS,Vuln,Valid_vuln,Fix_hash,D_McCC,D_NL '
        print(header, file=all_dynamic_function_merged)

        for repo_name in directory_contents:
            latest = latest_dir('mapping-results/' + repo_name)

            dynamic_path = os.path.join(RESULTS_DIR, repo_name, latest) + '/' + 'Mapped-Function.csv'

            with open(dynamic_path, 'r') as mapped_function_csv:
                data = mapped_function_csv.readlines()

                line = 0

                for row in data[1:]:
                    row = row.rstrip()

                    if row[-1].isnumeric():
                        all_lines += 1
                        line += 1
                        print(row, file=all_dynamic_function_merged)

            print('[MERGER] Merging dynamic:  ' + repo_name + ' done.')
            print('[MERGER] lines:', line)
    print("[MERGER] Dynamic merged ✓️")
    print("[MERGER] Number of lines: ", all_lines)


def merge_static_results():
    directory_contents = listdir('mapping-results')

    result_path = 'machine_learning_data/static-function-merged.csv'

    with open(result_path, 'w') as all_dynamic_function_merged:
        header = 'repo_name,name,longname,path,full_repo_path,line,column,endline,endcolumn,CC,CCL,CCO,CI,CLC,CLLC,' \
               'McCC,NL,NLE,CD,CLOC,DLOC,TCD,TCLOC,LLOC,LOC,NOS,NUMPAR,TLLOC,TLOC,TNOS,HOR_D,HOR_T,HON_D,HON_T,HLEN,' \
               'HVOC,HDIFF,HVOL,HEFF,HBUGS,HTIME,CYCL,PARAMS,CYCL_DENS,Vuln,Valid_vuln,Fix_hash,D_McCC,D_NL '
        print(header, file=all_dynamic_function_merged)

        for repo_name in directory_contents:
            latest = latest_dir('mapping-results/' + repo_name)

            dynamic_path = os.path.join(RESULTS_DIR, repo_name, latest) + '/' + 'Mapped-Function.csv'

            with open(dynamic_path, 'r') as mapped_function_csv:
                data = mapped_function_csv.readlines()

                for row in data[1:]:
                    row = row.rstrip()

                    if not row[-1].isnumeric():
                        print(row, file=all_dynamic_function_merged)

            # print('[MERGER] Merging static:  ' + repo_name + ' done.')
    print("[MERGER] only static merged.")


def merge_static_and_dynamic_results():
    directory_contents = listdir('mapping-results')

    result_path = 'machine_learning_data/static-and-dynamic-function-merged.csv'

    with open(result_path, 'w') as all_dynamic_function_merged:
        header = 'repo_name,name,longname,path,full_repo_path,line,column,endline,endcolumn,CC,CCL,CCO,CI,CLC,CLLC,' \
                 'McCC,NL,NLE,CD,CLOC,DLOC,TCD,TCLOC,LLOC,LOC,NOS,NUMPAR,TLLOC,TLOC,TNOS,HOR_D,HOR_T,HON_D,HON_T,HLEN,' \
                 'HVOC,HDIFF,HVOL,HEFF,HBUGS,HTIME,CYCL,PARAMS,CYCL_DENS,Vuln,Valid_vuln,Fix_hash,D_McCC,D_NL '
        print(header, file=all_dynamic_function_merged)

        for repo_name in directory_contents:
            latest = latest_dir('mapping-results/' + repo_name)

            dynamic_path = os.path.join(RESULTS_DIR, repo_name, latest) + '/' + 'Mapped-Function.csv'

            with open(dynamic_path, 'r') as mapped_function_csv:
                data = mapped_function_csv.readlines()

                for row in data[1:]:
                    row = row.rstrip()

                    print(row, file=all_dynamic_function_merged)

            # print('[MERGER] Merging static+dynamic:  ' + repo_name + ' done.')
    print("[MERGER] static+dynamic merged.")


def merge_all():
    # merge_static_results()
    merge_dynamic_results()
    # merge_static_and_dynamic_results()


if __name__ == '__main__':
    merge_all()