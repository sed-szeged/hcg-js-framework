const {JSONobj} = require('./json.js');

class JSONHandler {
	constructor() {
		this.jsonList = {};
	}

	getJSON(path) {
		if (!(path in this.jsonList)) {
			this.jsonList[path] = new JSONobj(path, true);
		}

		return this.jsonList[path];
	}

	flushAll() {
		for (let [path, jsonObj] of Object.entries(this.jsonList)) {
			jsonObj.flush();
		}
	}
}

module.exports = new JSONHandler();
