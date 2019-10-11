var fs = require('fs');
var assert = require('assert');

var is_eval = /^[\[<]/;

var node_data = { 0: { name:"<entry>", pos:"<entry>" } };
var final_result = '';
var known_nodes = {};
var known_eval_nodes = {};
var root_node = { 0:{} };
var next_id = 0;

function recursive_walk(current_frames, parent_node)
{
  assert.ok(current_frames instanceof Array);

  var len = current_frames.length;

  for (var i = 0; i < len; i++)
  {
    var current_node = current_frames[i];
    var current_id;

    if (current_node.pos.search(is_eval) != -1)
    {
      if (current_node.id in known_eval_nodes)
      {
        current_id = known_eval_nodes[current_node.id];
      }
      else
      {
        current_id = ++next_id;
        known_eval_nodes[current_node.id] = current_id;

        node_data[current_id] = {
                                  name: current_node.name,
                                  pos: current_node.pos,
                                };
      }
    }
    else
    {
      if (current_node.pos in known_nodes)
      {
        current_id = known_nodes[current_node.pos];
      }
      else
      {
        current_id = ++next_id;
        known_nodes[current_node.pos] = current_id;

        node_data[current_id] = {
                                  name: current_node.name,
                                  pos: current_node.pos,
                                };
      }
    }

    if (!(current_id in parent_node))
    {
      parent_node[current_id] = {};
    }

    if (current_node.frames.length == 0)
    {
      node_data[current_id].final = true;
      parent_node[current_id].final = true;
    }
    else
    {
      recursive_walk(current_node.frames, parent_node[current_id]);
    }
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
      recursive_walk(JSON.parse(trace), root_node[0]);
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
      recursive_walk(JSON.parse(trace), root_node[0]);
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

  final_result += '\n],\n"call_chains": [';
}

function recursive_print(prefix, call_chain_node, id_only)
{
  if (call_chain_node.final)
  {
    final_result += (comma_needed ? ',\n' : '\n') + prefix + ' ]';
    comma_needed = true;
  }

  for (var key in call_chain_node)
  {
    if (key == "final")
    {
      continue;
    }

    var str = ((prefix == '  [') ? ' ' : ', ');

    if (id_only)
    {
      str += key;
    }
    else
    {
      str += '{ "id": ' + key + ', "label": "' + node_data[key].name + '" }';
    }

    recursive_print(prefix + str, call_chain_node[key], id_only);
  }
}

process_files();

print_header();

var comma_needed = false;
recursive_print('  [', root_node, true);

final_result += '\n]\n}';

// Sanity check.
JSON.parse(final_result);

console.log(final_result);
