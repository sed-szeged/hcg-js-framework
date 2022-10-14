# The hcg-js-framework
This project implements a hybrid JavaScript call-graph framework that refines statically extracted JavaScript call-graphs with dynamic analysis. The project has been developed within the SETIT Project (2018-1.2.1-NKP-2018-00004). Project no. 2018-1.2.1-NKP-2018-00004 has been implemented with the support provided from the National Research, Development and Innovation Fund of Hungary, financed under the 2018-1.2.1-NKP funding scheme.
The connected publication can be referenced as follows:

```
@article{MTMT:31818460,
  author = {Antal, Gábor and Tóth, Zoltán Gábor and Hegedűs, Péter and Ferenc, Rudolf},
  doi = {10.3390/technologies9010003},
  title = {{Enhanced Bug Prediction in JavaScript Programs with Hybrid Call-Graph Based Invocation Metrics}},
  journal = {Technologies},
  volume = {9},
  unique-id = {31818460},
  year = {2021},
  pages = {3},
  orcid-numbers = {Tóth, Zoltán Gábor/0000-0002-2268-1877; Hegedűs, Péter/0000-0003-4592-6504; Ferenc, Rudolf/0000-0001-8897-7403}
}
```

Usage of the Framework
----------------------

The framework itself is a command line tool. The package is built up as
follows:

-   util - a folder containing the necessary tools for the framework,
    like the dynmaic and static analysis programs, helper scripts for
    handling dynamic traces, etc.

-   hybrid-metrics-extractor - a folder containing scripts for deriving
    hybrid call-graph metrics (NOI/NII) from hcg result json

-   hybrid-cg-main.py - the main script of the framework

-   jscg\_compare\_json.py - a module for merging various JSON files
    into one

-   jscg\_generate\_venny\_csv.py - a module for generating csv data
    for vizualization

-   jscg\_convert2json.py - a module for converting the different tool
    outputs to the common JSON format

-   CONFIG.py - the configuration file describing the arguments of the
    program analysis

In the CONFIG file, there should be a Python dictionary named CONF,
which contains the following:

-   modules - the description of the Node.js modules to be analyzed

    -   name - the name of the module

    -   repo - the Git repository where the sources can be found

    -   hash - the SHA hash of the commit to be analyzed

    -   filter - a set of filters to define which parts of the source
        code should be included in the analysis

    -   patch - if there is a modification to the source that should be
        applied before the analysis, list it here

-   node-orig - the path for the original, unmodified node binary
    (default: \"/usr/bin/node\")

-   js-tools - the utils directory (default: \"util\")

-   working-directed - the working directory where the sources are
    downloaded (default: \"node-sources\")

-   cg-path - the folder where the resulting call-graphs should be
    placed (default: \"callgraphs\")

To run the tool, type the following in a command line:

      python3 hybrid-cg-main.py {skip-clone}

This will run the necessary tools and produces a hybrid call-graph in
the previously discussed JSON format. If the sources need not to be
cloned from a Git repository, one can apply the \"skip-clone\"
parameter.

# Support service
You are free to use the framework on your own, however, University of Szeged, Software Engineering Department offers a support service as well in order to help the application of the framework. For details, please contact us by opening an issue or filing in a pull request.
