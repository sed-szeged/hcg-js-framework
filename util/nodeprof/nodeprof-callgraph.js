/*******************************************************************************
 * Copyright [2018] [Haiyang Sun, Università della Svizzera Italiana (USI)]
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *******************************************************************************/

// DO NOT INSTRUMENT

(function (sandbox) {
  function MyAnalysis() {
    var fs = require('fs');
    var log = fs.openSync('nptrace-' + process.pid + '.txt', 'w');
    var locationRegexp = /^\((.*):([0-9]+):([0-9]+):[0-9]+:[0-9]+\)$/;
    var knownIids = {};
    var cwd = process.cwd();

    var stringify = JSON.stringify;
    var writeSync = fs.writeSync;
    var existsSync = fs.existsSync;
    var include = undefined;
    var exclude = undefined;

    if (process.env.CALLCHAIN_INCLUDE) {
      include = new RegExp(process.env.CALLCHAIN_INCLUDE);
    }
    if (process.env.CALLCHAIN_EXCLUDE) {
      exclude = new RegExp(process.env.CALLCHAIN_EXCLUDE);
    }

    function getFileName(iid) {
      var loc;

      if (process.config.variables.graalvm) {
        // Truffle-Jalangi has unique IIDs
        loc = J$.iidToLocation(iid);
      } else {
        // Jalangi on V8/Node needs sid
        loc = J$.iidToLocation(J$.sid, iid);
      }

      loc = loc.match(locationRegexp);
      var fileName = loc[1];

      if (fileName[0] != '/') {
        var fullFileName = cwd + '/' + fileName;
        if (existsSync(fullFileName)) {
          fileName = fullFileName;
        }
      }

      if ((include && fileName.search(include) == -1) || (exclude && fileName.search(exclude) != -1)) {
        return undefined;
      }

      return fileName + ":" + loc[2] + ":" + loc[3];
    }

    writeSync(log, '[\n  { "id": 0, "pos": "<entry>" }');

    var stack = [ 0 ];
    var knownLinks = {};

    this.functionEnter = function (iid, f, dis, args) {
      id = knownIids[iid];

      if (!id) {
        var fn = getFileName(iid);

        if (fn) {
          writeSync(log, ',\n  { "id": ' + iid + ', "pos": ' + stringify(fn) + ' }');
          knownIids[iid] = 1;
        } else {
          knownIids[iid] = -1;
          return;
        }
      } else if (id === -1) {
        return;
      }

      if (stack.length > 0) {
        var from = stack[stack.length - 1];

        source = knownLinks[from];
        if (!source) {
          source = {};
          knownLinks[from] = source;
        }

        if (!(iid in source)) {
          source[iid] = true;
          writeSync(log, ',\n  [' + from + ', '  + iid + ']');
        }
      }

      stack.push(iid);
    };

    this.functionExit = function (iid, returnVal, wrappedExceptionVal) {
      if (knownIids[iid] === 1) {
        stack.pop();
      }

      return {returnVal: returnVal, wrappedExceptionVal: wrappedExceptionVal, isBacktrack: false};
    };

    this.endExecution = function () {
      /* Currently does nothing. */
    };
  }

  sandbox.analysis = new MyAnalysis();
})(J$);
