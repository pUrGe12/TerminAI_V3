#!/bin/bash

cmd="$1"

if man -w "$cmd" &> /dev/null; then
    # Show man page without formatting
    man "$cmd" | col -b
else
    echo "No man page found for '$cmd'"
fi
