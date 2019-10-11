#!/bin/bash

if [ "$1" != "v8" ]; then
  if [ "$1" != "np" ]; then
    if [ "$1" != "js" ]; then
      echo "Unknown mode. Please specifiy one of these"
      echo "v8 - combine results only (for modified v8)"
      echo "np - convert with jscc-convert first (for nodeprof.js)"
      echo "js - add trail and convert with jscc-convert first (for jsCallChain)"
      exit
    fi
  fi
fi

TOOLS=
MERGE=callchain-merge.py
CONVERT=convert-event-log.py

if [ "$2" == "-cg" ]; then
  MERGE="callgraph-merge.py"
  CONVERT="convert-event-log.py -cg"

  if [ -n "$3" ]; then
    TOOLS="$3/"
    NODE="$4"
  fi
else
  if [ -n "$2" ]; then
    TOOLS="$2/"
    NODE="$3"
  fi
fi

if [ "$1" != "v8" ]; then
  echo "Append ] at the end and generate callchain json"
  for X in `ls *trace*.txt`; do
    echo -e "\n]" >> $X

    ${TOOLS}${CONVERT} $X >__process-results__.tmp
    rm $X
    mv __process-results__.tmp $X
  done
fi

echo "Combine traces"
ls -1 *trace*.txt >__process-results__.tmp
${TOOLS}${MERGE} -l __process-results__.tmp >__process-results-trace__.json
rm __process-results__.tmp

if [ "$1" != "v8" ]; then
  echo "Update line info"
  ${NODE} ${TOOLS}lineinfo-update.js __process-results-trace__.json >__process-results__.tmp

  rm __process-results-trace__.json
  mv __process-results__.tmp __process-results-trace__.json
fi

rm *trace*.txt
mv __process-results-trace__.json full-trace.json.txt
