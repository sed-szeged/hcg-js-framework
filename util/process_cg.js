var fs = require('fs');
var assert = require('assert');

var is_eval = /^[\[<]/;

var node_data = { 0: { name:"<entry>", pos:"<entry>" } };
var final_result = '';
var call_graph = {};
var known_nodes = {};
var known_eval_nodes = {};
var next_id = 0;

function recursive_walk(target_nodes, source_id)
{
  assert.ok(target_nodes instanceof Array);

  var current_cg_node = call_graph[source_id];

  if (!current_cg_node)
  {
    current_cg_node = {};
    call_graph[source_id] = current_cg_node;
  }

  var len = target_nodes.length;

  if (len == 0)
  {
    node_data[source_id].final = true;
    return;
  }

  for (var i = 0; i < len; i++)
  {
    var target_node = target_nodes[i];
    var target_id;

    if (target_node.pos.search(is_eval) != -1)
    {
      if (target_node.id in known_eval_nodes)
      {
        target_id = known_eval_nodes[target_node.id];
      }
      else
      {
        target_id = ++next_id;
        known_eval_nodes[target_node.id] = target_id;

        node_data[target_id] = {
                                 name: target_node.name,
                                 pos: target_node.pos,
                               };
      }
    }
    else
    {
      if (target_node.pos in known_nodes)
      {
        target_id = known_nodes[target_node.pos];
      }
      else
      {
        target_id = ++next_id;
        known_nodes[target_node.pos] = target_id;

        node_data[target_id] = {
                                 name: target_node.name,
                                 pos: target_node.pos,
                               };
      }
    }

    current_cg_node[target_id] = true;

    recursive_walk(target_node.frames, target_id);
  }
}

function process_files()
{
  if (process.argv.length < 3)
  {
    throw 'List of filenames or -l filename required.';
  }

  if (process.argv[2] != '-l')
  {
    var len = process.argv.length;

    for (var i = 2; i < len; i++)
    {
      var trace = fs.readFileSync(process.argv[i], 'utf8');

      known_eval_nodes = {};
      recursive_walk(JSON.parse(trace), 0);
    }
    return;
  }

  if (process.argv.length < 4)
  {
    throw 'Filename required after -l.';
  }

  var fileList = fs.readFileSync(process.argv[3], 'utf8');

  fileList = fileList.split(/\r\n|\r|\n/);

  var len = fileList.length;

  for (var i = 0; i < len; i++)
  {
    if (fileList[i])
    {
      var trace = fs.readFileSync(fileList[i], 'utf8');

      known_eval_nodes = {};
      recursive_walk(JSON.parse(trace), 0);
    }
  }
}

function print_header()
{
  final_result = '{\n"directed": true,\n"multigraph": false,\n"nodes": [';

  var comma_needed = false;

  for (var key in node_data)
  {
    var node = node_data[key];

    var str = (comma_needed ? ',\n' : '\n');
    str += '  { "id": ' + key + ', "label": "' + node.name + '", "pos": "' + node.pos + '"'

    if (node.final)
    {
      str += ', "final": true';
    }

    if (key == 0)
    {
      str += ', "entry": true';
    }

    str += ' }';

    final_result += str;
    comma_needed = true;
  }

  final_result += '\n],\n"links": [';
}

function print_links()
{
  var comma_needed = false;

  for (var source_id in call_graph)
  {
    for (target_id in call_graph[source_id])
    {
      var str = (comma_needed ? ',\n' : '\n');

      str += '  { "source": ' + source_id + ', "target": ' + target_id + ' }';

      final_result += str;
      comma_needed = true;
    }
  }
}

process_files();

print_header();
print_links();
final_result += '\n]\n}';

// Sanity check.
JSON.parse(final_result);

console.log(final_result);
