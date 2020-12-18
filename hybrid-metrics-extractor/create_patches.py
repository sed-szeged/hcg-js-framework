import argparse
import os
import git
import subprocess
import re


parser = argparse.ArgumentParser(description='Patch creator')
parser.add_argument('project', metavar='PATH', type=str, help='Path to the project repo to be analyzed')
parser.add_argument('outputDir', metavar='PATH', type=str, default="patches", help='Relative directory in which the patches should be placed')
args = parser.parse_args()


def main(path, outputDir):
    repo = git.repo.Repo(path)
    tags = repo.tags
    for tag in tags:
        if re.match(r"(Bug-\d*)$", str(tag)):
            res = repo.git.diff(str(tag)+".."+str(tag) + "-fix")
            f = open(os.path.join(os.getcwd(), outputDir, str(tag) + ".patch"), "a")
            f.write(res)
            f.close()


if __name__ == '__main__':

    main(args.project, args.outputDir)
