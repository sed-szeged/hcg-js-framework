// let sprintf=require("sprintf-js").sprintf;
//						   S	   P        FN    L      C      EL    EC
// console.log(sprintf("%-12s | %-20s | %-40s | %-9s | %-3s | %-8s | %s |",
// 	"Statement", "Function Name", "Path", "Line", "Column", "EndLine", "EndColumn"));
// console.log("――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――");

const Syntax = require('./syntax.js');
const util = require('util');
const fs = require('fs');
const jsonHandler = require('./jsonhandler.js');

function initJSONHandler() {
	if (!fs.existsSync('./traces/')) {fs.mkdirSync('./traces');}
	let jsonPath = 'traces/' + 'test-' +  getTraceId('./traces/test-');

	var jsonObj = jsonHandler.getJSON(jsonPath);
	jsonObj.obj.functions = [];
	jsonObj.obj.classes = [];

	return jsonObj;
}

/**
 * Grabs the first part of an if, while, for statement <br>
 * 	example statement: if ( (j === 1) && (i === 0) ) test(); <br>
 * 	returns: 		  if ( (j === 1) && (i === 0) )
 * @param statement
 * @returns {string}
 */
function getStatement(statement) {
	let endIndex = getStatementEndIndex(statement);

	return statement.substr(0, endIndex);
}

/**
 * Finds a character in a string, while ignoring text inside quotation marks
 * @param text The text to search in
 * @param toFind The character to find
 * @returns {int} The index of the found character
 */
function getIndexIgnoreQuotation(text, toFind) {
	// TODO: improve quotation finding algorithm
	let foundIndex = -1;
	let stringMode = 'no'; // Are we currently in a string?

	for (let i = 0; i < text.length; i++) {
		let c = text[i];

		switch (c) {
			case '\'':
				if (stringMode === 'no') {
					stringMode = '\'';
				} else if (stringMode === '\'') {
					stringMode = 'no';
				}
				break;
			case '"':
				if (stringMode === 'no') {
					stringMode = '"';
				} else if (stringMode === '"') {
					stringMode = 'no';
				}
				break;
			case toFind:
				if (stringMode === 'no') {
					foundIndex = i;
				}
				break;
		}

		if (foundIndex !== -1) {
			break;
		}
	}

	return foundIndex;
}

/**
 * Get the end index of a statement
 * @param statement
 * @returns {int}
 */
function getStatementEndIndex(statement) {
	let depth = -1;
	let stringMode = 'no'; // are we currently in a string?

	for (let i = 0; i < statement.length; i++) {
		let c = statement[i];

		switch (c) {
			case '\'':
				if (stringMode === 'no') {
					stringMode = '\'';
				} else if (stringMode === '\'') {
					stringMode = 'no';
				}
				break;
			case '"':
				if (stringMode === 'no') {
					stringMode = '"';
				} else if (stringMode === '"') {
					stringMode = 'no';
				}
				break;
			case '(':
				if (stringMode !== 'no') {break;}
				if (depth === -1) {depth = 1;} else {depth++;}
				break;
			case ')':
				if (stringMode !== 'no') {break;}
				depth--;
				break;
			case '{':
				if (stringMode !== 'no') {break;}
				// Opening block before statement even began: no parentheses!
				if (depth === -1) {return 0;}
				break;
		}

		if (depth === 0) {return i + 1;}
	}

	return 0;
}

// TODO Refactor: duplicate lines
function getBlock(statement) {
	let depth = -1;
	let out = '';
	let stringMode = 'no'; // are we currently in a string?

	for (let i = 0; i < statement.length; i++) {
		let c = statement[i];
		out += c;
		switch (c) {
			case '\'':
				if (stringMode === 'no') {
					stringMode = '\'';
				} else if (stringMode === '\'') {
					stringMode = 'no';
				}
				break;
			case '"':
				if (stringMode === 'no') {
					stringMode = '"';
				} else if (stringMode === '"') {
					stringMode = 'no';
				}
				break;
			case '{':
				if (stringMode !== 'no') {break;}
				if (depth === -1) {depth = 1;} else {depth++;}
				break;
			case '}':
				if (stringMode !== 'no') {break;}
				depth--;
				break;
		}

		if (depth === 0) {break;}
	}

	return out;
}

// TODO: refactor duplicate lines
function getFunctionId(node, self, filename, getNode=false) {
	if (node.type === Syntax.FunctionDeclaration || node.type === Syntax.FunctionExpression) {
		if(getNode) {
			return node;
		}

		let functionName = self.getFunctionName(node);
		return formatFunctionId(filename, functionName, node.loc.start.line - 1, node.loc.start.column);
	}

	let currentNode = node;
	while (currentNode.parent !== undefined) {
		currentNode = currentNode.parent;
		let functionName = self.getFunctionName(currentNode);
		if (functionName) {
			if(getNode) {
				return currentNode;
			}

			// /home/wolf/Ceges/McBaby/example_lib.js@main:2:5
			return formatFunctionId(filename, functionName, currentNode.loc.start.line - 1, currentNode.loc.start.column);
		}
	}
}

function dumpFunctionSource(node, self, filename) {
	let currentNode = getFunctionId(node, self, filename, true);
	fs.writeFileSync('/workspaces/hybrid-metric-framework/temp/functionsource' + Math.floor(Math.random() * 10000) + '.js', currentNode.source());
}

function dumpFileSource(node, filename=undefined) {
	let currentNode = node;
	while (currentNode.parent !== undefined) {
		currentNode = currentNode.parent;
	}

	if (filename) {
		filename = '/home/user/hca-js-framework/temp/files/' + filename.split('/').pop();
	} else {
		filename = '/home/user/hca-js-framework/temp/filesource.js';
	}

	fs.writeFileSync(filename, currentNode.source());
}

function getParentClass(node) {
	let currentNode = getParentClassNode(node);
	if (currentNode) {
		return joinSuperClasses(currentNode);
	}

	return undefined;
}

function getParentClassNode(node) {
	let currentNode = node;
	while (currentNode.parent !== undefined) {
		currentNode = currentNode.parent;
		if (currentNode.type === Syntax.ClassDeclaration) {
			return currentNode;
		}
	}
}

function joinSuperClasses(node) {
	let currentNode = node;
	let out = '';
	while (currentNode !== undefined && currentNode !== null) {
		let append;
		if (currentNode.id) {
			append = currentNode.id.name;
		} else if (currentNode.name) {
			append = currentNode.name;
		} else {
			append = '[Anonymous]';
		}

		out = append + ':' + out;

		currentNode = currentNode.superClass;
	}

	// Remove last colon
	return out.slice(0, out.length - 1);
}

// TODO: refactor duplicate lines
function getNodeDepth(node, self) {
	let depth = 1;
	let prevNode;
	let currentNode = node;
	while (currentNode.parent !== undefined) {
		prevNode = currentNode;
		currentNode = currentNode.parent;

		if (currentNode.type !== Syntax.BlockStatement) {
			// Exclude some depth counting, because 'else-if's and 'catch clause's seem
			// to be embedded into their 'if' and 'try' statements, respectively

			// IfStatement nodes have an alternate property if they have an else block.
			/* if (currentNode.alternate && currentNode.alternate === prevNode) {
				continue;
			} */

			// TryStatement nodes have a handler property if they have a catch clause
			if (currentNode.handler && currentNode.handler === prevNode) {
				continue;
			}

			// TryStatement nodes have a finalizer property if they have a try clause
			if (currentNode.finalizer && currentNode.finalizer === prevNode) {
				continue;
			}

			// If this node isn't relevant for us, don't count it in
			if ([Syntax.IfStatement,
				Syntax.ForStatement,
				Syntax.ForInStatement,
				Syntax.ForOfStatement,
				Syntax.WhileStatement,
				Syntax.DoWhileStatement,
				Syntax.CatchClause,
				Syntax.TryStatement,
				Syntax.ConditionalExpression,
				Syntax.SwitchCase,
				'FinallyClause']
				.includes(currentNode.type)) { depth++; }
		} else if (prevNode !== node) { // in the first iteration don't add an extra depth
			if (prevNode.type === Syntax.BlockStatement) {depth++;}
		}

		let functionName = self.getFunctionName(currentNode);
		if (functionName) {
			return depth;
		}
	}
}

function getHcgColumn(node) {
	let source;

	if (node.id === null) {
		source = node.parent.source();
	} else {
		source = node.source();
	}

	let firstLine = source.split(/\r?\n/)[0];

	return firstLine.indexOf('(') + 1;
}

function formatFunctionId(filename, functionName, line, column) {
	return util.format('%s@%s:%s:%s', filename, functionName, line, column);
}

function getTraceId(path = '') {
	let traceId = 0;
	do {
		// trace_id = Math.floor(Math.random() * 10000) + 1;
		traceId++;
	} while (fs.existsSync(path + traceId + '.json'));

	return traceId + '.json';
}

module.exports = {
	getStatement,
	getStatementEndIndex,
	getBlock, getFunctionId,
	getNodeDepth,
	getIndexIgnoreQuotation,
	getTraceId,
	formatFunctionId,
	initJSONHandler,
	getParentClass,
	getParentClassNode,
	getHcgColumn,
	dumpFunctionSource,
	dumpFileSource
};

