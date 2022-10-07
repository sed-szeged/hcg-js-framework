from util.hca_handler import *


def main(sys_args):
    if get_sys_args()['map']:
        map_repos()
        return

    if get_sys_args()['map-merge-all']:
        from util.mapper.result_merger import merge_all
        merge_all()
        return

    init_modules()
    init_sheets()

    show_introduction()

    run_hca_for_modules(sys_args)


if __name__ == '__main__':
    main(get_sys_args())
