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
    var knownSids = {};
    var cwd = process.cwd();

    var stringify = JSON.stringify;
    var writeSync = fs.writeSync;
    var existsSync = fs.existsSync;
    var nextId = 0;

    function getFileName(iid, isFunc) {
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

      if (loc[2] == 1) {
        var column = +loc[3];
        column += 1;
        if (isFunc) {
          column += 61;
        }
        loc[3] = column;
      }

      return loc[1] + ":" + loc[2] + ":" + loc[3];
    }

    writeSync(log, '[\n  { "id": 0, "pos": "<entry>" }');

    var stack = [ 0 ];
    var knownLinks = {};

    function enter(iid, isFunc) {
      var sid = knownSids[J$.sid];

      if (sid === undefined) {
        sid = {};
        knownSids[J$.sid] = sid;
      }

      var id = sid[iid];

      if (id === undefined) {
        id = ++nextId;
        sid[iid] = id;

        var fn = getFileName(iid, isFunc);
        writeSync(log, ',\n  { "id": ' + id + ', "pos": ' + stringify(fn) + ' }');
      }

      if (stack.length > 0) {
        var from = stack[stack.length - 1];

        source = knownLinks[from];
        if (!source) {
          source = {};
          knownLinks[from] = source;
        }

        if (!(id in source)) {
          source[id] = true;
          writeSync(log, ',\n  [' + from + ', '  + id + ']');
        }
      }

      stack.push(id);
    }

    this.functionEnter = function (iid, f, dis, args) {
      enter(iid, true);
    };

    this.functionExit = function (iid, returnVal, wrappedExceptionVal) {
      stack.pop();
      return {returnVal: returnVal, wrappedExceptionVal: wrappedExceptionVal, isBacktrack: false};
    };

    this.scriptEnter = function (iid, instrumentedFileName, originalFileName) {
      enter(iid, false);
    }

    this.scriptExit = function (iid, wrappedExceptionVal) {
      stack.pop();
    }

    this.endExecution = function () {
      /* Currently does nothing. */
    };
  }

  sandbox.analysis = new MyAnalysis();
})(J$);
