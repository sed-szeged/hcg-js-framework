/* njsTrace */

var Module = require('module');
var Injector = require('./lib/injector.js');
var Tracer = require('./lib/tracer.js');

function CallChain() {
}

CallChain.prototype.inject = function() {
	// Set the tracer
	var tracer = new Tracer();

	global.__ccTraceEntry__ = tracer.onEntry.bind(tracer);
	global.__ccTraceExit__ = tracer.onExit.bind(tracer);
	this.tracer = tracer;

	this.hijackCompile();
	process.argv[0] = process.argv0;
	process.execPath = process.argv0;

	return this;
};

CallChain.prototype.hijackCompile = function() {
	var self = this;
	var injector = new Injector();

	// Save a reference to the _compile function and hijack it.
	var origCompile = Module.prototype._compile;
	var origWrap = Module.wrap;
	var filename = undefined;

	Module.wrap = function(script) {
		script = origWrap(script);

		if (!filename) {
			return script;
		}

		try {
			script = injector.injectTracing(filename, script);
		} catch(error) {
		}
		filename = undefined;
		return script;
	}

	Module.prototype._compile = function(content, fname) {
		filename = fname;
		origCompile.call(this, content, fname);
	};
};

module.exports = new CallChain();
