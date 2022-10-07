const assert = require('assert');

describe('Refactoring', function () {
	it('Should generate json for example_lib', function () {
		const fs = require('fs')

		let expected = fs.readFileSync("/home/wolf/Ceges/McBaby/hybrid-metric-framework/util/njsTrace/test/output.json", 'utf8');
		let result = "";

		try {
			result = fs.readFileSync("/home/wolf/Ceges/McBaby/hybrid-metric-framework/node-sources/example-repo/traces/test-1.json", 'utf8');
		} catch(e) {
			console.log(e);
		}


		assert.equal(expected, result);
	});


});
