#!/bin/bash

set -e

if ! [ -x "$(command -v nc)" ]; then
    # Install tcp-port-wait.sh requirements
    apt-get update
    apt-get install -y netcat
fi

# Help text
if [ -z "$1" -o -z "$2" ]
then
    echo "tcp-port-wait - block until specified TCP port becomes available"
    echo "Usage: ntcp-port-wait HOST PORT"
    exit 1
fi

echo $(date -u) "- Waiting for port $1:$2 to become available..."

while ! nc -z $1 $2 2>/dev/null
do
    let elapsed=elapsed+1
    if [ "$elapsed" -gt 120 ]
    then
        echo $(date -u) "- Time out. $1:$2 could not be reached"
        exit 1
    fi
    sleep 1;
done

echo $(date -u) "- $1:$2 is ready"
