// Note: plugins are disabled
var parse = require('./acorn.js').parse;
var Syntax = require('./syntax.js');
var stringify = JSON.stringify;

function falafel(src, opts, fn) {
    if (typeof opts === 'function') {
        fn = opts;
        opts = {};
    }
    if (src && typeof src === 'object' && src.constructor.name === 'Buffer') {
        src = src.toString();
    }
    else if (src && typeof src === 'object') {
        opts = src;
        src = opts.source;
        delete opts.source;
    }

    src = src === undefined ? opts.source : src;
    if (typeof src !== 'string') src = String(src);
    if (opts.parser) parse = opts.parser.parse;
    var ast = parse(src, opts);

    var result = {
        chunks : src.split(''),
        toString : function () { return result.chunks.join('') },
        inspect : function () { return result.toString() }
    };
    var index = 0;

    (function walk (node, parent) {
        insertHelpers(node, parent, result.chunks);

        var allKeys = Object.keys(node);
        var len = allKeys.length;

        for (var idx = 0; idx < len; idx++) {
            var key = allKeys[idx];

            if (key === 'parent') continue;

            var child = node[key];
            if (Array.isArray(child)) {
                var childLen = child.length;

                for (var childIdx = 0; childIdx < childLen; ++childIdx) {
                    var childValue = child[childIdx];

                    if (typeof childValue.type === 'string' && childValue) {
                        walk(childValue, node);
                    }
                };
            }
            else if (child && typeof child.type === 'string') {
                walk(child, node);
            }
        }
        fn(node);
    })(ast, undefined);

    return result;
};

function insertHelpers (node, parent, chunks) {
    node.parent = parent;

    node.source = function () {
        return chunks.slice(node.start, node.end).join('');
    };

    if (node.update && typeof node.update === 'object') {
        var prev = node.update;

        var allKeys = Object.keys(prev);
        var len = allKeys.length;

        for (var idx = 0; idx < len; ++idx) {
            var key = allKeys[idx];

            update[key] = prev[key];
        }
    }

    node.update = update;

    function update (s) {
        chunks[node.start] = s;
        for (var i = node.start + 1; i < node.end; i++) {
            chunks[i] = '';
        }
    }
}

function Injector() {
	this.strictRegex = /^(?:\s+|\/\/.*|\/\*[^*]*(?:\*(?!\/)[^*]*)*\*\/)*/;
	this.commentRegex = /\/\/.*|\/\*[^*]*(?:\*(?!\/)[^*]*)*\*\//g;
}

Injector.prototype.isStrict = function(code) {
	var start = this.strictRegex.exec(code)[0].length;

	var str = code.substring(start, start + 12);
	return str === '"use strict"' || str === "'use strict'";
}

Injector.prototype.updateArrowDeclaration = function(funcDec) {
	funcDec = funcDec.replace(this.commentRegex, "");
	return funcDec.substring(0, funcDec.lastIndexOf("=>") + 2);
}

Injector.prototype.injectTracing = function(filename, code) {
	var self = this;
	var output = falafel(code, {ranges: true, locations: true, ecmaVersion: 9}, function processASTNode(node) {
		// Ignore non-function nodes
		if (!node.range) {
			return;
		}

		if (node.type !== Syntax.FunctionDeclaration && node.type !== Syntax.FunctionExpression
		    && node.type !== Syntax.ArrowFunctionExpression) {
			return;
		}

		// Column starts at 0.
		var line = node.loc.start.line;
		var lineInfo = line + ':' + (node.loc.start.column + 1);

		// Separate the function declaration ("function foo") from function body ("{...}");
		var funcDec = node.source().slice(0, node.body.range[0] - node.range[0]);
		var srcInfo = stringify(filename + ':' + lineInfo);

		if (node.body.type !== Syntax.BlockStatement) {
			funcDec = self.updateArrowDeclaration(funcDec);
			node.update(funcDec + '{ try { __ccTraceEntry__(' + srcInfo + '); return (' + node.body.source() + '); } finally { __ccTraceExit__(); } }');
			return;
		}

		var origFuncBody = node.body.source();
		origFuncBody = origFuncBody.slice(1, origFuncBody.length - 1); // Remove the open and close braces "{}"

		var strictPrefix = "";
		if (self.isStrict(origFuncBody)) {
			strictPrefix = ' "use strict";';
		}

		node.update(funcDec + '{' + strictPrefix + ' try { __ccTraceEntry__(' + srcInfo + '); ' + origFuncBody + ' } finally { __ccTraceExit__(); } }');
	});

	output = output.toString();

	var strictPrefix = "";
	if (this.isStrict(output)) {
		strictPrefix = '"use strict"; ';
	}

	return strictPrefix + '__ccTraceEntry__(' + stringify(filename + ':1:1') + '); __ccTraceExit__(); ' + output;
};

module.exports = Injector;
