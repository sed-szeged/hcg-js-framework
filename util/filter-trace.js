var fs = require('fs');
var assert = require('assert');

if (process.argv.length < 4)
{
  throw "Usage: filename exclude_pattern";
}

var trace = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'))
var exclude = new RegExp(process.argv[3]);
var final_result = '[\n';

function recursive_walk(trace_node)
{
  assert.ok(trace_node instanceof Array);

  var len = trace_node.length;

  if (len == 0)
  {
    return;
  }

  var i = 0;
  while (i < len)
  {
    var frame = trace_node[i];

    if (frame.pos.search(exclude) == -1)
    {
      recursive_walk(frame.frames);
      i++;
      continue;
    }

    var frame_len = frame.frames.length;

    if (frame_len == 1)
    {
      trace_node[i] = frame.frames[0];
      continue;
    }

    if (frame_len == 0)
    {
      for (var j = i + 1; j < len; j++)
      {
        trace_node[j - 1] = trace_node[j];
      }

      len--;
      trace_node.length = len;
      continue;
    }

    var delta = frame_len - 1;

    for (var j = len - 1; j > i; j--)
    {
      trace_node[j + delta] = trace_node[j];
    }

    for (var j = 0; j < frame_len; j++)
    {
      trace_node[i + j] = frame.frames[j];
    }

    len += delta;
    assert.ok(trace_node.length == len);
  }
}

function recursive_print(trace_node, prefix)
{
  assert.ok(trace_node instanceof Array);

  var len = trace_node.length;

  if (len == 0)
  {
    return;
  }

  var begin = prefix + '  {\n' + prefix + '    "id": ';
  var end = '';

  for (var i = 0; i < len; i++)
  {
    var frame = trace_node[i];

    var str1 = begin + frame.id + ', "name": "' + frame.name + '", "pos": "' + frame.pos + '",\n';
    var str2 = prefix + '    "frames" : [\n';

    final_result += end + str1 + str2;

    recursive_print(frame.frames, prefix + '    ');

    if (end == '')
    {
      end = prefix + '    ]\n' + prefix + '  },\n';
    }
  }

  final_result += prefix + '    ]\n' + prefix + '  }\n';
}

recursive_walk(trace);
recursive_print(trace, '');

final_result += ']';

// Sanity check.
JSON.parse(final_result);

console.log(final_result);
