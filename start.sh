#!/usr/bin/env bash

while IFS='' read -r line || [[ -n "$line" ]]; do
    export ${line}
done < $1

python src/server.py