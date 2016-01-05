#!/usr/bin/env bash

while IFS='' read -r line || [[ -n "$line" ]]; do
    export ${line}
done < opt/$1

python src/server.py