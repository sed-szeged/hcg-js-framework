var fs = require('fs');
var stringify = JSON.stringify;

/**
 * Handling all the tracing and profiling collection
 * @param {Formatter|Formatter[]} formatters - A list of formatters to use as output
 * @constructor
 */
function Tracer() {
	this.log = fs.openSync('jstrace-' + process.pid + '.txt', 'w');
	fs.writeSync(this.log, '[\n  { "id": 0, "pos": "<entry>" }');

	this.stack = [0];
	this.realStack = [];
	this.entry = true;
	this.nextId = 1;
	this.idMap = {};
	this.knownChains = {};
	this.include = undefined;
	this.exclude = undefined;

	if (process.env.CALLCHAIN_INCLUDE)
		this.include = new RegExp(process.env.CALLCHAIN_INCLUDE);
	if (process.env.CALLCHAIN_EXCLUDE)
		this.exclude = new RegExp(process.env.CALLCHAIN_EXCLUDE);
}

/**
 * Called on functions entry
 * @param {NJSTrace.functionEntryArgs} args - The event args
 * @returns {Object} An object that will be passed as argument to the onExit function
 * @protected
 */
Tracer.prototype.onEntry = function(srcInfo) {
	var id;

	if (srcInfo in this.idMap) {
		id = this.idMap[srcInfo];
	} else {
		if ((this.include && srcInfo.search(this.include) == -1)
				|| (this.exclude && srcInfo.search(this.exclude) != -1)) {
			id = -1;
		}
		else {
			id = this.nextId;
			++this.nextId;

			fs.writeSync(this.log, ',\n  { "id": ' + id + ', "pos": ' + stringify(srcInfo) + ' }');
		}
		this.idMap[srcInfo] = id;
	}

	if (id != -1) {
		this.entry = true;
		this.stack.push(id);
	}
	this.realStack.push(id);
};

/**
 * Called on functions exit
 * @param {NJSTrace.functionExitArgs} args - The event args
 * @protected
 */
Tracer.prototype.onExit = function() {
	if (this.realStack.pop() == -1) {
		return;
	}

	var stack = this.stack;

	if (this.entry) {
		var currentMap = this.knownChains;
		var length = stack.length;

		for (var i = 1; i < length; i++) {
			var value = stack[i];
			if (value in currentMap) {
				currentMap = currentMap[value];
			} else {
				var obj = {};
				currentMap[value] = obj;
				currentMap = obj;
			}
		}

		if (!currentMap.dumped) {
			var chain = ',\n  [0';
			for (var i = 1; i < length; i++) {
				chain += ', ' + stack[i];
			}

			fs.writeSync(this.log, chain + ']');
			currentMap.dumped = true;
		}
	}

	stack.pop();
	this.entry = false;
};

module.exports = Tracer;
