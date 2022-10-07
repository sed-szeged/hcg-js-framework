/*
 * Tracks injecting and makes sure that the same
 * functions don't get instrumented more than once
 */

class InjectTracker {
	constructor() {
		this.functionList = {};
	}

	/*
	 * Adds a function to the list
	 * return true if function is new
	 */
	addFunction(fileName, functionName, parentClass = 'none') {
		if (this.functionList[fileName] === undefined) {
			this.functionList[fileName] = {classes: {}};
		}

		if (!this.functionList[fileName].classes.includes(parentClass)) {
			this.functionList[fileName].classes.push({[parentClass]: []});
		}

		if (!this.functionList[fileName].classes[parentClass].includes(functionName)) {
			this.functionList[fileName].classes[parentClass].push(functionName);
			return true;
		}

		return false;
	}
}

module.exports = new InjectTracker();
