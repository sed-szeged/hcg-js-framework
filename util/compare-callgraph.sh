#!/bin/bash

# Convenience script for quick comparison

SCRIPT_PATH="`dirname \"$0\"`"

SUMMARY=""
if [ "$1" = "-s" ]; then
  SUMMARY="-s"
  shift
fi

if [ -z $1 ] || [ ! -f $1 ]; then
  echo "Input file1 not found"
  echo "Usage: compare-callgraph.sh file1 file2"
  exit 1
fi

if [ -z $2 ] || [ ! -f $1 ]; then
  echo "Input file2 not found"
  echo "Usage: compare-callgraph.sh file1 file2"
  exit 1
fi

if [ ! -f $SCRIPT_PATH/collect-nodes.py ]; then
  echo "The collect-nodes.py script does not found"
  exit 1
fi

if [ ! -f $SCRIPT_PATH/callgraph-rebase.py ]; then
  echo "The callgraph-rebase.py script does not found"
  exit 1
fi

if [ ! -f $SCRIPT_PATH/compare-callgraph.py ]; then
  echo "The compare-callgraph.py script does not found"
  exit 1
fi

TMP_DIR="`dirname \"$1\"`"

$SCRIPT_PATH/collect-nodes.py $1 $2 >$TMP_DIR/__NODES__.$1

EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "The collect-nodes.py script failed to run"
    exit 1
fi

$SCRIPT_PATH/callgraph-rebase.py $TMP_DIR/__NODES__.$1 $1 >$TMP_DIR/__REBASED1__.$1

EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "The callgraph-rebase.py script failed to run"
    exit 1
fi

$SCRIPT_PATH/callgraph-rebase.py $TMP_DIR/__NODES__.$1 $2 >$TMP_DIR/__REBASED2__.$2

EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "The callgraph-rebase.py script failed to run"
    exit 1
fi

$SCRIPT_PATH/compare-callgraph.py $SUMMARY $TMP_DIR/__REBASED1__.$1 $TMP_DIR/__REBASED2__.$2

rm __NODES__.$1 __REBASED1__.$1 __REBASED2__.$2
