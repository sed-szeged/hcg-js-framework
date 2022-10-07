# This script is used to compare the output of the program to a predefined output.
# Found mismatches will be reported

from datetime import datetime
import os
from glob import glob
import difflib
import sys

PREFIX_TICK = '  ✓'
PREFIX_WARNING = '  !'
PREFIX_ERROR = '  X'
PREFIX_LEFT = '<--'
PREFIX_RIGHT = '-->'
PREFIX_PLUS = '  +'
PREFIX_MINUS = '  -'

# Results path
RESULTS_PATH = '../results/'

# Predefined result folder
RESULTS_PREDEFINED = 'predefined'

# Choose the latest results by date
RESULTS_COMPARE = ''


# Only needed if RESULTS_COMPARE_DATE is False
# RESULTS_COMPARE = os.path.join(RESULTS_PATH, '')

def sort_folders_by_datetime(path, datetime_format):
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
    return sort_folders_by_datetime(repo_path, '%Y-%m-%d-%H-%M-%S')[0]


def compare_file(left_file, right_file, left_slice=0, right_slice=0):
    # Open the files
    try:
        left_content = open(left_file, "r").read().splitlines()
    except OSError: 
        print('cannot open', left_file)
        return

    try:
        right_content = open(right_file, "r").read().splitlines()
    except OSError:
        print('cannot open', right_file)
        return

    difference = False

    for line in difflib.unified_diff(left_content, right_content, fromfile=left_file, tofile=right_file, lineterm=''):
        print(line)
        difference = True

    return difference


def compare_file_list(left, right, left_slice=0, right_slice=0):
    print('Running comparison')
    print('Compare from (LEFT): ', left[0][:left_slice])
    print('Compare to   (RIGHT):', right[0][:right_slice])
    print()

    left = [[path[left_slice:], path] for path in left if os.path.isfile(path)]
    right = [[path[right_slice:], path] for path in right if os.path.isfile(path)]

    files_common = []
    files_left = []
    files_right = []

    found = False

    print('    Common:')

    for left_file in left:
        try:
            right_file = next(f for f in right if f[0] == left_file[0])
        except StopIteration:
            right_file = False

        if right_file:
            found = True
            difference = compare_file(left_file[1], right_file[1], left_slice, right_slice)
            if not difference:
                print(PREFIX_TICK, left_file[0])

            files_common.append(left_file[0])
        else:
            files_left.append(left_file[0])

    if not found:
        print('  !', 'No common files found')

    for right_file in right:
        try:
            left_file = next(f for f in left if f[0] == right_file[0])
        except StopIteration:
            left_file = False

        if not left_file:
            files_right.append(right_file[0])

    print('-------------------------')
    print('    Left:')

    if len(files_left) == 0:
        print(PREFIX_TICK, 'All files on left are common')

    for left_file in files_left:
        print(PREFIX_LEFT, left_file)

    print('-------------------------')
    print('    Right:')

    if len(files_right) == 0:
        print(PREFIX_TICK, 'All files on right are common')

    for right_file in files_right:
        print(PREFIX_RIGHT, right_file)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {__file__} <repository-name>')
        exit(-1)

    repo_path = RESULTS_PATH + sys.argv[1]

    if not os.path.isdir(repo_path):
        print(f'ERROR: Repository path "{repo_path}" doesn\'t exist!')
        exit(-1)

    predefined_path = os.path.join(repo_path, RESULTS_PREDEFINED)

    if not os.path.isdir(predefined_path):
        print(f'ERROR: Predefined path "{predefined_path}" doesn\'t exist!')
        exit(-1)

    latest_path = os.path.join(repo_path, get_latest_result(repo_path)[1])

    if not os.path.isdir(latest_path):
        print('ERROR: Couldn\'t fetch latest result directory!')
        exit(-1)

    predefined = [y for x in os.walk(predefined_path) for y in glob(os.path.join(x[0], '*'))]
    latest = [y for x in os.walk(latest_path) for y in glob(os.path.join(x[0], '*'))]

    compare_file_list(predefined, latest, len(predefined_path), len(latest_path))
