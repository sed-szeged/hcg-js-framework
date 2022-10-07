import sys
import traceback

# 0 - no debug
# 1 - basic
# 2 - medium
# 3 - extreme
DEBUG_LEVEL = 0

# default location: log.txt
LOG_TO_FILE = False


def dprint_basic(string, *args, **kwargs):
    dprint(1, string, *args, **kwargs)


def dprint_medium(string, *args, **kwargs):
    dprint(2, string, *args, **kwargs)


def dprint_extreme(string, *args, **kwargs):
    dprint(3, string, *args, **kwargs)


def dprint(debug_level, string, *args, **kwargs):
    if debug_level <= DEBUG_LEVEL:
        print(string, *args, **kwargs)


def log_error():
    if LOG_TO_FILE:
        with open("log.txt", "w") as log:
            traceback.print_exc(file=log)
    else:
        traceback.print_exc(file=sys.stdout)
