import subprocess
import csv
import time
from util.color import Colors
from util.spinner import Spinner
from util.file_handler import *


# generate csv in compared folder which only contains:
# Name | LongName | Path | Line | Column | McCC | NL
def filter_instruction_csv(node_module, instruction):
    working_dir = latest_dir(f"results/{node_module['name']}")

    with open(f"results/{node_module['name']}/{working_dir}/metric/static/Static-{instruction}.csv", newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',')

        with open(f"results/{node_module['name']}/{working_dir}/metric/static/Static-{instruction}-Filtered.csv", mode='w') as filtered_csv:
            writer = csv.writer(filtered_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in data:
                writer.writerow([row[1], row[2], row[5], row[6], row[7], row[18], row[19]])


# generate csv in compared folder which only contains:
# class_name | NM | WMC
def filter_class_csv(node_module):
    working_dir = latest_dir(f"results/{node_module['name']}")

    with open(f"results/{node_module['name']}/{working_dir}/metric/static/Static-Class.csv", newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',')

        with open(f"results/{node_module['name']}/{working_dir}/metric/static/Static-Class-Filtered.csv", mode='w') as filtered_csv:
            writer = csv.writer(filtered_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in data:
                writer.writerow([row[1], row[2], row[5], row[6], row[7],  row[41], row[20]])


def create_static_csv(node_module):
    working_dir = latest_dir(f"results/{node_module['name']}")

    move_folder(node_module, "node_modules")
    move_folder(node_module, "test")
    move_folder(node_module, "tests")
    move_folder(node_module, "__test__")

    # move_file(node_module, "test.js")

    try:
        print(" " + Colors.CYELLOW2, end="")
        with Spinner("Running SourceMeter"):
            # TODO : redirect stdout to log file
            subprocess.check_call(
                f"./util/SourceMeter/SourceMeterJavaScript -projectBaseDir:node-sources/{node_module['name']}/ -projectName:{node_module['name']} -resultsDir:results/{node_module['name']}/{working_dir}/metric/static",
                shell=True, stdout=subprocess.DEVNULL)
            time.sleep(3)

        print(Colors.ENDC)
        sys.stdout.write("\033[F")
    except Exception as e:
        print(Colors.ENDC)
        sys.stdout.write("\033[F")
        # TODO: log file
        print(f" {Colors.CRED2}✘ Error in static analysis.{Colors.ENDC}\n\n")
        print(e)
    finally:
        restore_folder(node_module, "node_modules")
        restore_folder(node_module, "test")
        restore_folder(node_module, "tests")
        restore_folder(node_module, "__test__")

        # restore_file(node_module, "test.js")

    dir_path = f"results/{node_module['name']}/{working_dir}/metric/static/{node_module['name']}/javascript/"

    csv_dir = latest_dir(dir_path)

    method_csv_path = dir_path + csv_dir + f"/{node_module['name']}-Method.csv"
    functions_csv_path = dir_path + csv_dir + f"/{node_module['name']}-Function.csv"
    class_csv_path = dir_path + csv_dir + f"/{node_module['name']}-Class.csv"

    Path(functions_csv_path).rename(f"results/{node_module['name']}/{working_dir}/metric/static/Static-Function.csv")
    Path(method_csv_path).rename(f"results/{node_module['name']}/{working_dir}/metric/static/Static-Method.csv")
    Path(class_csv_path).rename(f"results/{node_module['name']}/{working_dir}/metric/static/Static-Class.csv")

    shutil.rmtree(f"results/{node_module['name']}/{working_dir}/metric/static/{node_module['name']}")

    filter_instruction_csv(node_module, "Function")
    filter_instruction_csv(node_module, "Method")
    filter_class_csv(node_module)
