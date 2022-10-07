let util = require('util'),
	esparse = require('./esparse.js'),
	Syntax = require('./syntax.js'),
	injectUtils = require('./inject-utils');

let jsonHandler = injectUtils.initJSONHandler();

let TRACE_ENTRY = 'var __njsEntryData__ = __njsTraceEntry__({file: %s, name: %s, line: %s, column: %s, args: %s});';
let TRACE_EXIT = '__njsTraceExit__({entryData: __njsEntryData__, exception: %s, line: %s, column: %s, returnValue: %s, jsonPath: "%s"});';
let ON_STATEMENT = '__njsOnStatement__(%s);';
let DUMP_FILES = false;

/**
 * Creates a new instance of Instrumentation "class"
 * @class Provides instrumentation functionality
 * @param {NJSTrace} njsTrace - A reference to an NJSTrace object
 * @constructor
 */
function Injector(njsTrace) {
	this.njs = njsTrace;
}

/**
 * Returns whether the given node is a function node
 * @param {Object} node - The node to check
 * @returns {boolean}
 */
Injector.prototype.isFunctionNode = function(node) {
	return (node.type === Syntax.FunctionDeclaration || node.type === Syntax.FunctionExpression || node.type === Syntax.ArrowFunctionExpression) && node.range;
};

/**
 * Gets the function name (if this node is a function node).
 * @param {object} node - The falafel AST node
 * @returns {string} The function name
 */
Injector.prototype.getFunctionName = function(node) {
	// Make sure this is a function node.
	if (!this.isFunctionNode(node)) {
		return;
	}

	// Not all functions have ids (i.e Anonymous functions), in case we do have id we can get it and stop.
	if (node.id) {
		return node.id.name;
	}

	// FunctionDeclaration (function foo(){...}) should ALWAYS have id,
	// so in case this is FunctionDeclaration and it had no id it's an error.
	if (node.type === Syntax.FunctionDeclaration) {
		this.njs.emit(this.njs.prototype.events.Error, new Error('A FunctionDeclaration node has no id data, node:' + JSON.stringify(node)));
		return '';
	}

	// So this is an anonymous FunctionExpression, we try to get a name using the parent data,
	// for example in case of: let foo = function(){}, the name would be foo.
	let parent = node.parent;
	switch (parent.type) {
		// let f; f = function () {...}
		case Syntax.AssignmentExpression:
			// Extract the variable name
			if (parent.left.range) {
				return parent.left.source().replace(/"/g, '\\"');
			}
			break;

		// let f = function(){...}
		case Syntax.VariableDeclarator:
			return parent.id.name;

		// IIFE (function(scope) {})(module);
		case Syntax.CallExpression:
			return parent.callee.id ? parent.callee.id.name : '[Anonymous]';

		// Don't give up, can still find
		default:
			// Happens when a function is passed as an argument foo(function() {...})
			if (typeof parent.length === 'number') {
				return parent.id ? parent.id.name : '[Anonymous]';
				// Not sure when this happens...
			} else if (parent.key && parent.key.type === 'Identifier' &&
				parent.value === node && parent.key.name) {
				return parent.key.name;
			}
	}

	return '[Anonymous]';
};

/**
 * Get the long name of a function/method
 * @param functionName Name of the function
 * @param filename Filename of where the function is located
 * @param className Parent class name
 * @returns {string} LongName of function/method
 */
function getFunctionLongName(functionName, filename, className = '') {
	let repoPath = process.cwd() + '/';
	let newName = filename.replace(repoPath, '').replace('/', '.').replace('\\', '.');
	let extension = newName.split('.').pop();
	if (className !== '') {
		className = className.split(':').pop();
		className += '.';
	}

	newName = newName.slice(0, newName.length - extension.length) + className + functionName;

	return newName;
}

/**
 * Get the long name of a class
 * @param className Name of the class
 * @param filename Filename of where the class is located
 * @returns {string} LongName of class
 */
function getClassLongName(className, filename) {
	let repoPath = process.cwd() + '/';
	let newName = filename.replace(repoPath, '').replace('/', '.').replace('\\', '.');
	let extension = newName.split('.').pop();
	className = className.split(':').pop();

	return newName.slice(0, newName.length - extension.length) + className;
}

/**
 * Checks whether this node belongs to Node's wrapper function (the top level function that wraps every Node's module)
 * @param {object} node - The falafel AST node
 * @returns {boolean}
 */
Injector.prototype.isOnWrapperFunction = function(node) {
	let parent = node.parent;
	while (parent) {
		if (this.isFunctionNode(parent)) {
			return parent.loc.start.line === 1;
		}

		parent = parent.parent;
	}

	return true;
};

/**
 * Inject hybrid-metric-framework tracing functions into the given code text
 * @param {string} filename - The file being instrumented
 * @param {string} code - The JS code to trace
 * @param {Boolean} wrapFunctions - Whether to wrap functions in try/catch
 * @param {boolean} includeArguments - Whether a traced function arguments and return values should be passed to the tracer
 * @param {boolean} wrappedFile - Whether this entire file is wrapped in a function (i.e like node is wrapping the modules in a function)
 * @returns {string} The modified JS code text
 */
Injector.prototype.injectTracing = function(filename, code, wrapFunctions, includeArguments, wrappedFile) {
	let self = this;
	let traceExit;
	let output = esparse(code, {range: true, loc: true, ecmaVersion: 10}, function processASTNode(node) {
		// In wrapped files the first line is the wrapper function so we need to offset location to get the real lines in user-world
		let startLine = wrappedFile ? node.loc.start.line - 1 : node.loc.start.line;
		let retLine = wrappedFile ? node.loc.end.line - 1 : node.loc.end.line;

		// If we have name this is a function
		let name = self.getFunctionName(node);

		let statementData = getStatementData();

		if (name) {
			addFunctionToJSON();

			setUpTracing();

			let modified = modifiedFunctionDeclaration();
			node.update(modified);

			if (DUMP_FILES) {
				injectUtils.dumpFileSource(node, filename);
			}


		// If this is a return statement we should trace exit
		} else if (node.type === Syntax.ReturnStatement && (!wrappedFile || !self.isOnWrapperFunction(node))) {
			node.update(modifiedReturnStatement());

			if (DUMP_FILES) {
				injectUtils.dumpFileSource(node, filename);
			}
		} else {
			modifyCode();
		}

		function statementFunctions() {
			const result = new Map();

			result.set(Syntax.BlockStatement, modifiedBlockStatement);

			result.set(Syntax.IfStatement, modifiedOtherStatement);
			result.set(Syntax.ForStatement, modifiedOtherStatement);
			result.set(Syntax.ForInStatement, modifiedOtherStatement);
			result.set(Syntax.ForOfStatement, modifiedOtherStatement);
			result.set(Syntax.WhileStatement, modifiedOtherStatement);
			result.set(Syntax.CatchClause, modifiedOtherStatement);
			result.set(Syntax.SwitchCase, modifiedSwitchCase);

			result.set(Syntax.TryStatement, modifiedOtherStatement);

			result.set(Syntax.DoWhileStatement, modifiedDoWhile);
			result.set(Syntax.LogicalExpression, modifiedLogicalExpression);
			result.set(Syntax.ConditionalExpression, modifiedConditionalExpression);

			result.set(Syntax.ReturnStatement, modifiedReturnStatement);

			return result;
		}

		/**
		 * Modify the code if it has a corresponding modify function
		 * @returns {string} Modified code
		 */
		function modifyCode() {
			let modifyFunction = statementFunctions().get(node.type);
			if (modifyFunction) {
				let modified = modifyFunction();
				if (modified) {
					node.update(modified);
					if (DUMP_FILES) {
						injectUtils.dumpFileSource(node, filename);
					}
				}
			}
		}

		function modifiedFunctionDeclaration() {
			let startIndex = 0;

			// ArrowFunctionExpressions can have their only parameter without parantheses '()'
			// eg. error => { ... } instead of (error) => { ... }
			// If this is the case, we shouldn't change the start position!
			startIndex = injectUtils.getStatementEndIndex(node.source());

			let pos = node.source().indexOf('{', startIndex);

			pos += 1;

			return node.source().slice(0, pos) + '\n' + fillOnStatement() + '\n' + node.source().slice(pos);
		}

		/**
		 * Modify a do-while loop to inject code
		 * @returns {string} Modified code
		 */
		function modifiedDoWhile() {
			let firstPart = injectUtils.getBlock(node.source());
			let secondPart = node.source().split(firstPart).slice(1).join(firstPart);
			secondPart = injectUtils.getStatement(secondPart);
			secondPart = secondPart.slice(0, secondPart.length - 1); // remove end

			return util.format('%s%s && (function(){%s return true})() );', firstPart, secondPart, fillOnStatement());
		}

		/**
		 * Modify a logical expression to inject code
		 * @returns {string} Modified code
		 */
		function modifiedLogicalExpression() {
			let newBlock = node.source();

			if (newBlock.includes('&&') || newBlock.includes('||')) {
				newBlock = util.format('(function(){%s return false})() || (%s)', fillOnStatement(), node.source());
			}

			return newBlock;
		}

		/**
		 * Modify a conditional expression to inject code
		 * @returns {string} Modified code
		 */
		function modifiedConditionalExpression() {
			// If this is a Conditional Expression we should inject an IIFE to the start of the conditional
			// IIFE = Immediately Invoked Function Expression
			return util.format('(function(){%s return false})() || %s', fillOnStatement(), node.source());
		}

		function modifiedBlockStatement() {
			// Finally: TryStatement -> BlockStatement
			// TryStatement has a 'finalizer' property in case it has a finally branch.
			// This 'finalizer' property is the finally node.
			let tryParent = node.parent;
			if (tryParent && tryParent.type === Syntax.TryStatement) {
				if (tryParent.finalizer && tryParent.finalizer === node) {
					return modifiedOtherStatement();
				}
			}

			// NL: "Block statements directly inside other block statements"
			if (node.parent.type === Syntax.BlockStatement) {
				let source = node.source();
				let pos = source.indexOf('{');
				if (pos !== -1) {
					pos += 1;
					return '{\n' + fillOnStatement() + '\n' + source.slice(pos);
				}
			}

			return undefined; // Return undefined because node.source() strips "`" characters!!
		}

		// eslint-disable-next-line no-extend-native
		String.prototype.indexOfEnd = function(string) {
			const io = this.indexOf(string);
			return io === -1 ? -1 : io + string.length;
		};

		/**
		 * Modify other statements to inject code
		 * Block Statements are: If, For, For-In, For-Of, While
		 * @returns {string} Modified code
		 */
		function modifiedOtherStatement() {

			if ([Syntax.IfStatement, Syntax.ForStatement, Syntax.WhileStatement].includes(node.type)) {
				// This statement isn't followed by a block, but we need to run 2 statements. Add a block.
				let ifStatement = injectUtils.getStatement(node.source());

				// We have the if statement. Check if it's directly followed by a {, if not, the statement isn't in a block.
				let source = node.source();
				let afterStatementIndex = source.indexOfEnd(ifStatement); // Get where the last character of the statement is (without the {} block)

				let blockIndex = -1; // Where does the block of this statement start?

				for (let i = afterStatementIndex; i < source.length; i++) {
					const char = source[i];

					if (char === ' ') { continue; }
					else if (char === '{') { blockIndex = i; break; }
					else { break; }
				}

				if (blockIndex !== -1) {
					// If we have a block, insert into it
					let pos = blockIndex + 1;
					return node.source().slice(0, pos) + '\n' + fillOnStatement() + '\n' + node.source().slice(pos);
				}

				let afterIf = node.source().split(ifStatement).slice(1).join(ifStatement);
				let remaining = '';

				// Sometimes if statements include the 'else' branch too, mitigate for this
				if (afterIf.includes('else')) {
					let splitCode = afterIf.split('else');
					afterIf = splitCode[0];
					remaining = 'else' + splitCode.slice(1).join('else'); // everything after else
				}

				// If we don't have a block, create one (we need 2 statements, not just one!)
				return ifStatement + '\n{\n' + fillOnStatement() + afterIf + '\n}' + remaining + '\n';
			}

			let pos = node.source().indexOf('{');
			if (pos !== -1) {
				// This statement is followed by a block! eg. if(true) {doSomething;}
				pos += 1; // move one to the right
				return node.source().slice(0, pos) + '\n' + fillOnStatement() + '\n' + node.source().slice(pos);
			}

			return fillOnStatement() + '\n' + node.source() + '\n';
		}

		/**
		 * Modify switch cases to inject code
		 * @returns {string} Modified code
		 */
		function modifiedSwitchCase() {
			let colonIndex = injectUtils.getIndexIgnoreQuotation(node.source(), ':');

			let modified = node.source().substring(0, colonIndex + 1) + '\n' + fillOnStatement() + '\n' + node.source().substring(colonIndex + 1);

			if (node.source().includes('break')) {
				modified += '\nbreak;\n';
			}

			return modified;
		}

		/**
		 * If this return stmt has some argument (e.g return XYZ;) we will put this argument in a helper let, do our TRACE_EXIT,
		 * and return the helper var. This is because the return stmt could be a function call and we want
		 * to make sure that our TRACE_EXIT is definitely the last call.
		 * @returns {string}
		 */
		function modifiedReturnStatement() {
			let result = '';

			if (node.argument) {
				// Use a random variable name
				let tmpVar = '__njsTmp' + Math.floor(Math.random() * 10000) + '__';

				// We wrap the entire thing in a new block for cases when the return stmt is not in a block (i.e "if (x>0) return;").
				traceExit = util.format(TRACE_EXIT, 'false', startLine, injectUtils.getHcgColumn(node), includeArguments ? tmpVar : 'null', jsonHandler.path);
				result = ('{\nvar ' + tmpVar + ' = (' + node.argument.source() + ');\n' + traceExit + '\nreturn ' + tmpVar + ';\n}');
			} else {
				traceExit = util.format(TRACE_EXIT, 'false', startLine, injectUtils.getHcgColumn(node), 'null', jsonHandler.path);
				result = ('{' + traceExit + node.source() + '}');
			}

			return result;
		}

		/**
		 * Return FinallyClause if needed
		 * @returns {string|*} node type string
		 */
		function getNodeType() {
			if (node.type === Syntax.BlockStatement) {
				if (node.parent.finalizer === node) {
					return 'FinallyClause';
				}
				if (node.parent.type === Syntax.BlockStatement) {
					return 'DirectBlockStatement';
				}
			}

			return node.type;
		}

		/**
		 * Get an object with all the data needed about the current statement
		 * @returns {{}} Statement data object
		 */
		function getStatementData() {
			let result = {};
			result.function_id = injectUtils.getFunctionId(node, self, filename);
			result.name = self.getFunctionName(node);
			result.long_name = getFunctionLongName(result.name, filename);
			result.parent_class = injectUtils.getParentClass(node);
			result.type = getNodeType();
			result.file_name = filename;
			result.line = startLine;
			result.column = node.loc.start.column;
			result.end_line = retLine;
			result.end_column = node.loc.end.column;
			result.json_path = jsonHandler.path;
			result.depth = injectUtils.getNodeDepth(node, self);

			return result;
		}

		function fillOnStatement() {
			return util.format(ON_STATEMENT, JSON.stringify(statementData));
		}

		function addFunctionToJSON() {
			// function_id: "/home/wolf/Ceges/McBaby/example_lib.js@say_hello_if_five:29:0"
			const functionId = injectUtils.formatFunctionId(filename, name, startLine, node.loc.start.column);
			let parentClass = injectUtils.getParentClass(node);

			if (parentClass) {
				// This is a class method, insert it into the corresponding class
				jsonInsertClassMethod(parentClass, {function_id: functionId, name: self.getFunctionName(node), long_name: getFunctionLongName(name, filename, parentClass), path: filename, parent_class: parentClass, is_called: false, line: startLine, column: node.loc.start.column, statements: []});
			} else {
				// This is a regular function
				jsonInsertFunction({function_id: functionId, name: self.getFunctionName(node), long_name: getFunctionLongName(name, filename), path: filename, is_called: false, line: startLine, column: node.loc.start.column, statements: []});
			}
		}

		// Push a function into the json object
		function jsonInsertFunction(method) {
			jsonHandler.obj.functions.push(method);
		}

		// Push a class into the json object
		function jsonInsertClass(properties) {
			let classNode = injectUtils.getParentClassNode(node);
			if (classNode) {
				properties.line = wrappedFile ? classNode.loc.start.line - 1 : classNode.loc.start.line;
				properties.column = classNode.loc.start.column;
			}

			jsonHandler.obj.classes.push(properties);
		}

		// Push a method into an existing (or not existing) class
		function jsonInsertClassMethod(className, method) {
			let index = jsonFindClassIndex(className);
			if (index === -1) {
				jsonInsertClass({name: className, path: filename, long_name: getClassLongName(className, filename), methods: []});
				index = jsonFindClassIndex(className);
			}

			jsonHandler.obj.classes[index].methods.push(method);
		}

		// Get the index of a class in the class list
		function jsonFindClassIndex(className) {
			for (let i in jsonHandler.obj.classes) {
				if (jsonHandler.obj.classes[i].name === className) {
					return i;
				}
			}

			return -1;
		}

		function setUpTracing() {
			// console.log("function_id: " + function_id)
			self.njs.log('  Instrumenting ', name, 'line:', node.loc.start.line);

			// Empty arrow functions are NOT BlockStatements (i.e "() => i")
			let isBlockStatement = (node.body.type === Syntax.BlockStatement);

			// Separate the function declaration ("function foo") from function body ("{...}")
			let funcDec = node.source().slice(0, node.body.range[0] - node.range[0]);
			let origFuncBody = node.body.source();
			if (isBlockStatement) {
				// Remove the open and close braces "{}"
				origFuncBody = origFuncBody.slice(1, origFuncBody.length - 1);
			} else {
				// Take the part of the function declaration only till the "=>" (i.e if it's "res => ({x:123})" ignore the "(" )
				let idx = funcDec.indexOf('=>');
				if (idx > 0) {
					funcDec = funcDec.substring(0, idx + 2);
				}

				// This function is not BlockStatement, meaning what we have as the function body is just
				// a return value. Convert it to a BlockStatement function that just return that value, so
				// we can put our injection code inside that function.

				let rLine = wrappedFile ? node.body.loc.start.line - 1 : node.body.loc.start.line; // return line of our func
				let tmpVar = '__njsTmp' + Math.floor(Math.random() * 10000) + '__'; // hold the return value

				let exitTrace = util.format(TRACE_EXIT, 'false', rLine, injectUtils.getHcgColumn(node), includeArguments ? tmpVar : 'null', jsonHandler.path);

				// The new function body, just return the value represented by the arrow function
				origFuncBody = '\nlet ' + tmpVar + ' = (' + origFuncBody + ');\n' + exitTrace + '\nreturn ' + tmpVar + ';\n';
			}

			// If this file is wrapped in a function and this is the first line, it means that this is the call
			// to the file wrapper function, in this case we don't want to instrument it (as this function is hidden from the user and also creates a mess with async/await)
			// In reality it means that this is the function that Node is wrapping all the modules with and call it when
			// the module is being required.
			if (wrappedFile && node.loc.start.line === 1) {return;}

			let args = 'null';
			if (includeArguments) {
				args = '[' + node.params.map(p => {
					if (p.type === Syntax.RestElement) {
						return p.argument.name;
					}

					return p.name;
				}).join(',') + ']';
			}

			// put our TRACE_ENTRY as the first line of the function and TRACE_EXIT as last line
			let traceEntry = util.format(TRACE_ENTRY, JSON.stringify(filename), JSON.stringify(name), startLine, injectUtils.getHcgColumn(node), args);
			traceExit = util.format(TRACE_EXIT, 'false', retLine, node.loc.start.column, 'null', jsonHandler.path);

			let newFuncBody = '\n' + traceEntry + '\n' + origFuncBody + '\n' + traceExit + '\n';

			if (wrapFunctions) {
				let traceEX = util.format(TRACE_EXIT, 'true', startLine, node.loc.start.column, 'null', jsonHandler.path);
				node.update(funcDec + '{\ntry {' + newFuncBody + '} catch(__njsEX__) {\n' + traceEX + '\nthrow __njsEX__;\n}\n}');
			} else {
				node.update(funcDec + '{' + newFuncBody + '}');
			}
		}
	});
	return output.toString();

};


module.exports = Injector;
