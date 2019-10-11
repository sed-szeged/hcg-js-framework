var fs = require("fs");
var parse = require('./jsCallChain/lib/acorn.js').parse;

var opts = { ecmaVersion: 9, locations: true };
var stdout = process.stdout;
var stderr = process.stderr;
var locationParse = /^(.*):([0-9]+:[0-9]+)$/;
var shebangParse = /^.*/;
var fileMap = new Map();

if (process.argv.length < 3) {
    stderr.write("Usage: lineinfo-update.js file_name\n");
    process.exit(-1);
}

function defineStart(positionRemap, loc)
{
    var column = loc.column + 1 - (loc.line == 1 ? 62 : 0);
    positionRemap.set(loc.line + ":" + (loc.column + 1), loc.line + ":" + column);
}

function searchOpenBracket(positionRemap, src, offset, startLoc, loc)
{
    var line = startLoc.line;
    var column = startLoc.column + 1;

    while (src[offset] != '(') {
        var chr = src[offset];

        if (chr == '\r') {
            offset += (src[offset + 1] == '\n') ? 2 : 1;
            column = 1;
            line += 1;
            continue;
        }

        if (chr == '\n') {
            offset++;
            column = 1;
            line += 1;
            continue;
        }

        offset++;
        column++;
    }

    if (line == 1) {
        column -= 62;
    }

    positionRemap.set(loc.line + ":" + (loc.column + 1), line + ":" + column);
}

function skipSpaces(src, offset, startLoc, extra)
{
    var line = startLoc.line;
    var column = startLoc.column + extra;

    offset += extra;

    while (true) {
        var chr = src[offset];

        if (chr == '\r') {
            offset += (src[offset + 1] == '\n') ? 2 : 1;
            column = 0;
            line += 1;
            continue;
        }

        if (chr == '\n') {
            offset++;
            column = 0;
            line += 1;
            continue;
        }

        if (chr == ' ' || chr == ' ')  {
            offset++;
            column++;
            continue;
        }

        return { line, column };
    }
}

function processProperty(positionRemap, src, node)
{
    var loc = node.loc.start;

    if (node.static) {
        loc = skipSpaces(src, node.start, loc, 6);
    }
    else {
        var chr = src[node.start];

        if (chr == '"' || chr == "'") {
            loc = { line: loc.line, column: loc.column + 1 };
        }
    }

    var func = node.value;

    searchOpenBracket(positionRemap, src, func.start, func.loc.start, loc);

    func.skipSearch = true;
}

function processClass(positionRemap, src, node)
{
    var body = node.body.body;
    var bodyLen = body.length;

    for (var i = 0; i < bodyLen; i++) {
        var child = body[i];
        if (child.type == 'MethodDefinition' && child.kind == 'constructor') {
            searchOpenBracket(positionRemap, src, child.start, child.loc.start, node.loc.start);
            return;
        }
    }
    defineStart(positionRemap, node.loc.start);
}

function getLineInfo(fileName)
{
    try {
        var src = fs.readFileSync(fileName).toString();
    } catch(err) {
        // stderr.write("Warning: file '" + fileName + "' is not found.\n");
        fileMap.set(fileName, "no_data");
        return "no_data";
    }

    if (src[0] == '#' && src[1] == '!') {
        // Remove Shebang
        src = src.replace(shebangParse, '');
    }

    src = '(function (exports, require, module, __filename, __dirname) { ' + src + '\n});'

    try {
        var ast = parse(src, opts);
    } catch(err) {
        stderr.write("Error: '" + err +  "'\n'" + fileName + "' is not a valid JavaScript source code.\n");
        process.exit(-1);
    }

    var positionRemap = new Map();

    positionRemap.set("1:1", "1:0");
    positionRemap.set("1:2", "1:1");
    ast.body[0].expression.skipSearch = true;

    function walk(node) {
        switch (node.type) {
        case 'FunctionDeclaration':
        case 'FunctionExpression':
            // Generators are also handled here.
            if (!node.skipSearch) {
                searchOpenBracket(positionRemap, src, node.start, node.loc.start, node.loc.start);
            }
            break;
        case 'ArrowFunctionExpression':
            defineStart(positionRemap, node.loc.start);
            break;
        case 'Property':
            if (node.method || node.kind == "get" || node.kind == "set") {
                processProperty(positionRemap, src, node);
            }
            break;
        case 'ClassDeclaration':
        case 'ClassExpression':
            processClass(positionRemap, src, node);
            break;
        case 'MethodDefinition':
            if (node.kind == 'constructor') {
                node.value.skipSearch = true;
                break;
            }
            processProperty(positionRemap, src, node);
            break;
        }

        for (var key in node) {
            var child = node[key];

            if (Array.isArray(child)) {
                var childLen = child.length;

                for (var childIdx = 0; childIdx < childLen; ++childIdx) {
                    var childValue = child[childIdx];

                    if (childValue && typeof childValue.type === 'string') {
                        walk(childValue);
                    }
                }
            }
            else if (child && typeof child.type === 'string') {
                walk(child);
            }
        }
    }

    walk(ast);

    fileMap.set(fileName, positionRemap);
    return positionRemap;
}

function lineInfoUpdate(fileName)
{
    try {
        var src = JSON.parse(fs.readFileSync(fileName).toString());
    } catch(err) {
        stderr.write("Error: '" + fileName + "' is not a valid JSON file.\n");
        process.exit(-1);
    }

    stdout.write('{\n"directed": true,\n"multigraph": false,\n"nodes": [\n');
    stdout.write("  { \"id\": 0, \"label\": \"<entry>\", \"pos\": \"<entry>\", \"entry\": true }");

    var nodes = src.nodes;
    var len = nodes.length;

    for (var i = 0; i < len; i++) {
        var node = nodes[i];
        if (node.id == 0) {
            continue;
        }

        var pos = locationParse.exec(node.pos);

        if (pos == null) {
            stderr.write("Error: '" + node.pos + "' is not a valid node position.\n");
            process.exit(-1);
        }

        var fileName = pos[1];

        var positionRemap = fileMap.get(fileName);
        if (!positionRemap) {
            positionRemap = getLineInfo(fileName);
        }

        if (positionRemap !== "no_data") {
            var mappedPos = positionRemap.get(pos[2]);
            if (!mappedPos) {
                stderr.write("Warning: position '" + node.pos + "' is not mapped.\n");
                pos = node.pos;
            }
            else {
                pos = fileName + ":" + mappedPos;
            }
        }
        else {
            if (pos[2] == "1:1") {
                pos = pos[1] + ":1:0";
            }
            else if (pos[2] == "1:2") {
                pos = pos[1] + ":1:1";
            }
            else {
                pos = node.pos;
            }
        }

        stdout.write(',\n  { "id": ' + node.id + ', "label": ' + JSON.stringify(node.label) + ', "pos": ' + JSON.stringify(pos) + ' }');
    }

    stdout.write('\n],\n"links": [\n');

    var links = src.links;
    var len = links.length - 1;

    for (var i = 0; i <= len; i++) {
        var link = links[i];
        console.log('  { "source": ' + link.source + ', "target": ' + link.target + ' }' + (i < len ? ',' : ''));
    }
    console.log(']\n}');
}

lineInfoUpdate(process.argv[2]);
