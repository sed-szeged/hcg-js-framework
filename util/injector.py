import os
import glob
from util.debug_handler import dprint

MAIN_DIR = os.getcwd()
NJSTRACE_PATH = "/util/njsTrace"
INJECT_STRING = f"require('{MAIN_DIR}{NJSTRACE_PATH}').inject()"


def get_inject_string(current_path, abs_path=False):
    root_path = MAIN_DIR + NJSTRACE_PATH

    if abs_path:
        return f"require('{root_path}').inject()"

    rel_path = os.path.relpath(root_path, current_path)
    return f"require('{rel_path}').inject()"


def _prepend_line(file_name, line):
    """ Insert given string as a new line at the beginning of a file """
    # define name of temporary dummy file
    dummy_file = file_name + '.bak'
    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)


def _needs_semicolon(lines):
    for line in lines:
        if line.endswith(";"):
            return True

    return False


def _remove_line(file_name, str_to_find, substring=False):
    with open(file_name, 'r') as fin:
        data = fin.read().splitlines(True)

    try:
        if substring:
            to_remove = []
            for line in data:
                if str_to_find in line:
                    to_remove.append(line)

            for line in to_remove:
                data.remove(line)
        else:
            if str_to_find in data:
                data.remove(str_to_find)
            elif str_to_find + "\n" in data:
                data.remove(str_to_find + "\n")

    except Exception:
        return False

    with open(file_name, 'w') as fout:
        fout.writelines(data)

    return True


# Remove hashbang comment if it exists. They cause problems
def _remove_hashbang(file_name):
    with open(file_name, 'r') as fin:
        data = fin.read().splitlines(True)

    if data[0].startswith('#!/'):
        _remove_line(file_name, data[0])
        return data[0]

    return None

def _remove_usestrict(file_name):
    with open(file_name, 'r') as fin:
        data = fin.read().splitlines(True)

    for line in data:
        if line.startswith('\'use strict\''):
            _remove_line(file_name, line)
            return line

    return None

def remove_njstrace(file_list):
    for file in file_list:
        if os.path.isfile(file) and file.endswith(".js"):
            with open(file) as myFile:
                lines = myFile.read().split()

            if len(lines) < 1:
                dprint(2, f"{file} is an empty file. skipping...")
                continue

            if _remove_line(file, "njsTrace').inject()", substring=True):
                dprint(2, f"Tracer removed from {file}")
            else:
                dprint(2, f"Nothing to remove! from {file}")

        elif os.path.isdir(file):
            remove_njstrace(glob.glob(os.path.join(file, '*')))
        else:
            # This might be a wildcard entry
            for c in ["*", "?", "["]:
                if c in file:
                    wildcard_list = glob.glob(file)
                    if len(wildcard_list) > 0:
                        # Recursively inject into all found wildcard entries
                        remove_njstrace(wildcard_list)
                        break
            else:
                if file.endswith(".js"):
                    # this is not a directory & it doesn't exist
                    print(f"error: {file} not exist")


def find_substring(list, substring):
    for item in list:
        if substring in item:
            return True
    return False


def inject_njstrace(file_list, abs_path=False):
    for file in file_list:

        if os.path.exists(file) and os.path.isfile(file) and file.endswith(".js"):
            path = os.path.dirname(os.path.abspath(file))

            with open(file) as myFile:
                content = myFile.read()
                lines = content.splitlines()

            if len(lines) < 1:
                dprint(2, f"{file} is an empty file. skipping...")
                continue

            already_injected = "njsTrace').inject()" in content

            # If inject string isn't among the lines
            if not already_injected:
                # Remove hashbang and 'use strict' lines, then prepend them later
                prepend_hashbang = _remove_hashbang(file)
                prepend_usestrict = _remove_usestrict(file)

                to_prepend = ""
                if prepend_hashbang != None:
                    to_prepend += prepend_hashbang + '\n'
                if prepend_usestrict != None:
                    to_prepend += prepend_usestrict + '\n'

                to_prepend += get_inject_string(path, abs_path)

                if _needs_semicolon(lines):
                    to_prepend += ";"

                _prepend_line(file, to_prepend)
                dprint(3, f"Tracer injected into {file}!")
            else:
                dprint(3, f"Tracer already injected into {file}!")
                pass
        elif os.path.isdir(file):
            inject_njstrace(glob.glob(os.path.join(file, '*')), abs_path)
        else:
            # This might be a wildcard entry
            for c in ["*", "?", "["]:
                if c in file:
                    wildcard_list = glob.glob(file)
                    if len(wildcard_list) > 0:
                        # Recursively inject into all found wildcard entries
                        inject_njstrace(wildcard_list, abs_path)
                        break
            else:
                if file.endswith(".js"):
                    # this is not a directory & it doesn't exist
                    print(f"error: {file} not exist")
