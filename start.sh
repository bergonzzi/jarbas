#!/usr/bin/env bash

while IFS='' read -r line || [[ -n "$line" ]]; do
    export ${line}
done < opt/auth.conf

python src/server.py