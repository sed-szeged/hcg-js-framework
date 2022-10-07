import json
import os


def find_in_json_list(json_list, key, value):
    for i in range(len(json_list)):
        if json_list[i][key] == value:
            return i

    return -1


def is_statement_in_list(statement_list, statement_to_find):
    for statement in statement_list:
        if statement['start']['line'] == statement_to_find['start']['line'] and statement['start']['column'] == statement_to_find['start']['column']:
            return True

    return False


def dump_to_file(fname, json_obj):
    with open(fname, "w") as f:
        json.dump(json_obj, f, indent=4)


def absolute_file_paths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

def merge_json(json_file_list):
    merged_obj = {"functions": [], "classes": []}

    for file in json_file_list:
        size = os.path.getsize(file)

        if size == 0:
            # sometimes we have empty json files. skip those
            continue

        with open(file) as f:
            obj = json.load(f)

            if 'functions' in obj:
                # Iterate through each function in the list
                for function in obj['functions']:
                    function['parent_class'] = function['parent_class'] if 'parent_class' in function else None

                    # Check if the function_id already exists in the merged object
                    function_index = find_in_json_list(merged_obj['functions'], 'function_id', function['function_id'])

                    if function_index == -1:
                        # Add the function to the list
                        merged_obj['functions'].append(function)
                        function_index = len(merged_obj['functions']) - 1

                    merge_function = merged_obj['functions'][function_index]

                    # Iterate through each statement in the function
                    for statement in function['statements']:

                        # If statement isn't in the merged json object already, append it
                        if not is_statement_in_list(merge_function['statements'], statement):
                            merge_function['statements'].append(statement)

            if 'classes' in obj:
                for _class in obj['classes']:
                    classname = _class['name']
                    class_index = find_in_json_list(merged_obj['classes'], 'name', classname)

                    if class_index == -1:
                        # Add the class to the list
                        merged_obj['classes'].append(_class)
                        class_index = len(merged_obj['classes']) - 1 # get last item

                    merge_class = merged_obj['classes'][class_index]

                    for method in _class['methods']:
                        method['parent_class'] = method['parent_class'] if 'parent_class' in method else None

                        method_index = find_in_json_list(merge_class['methods'], 'function_id', method['function_id'])

                        if method_index == -1:
                            # Add the method to the list
                            merge_class['methods'].append(method)
                            method_index = len(merge_class['methods']) - 1

                        merge_method = merge_class['methods'][method_index]

                        # Iterate through each statement in the function
                        for statement in method['statements']:

                            # If statement isn't in the merged json object already, append it
                            if not is_statement_in_list(merge_method['statements'], statement):
                               merge_method['statements'].append(statement)

    return merged_obj

def get_class_index(classname, class_list):
    for i in range(len(class_list)):
        if class_list[i]['name'] == classname:
            return i

    return -1

def run_merge(folder, results_path):
    merged_obj = merge_json(absolute_file_paths(folder))

    if not os.path.exists(results_path):
        os.mkdir(results_path)

    if not os.path.exists(results_path + "metric/dynamic"):
        os.mkdir(results_path + "/metric/dynamic")

    functions_obj = {'functions': merged_obj['functions']}
    classes_obj = {'classes': merged_obj['classes']}

    dump_to_file(f"{results_path}metric/dynamic/function.json", functions_obj)
    dump_to_file(f"{results_path}metric/dynamic/class.json", classes_obj)
