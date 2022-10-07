if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',15,124,options.extend)) {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js@decorate:114:12 (IfStatement:125:100)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',
      line: 124,
      column: 100,
      end_line: 133,
      end_column: 9,
      json_path: 'traces/test-1.json',
      depth: 1
    });
    
                global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',125);Hoek.assert(type !== 'handler', 'Cannot extent handler decoration:', propertyName);
                global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',126);Hoek.assert(existing, `Cannot extend missing ${type} decoration: ${propertyName}`);
                global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',127);Hoek.assert(typeof method === 'function', `Extended ${type} decoration method must be a function: ${propertyName}`);
    
                global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',129);method = method(existing);
            }
            else {
                global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',132);Hoek.assert(existing === undefined, `${type[0].toUpperCase() + type.slice(1)} decoration already defined: ${propertyName}`);
            }
    (function(){__njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js@[Anonymous]:235:143 (ConditionalExpression:238:133)',
      type: 'ConditionalExpression',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',
      line: 237,
      column: 133,
      end_line: 237,
      end_column: 467,
      json_path: 'traces/test-1.json',
      depth: 1
    }); return false})() || global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',40,238,!options.scope)? global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',41,238,('')) : global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',42,238,(`${$1}__`))
    if (((function(){
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js@expose:228:10 (IfStatement:234:100)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',
      line: 233,
      column: 100,
      end_line: 239,
      end_column: 9,
      json_path: 'traces/test-1.json',
      depth: 1
    });
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js@expose:228:10 (LogicalExpression:234:105)',
      type: 'LogicalExpression',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',
      line: 233,
      column: 105,
      end_line: 233,
      end_column: 346,
      json_path: 'traces/test-1.json',
      depth: 2
    }); return false})() || (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',38,233,plugin[0] === '@')&&global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',39,233,options.scope !== true)))) {
    
                global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',236);plugin = plugin.replace(/^@([^/]+)\//, ($0, $1) => {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js@expose:228:10 (ArrowFunctionExpression:236:143)',
      type: 'ArrowFunctionExpression',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',
      line: 235,
      column: 143,
      end_line: 238,
      end_column: 13,
      json_path: 'traces/test-1.json',
      depth: 2
    });
    
    try {
    var __njsEntryData__ = __njsTraceEntry__({file: "/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js", name: "[Anonymous]", line: 235, args: [$0,$1]});
    
    
                    global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js', 43, 238, true); {
    var __njsTmp1420__ = ((function(){__njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js@[Anonymous]:235:143 (ConditionalExpression:238:133)',
      type: 'ConditionalExpression',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',
      line: 237,
      column: 133,
      end_line: 237,
      end_column: 467,
      json_path: 'traces/test-1.json',
      depth: 1
    }); return false})() || global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',40,238,!options.scope)? global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',41,238,('')) : global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/server.js',42,238,(`${$1}__`)));
    __njsTraceExit__({entryData: __njsEntryData__, exception: false, line: 237, returnValue: __njsTmp1420__});
    return __njsTmp1420__;
    };
                
    __njsTraceExit__({entryData: __njsEntryData__, exception: false, line: 238, returnValue: null});
    } catch(__njsEX__) {
    __njsTraceExit__({entryData: __njsEntryData__, exception: true, line: 235, returnValue: null});
    throw __njsEX__;
    }
    });
            }
    if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/config.js',2,18,result.error)) {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/config.js@exports.apply:14:107 (IfStatement:19:95)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/config.js',
      line: 18,
      column: 95,
      end_line: 20,
      end_column: 5,
      json_path: 'traces/test-1.json',
      depth: 1
    });
    
            global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/config.js',19);throw new Error(`Invalid ${type} options ${((function(){__njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/config.js@exports.apply:14:107 (ConditionalExpression:20:143)',
      type: 'ConditionalExpression',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/config.js',
      line: 19,
      column: 143,
      end_line: 19,
      end_column: 491,
      json_path: 'traces/test-1.json',
      depth: 2
    }); return false})() || global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/config.js',3,19,message.length)? global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/config.js',4,19,('(' + message.join(' ') + ')')) : global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/config.js',5,19,('')))} ${result.error.annotate()}`);
        }
    if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/route.js',100,359,this.method[0] !== '_')) {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/route.js@_assert:346:11 (IfStatement:353:99)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/route.js',
      line: 352,
      column: 99,
      end_line: 354,
      end_column: 9,
      json_path: 'traces/test-1.json',
      depth: 1
    });
    
                global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/route.js',360);message = `${message}: ${this.method.toUpperCase()} ${this.path}`;
            }
    (function(){__njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/validation.js@internals.input:103:114 (ConditionalExpression:147:122)',
      type: 'ConditionalExpression',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/validation.js',
      line: 146,
      column: 122,
      end_line: 146,
      end_column: 530,
      json_path: 'traces/test-1.json',
      depth: 1
    }); return false})() || global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/validation.js',26,148,validationError.isBoom)? global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/validation.js',27,148,(validationError)) : global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/validation.js',28,148,(Boom.badRequest(`Invalid request ${source} input`)))
    if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/toolkit.js',10,80,response === undefined)) {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/toolkit.js@execute:42:17 (IfStatement:81:100)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/toolkit.js',
      line: 80,
      column: 100,
      end_line: 82,
      end_column: 9,
      json_path: 'traces/test-1.json',
      depth: 1
    });
    
                global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/toolkit.js',81);response = Boom.badImplementation(`${method.name} method did not return a value, a promise, or throw an error`);
            }
    try {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/test/common.js@internals.hasLsof:7:20 (TryStatement:10:4)',
      type: 'TryStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/test/common.js',
      line: 9,
      column: 4,
      end_line: 14,
      end_column: 5,
      json_path: 'traces/test-1.json',
      depth: 1
    });
    
            ChildProcess.execSync(`lsof -p ${process.pid}`, { stdio: 'ignore' });
        }
        catch (err) {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/test/common.js@internals.hasLsof:7:20 (CatchClause:13:4)',
      type: 'CatchClause',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/test/common.js',
      line: 12,
      column: 4,
      end_line: 14,
      end_column: 5,
      json_path: 'traces/test-1.json',
      depth: 1
    });
    
            {
    var __njsTmp8423__ = (false);
    __njsTraceExit__({entryData: __njsEntryData__, exception: false, line: 13, returnValue: __njsTmp8423__});
    return __njsTmp8423__;
    }
        }
    if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',60,246,etag === `W/${
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (IfStatement:241:110)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 240,
      column: 110,
      end_line: 242,
      end_column: 17,
      json_path: 'traces/test-1.json',
      depth: 3
    });
    entity.etag}`)) {      // Weak comparison
                        global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',247);{
    var __njsTmp3650__ = (etag);
    __njsTraceExit__({entryData: __njsEntryData__, exception: false, line: 241, returnValue: __njsTmp3650__});
    return __njsTmp3650__;
    }
                    }
    if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',61,253,etag === etagBase + `-${
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (IfStatement:248:114)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 247,
      column: 114,
      end_line: 249,
      end_column: 21,
      json_path: 'traces/test-1.json',
      depth: 4
    });
    encoder}"`)) {
                            global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',254);{
    var __njsTmp1206__ = (true);
    __njsTraceExit__({entryData: __njsEntryData__, exception: false, line: 248, returnValue: __njsTmp1206__});
    return __njsTmp1206__;
    }
                        }
    for (const encoder of encoders) {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (ForOfStatement:247:16)',
      type: 'ForOfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 246,
      column: 16,
      end_line: 250,
      end_column: 17,
      json_path: 'traces/test-1.json',
      depth: 3
    });
    
                        global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',253);if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',61,253,etag === etagBase + `-${
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (IfStatement:248:114)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 247,
      column: 114,
      end_line: 249,
      end_column: 21,
      json_path: 'traces/test-1.json',
      depth: 4
    });
    encoder}"`)) {
                            global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',254);{
    var __njsTmp1206__ = (true);
    __njsTraceExit__({entryData: __njsEntryData__, exception: false, line: 248, returnValue: __njsTmp1206__});
    return __njsTmp1206__;
    }
                        }
                    }
    for (const etag of ifNoneMatch) {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (ForOfStatement:229:12)',
      type: 'ForOfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 228,
      column: 12,
      end_line: 251,
      end_column: 13,
      json_path: 'traces/test-1.json',
      depth: 2
    });
    
    
                    // Compare tags (https://tools.ietf.org/html/rfc7232#section-2.3.2)
    
                    global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',238);if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',58,238,etag === entity.etag)) {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (IfStatement:233:110)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 232,
      column: 110,
      end_line: 234,
      end_column: 17,
      json_path: 'traces/test-1.json',
      depth: 3
    });
                 // Strong comparison
                        global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',239);{
    var __njsTmp5192__ = (true);
    __njsTraceExit__({entryData: __njsEntryData__, exception: false, line: 233, returnValue: __njsTmp5192__});
    return __njsTmp5192__;
    }
                    }
    
                    global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',242);if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',59,242,!entity.vary)) {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (IfStatement:237:110)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 236,
      column: 110,
      end_line: 238,
      end_column: 17,
      json_path: 'traces/test-1.json',
      depth: 3
    });
    
                        global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',243);continue;
                    }
    
                    global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',246);if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',60,246,etag === `W/${
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (IfStatement:241:110)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 240,
      column: 110,
      end_line: 242,
      end_column: 17,
      json_path: 'traces/test-1.json',
      depth: 3
    });
    entity.etag}`)) {      // Weak comparison
                        global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',247);{
    var __njsTmp3650__ = (etag);
    __njsTraceExit__({entryData: __njsEntryData__, exception: false, line: 241, returnValue: __njsTmp3650__});
    return __njsTmp3650__;
    }
                    }
    
                    global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',250);const etagBase = entity.etag.slice(0, -1);
                    global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',251);const encoders = request._core.compression.encodings;
                    for (const encoder of encoders) {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (ForOfStatement:247:16)',
      type: 'ForOfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 246,
      column: 16,
      end_line: 250,
      end_column: 17,
      json_path: 'traces/test-1.json',
      depth: 3
    });
    
                        global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',253);if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',61,253,etag === etagBase + `-${
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (IfStatement:248:114)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 247,
      column: 114,
      end_line: 249,
      end_column: 21,
      json_path: 'traces/test-1.json',
      depth: 4
    });
    encoder}"`)) {
                            global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',254);{
    var __njsTmp1206__ = (true);
    __njsTraceExit__({entryData: __njsEntryData__, exception: false, line: 248, returnValue: __njsTmp1206__});
    return __njsTmp1206__;
    }
                        }
                    }
                }
    if (((function(){
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (IfStatement:226:102)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 225,
      column: 102,
      end_line: 254,
      end_column: 9,
      json_path: 'traces/test-1.json',
      depth: 1
    });
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (LogicalExpression:226:107)',
      type: 'LogicalExpression',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 225,
      column: 107,
      end_line: 225,
      end_column: 356,
      json_path: 'traces/test-1.json',
      depth: 2
    }); return false})() || (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',56,230,entity.etag)&&global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',57,230,request.headers['if-none-match'])))) {
    
                global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',233);const ifNoneMatch = request.headers['if-none-match'].split(/\s*,\s*/);
                for (const etag of ifNoneMatch) {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (ForOfStatement:229:12)',
      type: 'ForOfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 228,
      column: 12,
      end_line: 251,
      end_column: 13,
      json_path: 'traces/test-1.json',
      depth: 2
    });
    
    
                    // Compare tags (https://tools.ietf.org/html/rfc7232#section-2.3.2)
    
                    global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',238);if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',58,238,etag === entity.etag)) {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (IfStatement:233:110)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 232,
      column: 110,
      end_line: 234,
      end_column: 17,
      json_path: 'traces/test-1.json',
      depth: 3
    });
                 // Strong comparison
                        global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',239);{
    var __njsTmp5192__ = (true);
    __njsTraceExit__({entryData: __njsEntryData__, exception: false, line: 233, returnValue: __njsTmp5192__});
    return __njsTmp5192__;
    }
                    }
    
                    global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',242);if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',59,242,!entity.vary)) {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (IfStatement:237:110)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 236,
      column: 110,
      end_line: 238,
      end_column: 17,
      json_path: 'traces/test-1.json',
      depth: 3
    });
    
                        global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',243);continue;
                    }
    
                    global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',246);if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',60,246,etag === `W/${
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (IfStatement:241:110)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 240,
      column: 110,
      end_line: 242,
      end_column: 17,
      json_path: 'traces/test-1.json',
      depth: 3
    });
    entity.etag}`)) {      // Weak comparison
                        global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',247);{
    var __njsTmp3650__ = (etag);
    __njsTraceExit__({entryData: __njsEntryData__, exception: false, line: 241, returnValue: __njsTmp3650__});
    return __njsTmp3650__;
    }
                    }
    
                    global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',250);const etagBase = entity.etag.slice(0, -1);
                    global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',251);const encoders = request._core.compression.encodings;
                    for (const encoder of encoders) {
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (ForOfStatement:247:16)',
      type: 'ForOfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 246,
      column: 16,
      end_line: 250,
      end_column: 17,
      json_path: 'traces/test-1.json',
      depth: 3
    });
    
                        global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',253);if (global.__$$labCov._statement('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',61,253,etag === etagBase + `-${
    __njsOnStatement__({
      function_id: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js@unmodified:216:21 (IfStatement:248:114)',
      type: 'IfStatement',
      file_name: '/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',
      line: 247,
      column: 114,
      end_line: 249,
      end_column: 21,
      json_path: 'traces/test-1.json',
      depth: 4
    });
    encoder}"`)) {
                            global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',254);{
    var __njsTmp1206__ = (true);
    __njsTraceExit__({entryData: __njsEntryData__, exception: false, line: 248, returnValue: __njsTmp1206__});
    return __njsTmp1206__;
    }
                        }
                    }
                }
    
                global.__$$labCov._line('/workspaces/hybrid-metric-framework/node-sources/hapi/lib/response.js',259);{
    var __njsTmp9186__ = (false);
    __njsTraceExit__({entryData: __njsEntryData__, exception: false, line: 253, returnValue: __njsTmp9186__});
    return __njsTmp9186__;
    }
            }