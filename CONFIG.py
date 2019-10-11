CONF = {
    "modules": [
        {
            "name": "hessian.js",
            "repo": "https://github.com/BugsJS/hessian.js.git",
            "hash": "3f0b392c58a9b5e65915eca55bc209439ba1e3db",
            "filter": ["hessian.js/lib"],
            "patch": ""
        },
        {
            "name": "hexo",
            "repo": "https://github.com/BugsJS/hexo.git",
            "hash": "e6cac927b2a116b67bc4d4f51b145a8cce467110",
            "filter": ["hexo/lib"],
            "patch": "patches/hexo.diff"
        },
        {
            "name": "express",
            "repo": "https://github.com/BugsJS/express.git",
            "hash": "dc538f6e810bd462c98ee7e6aae24c64d4b1da93",
            "filter": ["express/lib"],
            "patch": ""
        }
    ],
    "node-orig": "/usr/bin/node",
    "js-tools": "util",
    "working-dir": "node-sources",
    "cg-path": "callgraphs"
}