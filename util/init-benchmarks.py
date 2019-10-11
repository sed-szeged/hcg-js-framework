#!/usr/bin/env python3

import os
import subprocess

benchmarks_filename = "benchmarks.txt"

benchmarks = [
  ["https://github.com/babel/babel.git",                "0d9eef475072ddd6fe371cbbfc2faa1270b3087a"],
  ["https://github.com/badges/shields",                 "04290e890bcbb27264a69f6693fa27ec4cb69359"],
  ["https://github.com/bower/bower",                    "e8b94ecbd07376996eb0bea6cb30c20deb7e89b6"],
  ["https://github.com/capaj/Moonridge.git",            "cc8119d1b7f278d59e8a114b9fa8ad34a4228c3e"],
  ["https://github.com/emberjs/ember.js.git",           "faf7f6366242865a3a30e789095848760f29b8b5"],
  ["https://github.com/eslint/doctrine.git",            "36ed02794b7d65339366f77a6f90892eadeee6cf"],
  ["https://github.com/eslint/eslint.git",              "e51868d8efdfecdfa8e7593b501ff7f06f00dafa"],
  ["https://github.com/expressjs/express",              "451ee5d9c17b8abd6859b939a5edfa083a61127d"],
  ["https://github.com/fullcalendar/fullcalendar.git",  "c59e5d49daaf1b207d2605b885317c60804348d8"],
  ["https://github.com/JSBenchmark/hexo.git",           "0b26940f7e0a35f6937b944012468bbf0d844010"],
  ["https://github.com/jshint/jshint.git",              "274d2be164b11899006d6df308c19a472f7e4809"],
  ["https://github.com/karma-runner/karma",             "6742ecfbc9501a454430cbb3b814be28f459cb38"],
  ["https://github.com/node-modules/hessian.js",        "3f0b392c58a9b5e65915eca55bc209439ba1e3db"],
  ["https://github.com/NodeRedis/node_redis",           "23ef1e7afadd6022526860d22ac0a7f78495106d"],
  ["https://github.com/pencilblue/pencilblue",          "522def1148a159d5f46d8361a5558149ced6c924"],
  ["https://github.com/request/request.git",            "8162961dfdb73dc35a5a4bfeefb858c2ed2ccbb7"],
  ["https://github.com/Unitech/pm2.git",                "8bfdc31c7b3490229a51efd111774095a0a9b29c"],
  ["https://github.com/visionmedia/debug.git",          "22f993216dcdcee07eb0601ea71a917e4925a30a"]
]

def init_bench(url, hash):
  name = url[url.rfind("/")+1:].replace(".git","")

  if not os.path.isdir(name):
    print("Cloning " + name + " repository from " + url)
    p = subprocess.Popen(['git', 'clone', url, name], stdout=subprocess.PIPE)
    out, err = p.communicate()

  p = subprocess.Popen(['git', '-C', name, 'config', '--get', 'remote.origin.url'], stdout=subprocess.PIPE)
  old_url = str(p.communicate()[0].split()[0], 'utf-8')

  p = subprocess.Popen(['git', '-C', name, 'rev-parse', 'HEAD'], stdout=subprocess.PIPE)
  old_hash = str(p.communicate()[0].split()[0], 'utf-8')

  if old_url != url:
    print("Reset "+name+" URL (from "+old_url+" to "+url+")")
    p = subprocess.Popen(['git', '-C', name, 'remote', 'set-url', 'origin', url], stdout=subprocess.PIPE)
    p.communicate()
    p = subprocess.Popen(['git', '-C', name, 'fetch'], stdout=subprocess.PIPE)
    p.communicate()

  if old_hash != hash:
    print("Reset "+name+" hash (from "+old_hash+" to "+hash+")")
    p = subprocess.Popen(['git', '-C', name, 'fetch'], stdout=subprocess.PIPE)
    p.communicate()
    p = subprocess.Popen(['git', '-C', name, 'reset', '--hard', hash], stdout=subprocess.PIPE)
    p.communicate()

  print(name + " is done.")

def next_bench():
  for i in range(0, len(benchmarks)):
    yield benchmarks[i]

def try_load_benchmarks():
  global benchmarks
  try:
    with open(benchmarks_filename, 'r') as f:
      print("Loading benchmarks from '%s' file..." % (benchmarks_filename))
      benchmarks = []
      for line in f:
        data = line.split()
        if len(data) == 3 and data[1] in [',', ';', '-']:
          data = [data[0], data[2]]
        if len(data) == 2 and data[0].startswith('http'):
          benchmarks.append(data)
  except:
    print("Using built-in benchmarks")
    pass

if __name__ == "__main__":
  try_load_benchmarks()
  for i in range(0, len(benchmarks)):
    init_bench(benchmarks[i][0], benchmarks[i][1])
