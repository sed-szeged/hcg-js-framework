from util.color import Colors


def print_repo_name(sheet_data):
    print(Colors.CBLACKBG + Colors.CBOLD + Colors.CBLUE + '\nMapping: ' + sheet_data['name'] + Colors.ENDC + '\n')


def print_line(size, char):
    [print(char, end="") for _ in range(size)]
    print()


def print_dynamic_row(dynamic):
    print(f"{'+Name':<5} | {'':30} | {dynamic['Name']:50} | {dynamic['Long Name']:50} | {dynamic['Line']:10} |"
          f" {dynamic['Column']:10} | {dynamic['McCC']:10} | {dynamic['NL']:10}")


def print_static_functions():
    pass


def print_dynamic_functions(dyn_functions_path):
    print(Colors.BOLD + Colors.CVIOLET2 + "Dynamic functions:" + Colors.ENDC)
    print_line(200, '.')
    with open(dyn_functions_path, 'r') as hca_dyn_func_file:
        hca_functions = hca_dyn_func_file.readlines()
        i = 1
        for data in hca_functions:
            row = data.split(',')
            row[-1] = row[-1].strip()
            print(
                f"{str(i) + '.':<5} | {row[0]:30} | {row[1]:50} | {row[3]:20} | {row[4]:10} | {row[5]:10} | {row[6]:10}")
            i += 1