var fs = require('fs');
var assert = require('assert');

if (process.argv.length < 4)
{
  throw "Usage: filename include_pattern [exclude_pattern]";
}

var include = new RegExp(process.argv[3]);
var exclude = null;

if (process.argv.length >= 5)
{
  exclude = new RegExp(process.argv[4]);
}

var call_graph = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'))
var next_id = 0;
var entry_links = {};

function check_included(id)
{
  var node = call_graph.nodes[id];

  if (node.included === undefined)
  {
    node.included = node.pos.search(include) != -1;
  }

  return node.included;
}

function get_id(id)
{
  var node = call_graph.nodes[id];

  if (exclude)
  {
    if (node.exclude === undefined)
    {
      node.exclude = node.pos.search(exclude) != -1;
    }

    if (node.exclude)
    {
      return 0;
    }
  }

  if (node.new_id === undefined)
  {
    node.new_id = ++next_id;
  }

  return node.new_id;
}

function filter_cg()
{
  var links = call_graph.links;
  var links_len = links.length;

  for (var i = 0; i < links_len; i++)
  {
    var link = links[i];

    var source_included = check_included(link.source);
    var target_included = check_included(link.target);

    if (source_included || target_included)
    {
      link.source = get_id(link.source);
      link.target = get_id(link.target);

      if (link.target != 0)
      {
        if (link.source != 0)
        {
          continue;
        }
        if (!entry_links[link.target])
        {
          entry_links[link.target] = true;
          continue;
        }
      }
    }

    /* Remove this link. */
    link.source = undefined;
    link.target = undefined;
  }
}

function print_header()
{
  var nodes = call_graph.nodes;
  var len = nodes.length;
  var comma_needed = false;

  function sort_function(a,b)
  {
    a = (a.new_id === undefined) ? 0 : a.new_id;
    b = (b.new_id === undefined) ? 0 : b.new_id;
    return a - b;
  }

  nodes.sort(sort_function);

  final_result = '{\n"directed": true,\n"multigraph": false,\n"nodes": [';

  for (var i = 0; i < len; i++)
  {
    var node = nodes[i];

    if (node.new_id === undefined)
    {
      continue;
    }

    var str = (comma_needed ? ',\n' : '\n');
    str += '  { "id": ' + node.new_id + ', "label": "' + node.label + '", "pos": "' + node.pos + '"'

    if (node.final)
    {
      str += ', "final": true';
    }

    if (node.new_id == 0)
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
  var links = call_graph.links;
  var len = links.length;
  var comma_needed = false;

  for (var i = 0; i < len; i++)
  {
    var link = links[i];

    if (link.source !== undefined)
    {
      var str = (comma_needed ? ',\n' : '\n');

      str += '  { "source": ' + link.source + ', "target": ' + link.target + ' }';

      final_result += str;
      comma_needed = true;
    }
  }
}

call_graph.nodes[0].new_id = 0;

filter_cg();

print_header();
print_links();
final_result += '\n]\n}';

// Sanity check.
JSON.parse(final_result);

console.log(final_result);
