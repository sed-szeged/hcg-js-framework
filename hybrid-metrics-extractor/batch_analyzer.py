import argparse
import os
import git
import subprocess
import re

parser = argparse.ArgumentParser(description='Batch SourceMeter runner')
parser.add_argument('project', metavar='PATH', type=str, help='Path to the project repo to be analyzed')
parser.add_argument('sm', metavar='SM_PATH', type=str, help='Path to SourceMeter')
parser.add_argument('outputDir', metavar='PATH', type=str, default="Results", help='Relative directory in which the results of the static analysis should be placed')
args = parser.parse_args()


def collect_buggy_hashes(path, sm, outputDir):
    os.chdir(path)
    repo = git.repo.Repo(path)
    tags = repo.tags
    for tag in tags:
        if re.match(r"(Bug-\d*)-fix$", str(tag)) or re.match(r"(Bug-\d*)$", str(tag)):
            print('Checking out: ' + str(tag))
            repo.git.checkout(str(tag))
            os.chdir(sm)
            print('Running SM on: ' + str(tag))
            sm_res = subprocess.run(["SourceMeterJavaScript", "-projectBaseDir:"+path, "-projectName:"+str(tag),
                                     "-resultsDir:" + outputDir, "-runESLint:false", "-runDCF:false", "-runChangeTracker:false", "-runMetricHunter:false"])
            


def main(path, sm, outputDir):
    collect_buggy_hashes(path, sm, outputDir)


if __name__ == '__main__':

    main(args.project, args.sm, args.outputDir)
