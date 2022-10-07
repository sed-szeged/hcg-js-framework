import sys

allowed_args = [
    'skip-clone',
    'skip-npm',
    'skip-metric',
    'skip-static',
    'skip-cg',
    'skip-static-cg',
    'sheets',
    'init',
    'standard',
    'abs-path',
    'map',
    'map-merge-all',
    'skip-npm-test'
]


def get_sys_args():
    """
    Returns a dictionary based on which allowed arguments were passed.
    python3 hybrid-hca-main.py skip-clone skip-npm sheets
    _result = {
        'skip-clone' : True,
        'skip-npm' : True,
        'skip-metric' : False,
        'skip-static' : False,
        'skip-cg' : False,
        'skip-static-cg' : False,
        'sheets' : True,
        'init' : False
        'standard' : False,
        'abs-path' : False
        'map' : False
        'map-merge-all' : False
    }
    """

    _result = {}

    for arg in allowed_args:
        _result[arg] = arg in sys.argv

    return _result
