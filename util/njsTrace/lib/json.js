const fs = require('fs');

/**
 * A class that handles JSONobj objects and writes to files
 */
class JSONobj {
	/**
	 * Creates a JSONobj handler
	 * @param path File path to write/read from
	 * @param overwrite Should we overwrite the file even if it exists?
	 */
	constructor(path,overwrite = false) {
		this.path = path;
		this.obj = {};

		if (!overwrite) {this.read();}
	}

	/**
	 * Write stored object to file
	 */
	flush() {
		fs.writeFileSync(this.path, JSON.stringify(this.obj, null, 4));
	}

	/**
	 * Read JSONobj from specified file path
	 * Will be an empty object if file doesn't exist, or is not a JSONobj
	 */
	read() {
		if (!fs.existsSync(this.path)) {return;}

		try {
			let content = fs.readFileSync(this.path, 'utf8');
			this.obj = JSON.parse(content);
		} catch(e) {}
	}
}

module.exports = {JSONobj};
