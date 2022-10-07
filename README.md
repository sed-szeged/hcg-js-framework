# hybrid-code-analyzer
todo: short description

To set up, do the following steps:
- Clone the repository
- Set up CONFIG.py (more on this later)
- Create a folder inside of the repo called "node-sources"
- Execute `npm install` in the root folder
- Run `hybrid-metric-main.py` using python3+

Results will be found in the "results" directory, under the given repository's name.

# Setting up CONFIG.py
This is the main configuration file, made in a JSON/dict format. You can add Git repositories here with their commit hashes for automatic cloning and testing. When the main python file is ran, these repositories will be analyzed.
These are the following options for each 'module':
- `name`: Name of the repository
- `repo`: .git link of the repository
- `hash`: Commit hash
- `inject`: List of files to inject into. This has to be the main root js file and the main testing js file!
