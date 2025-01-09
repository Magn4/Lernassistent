#!/bin/bash

# wait-for-it.sh

# Usage: wait-for-it.sh host:port -- command

TIMEOUT=15
QUIET=0
HOST=$1
PORT=$2
shift 2
CMD=$@

# Check if command is provided
if [[ -z "$CMD" ]]; then
  echo "No command provided"
  exit 1
fi

# Check if host and port are provided
if [[ -z "$HOST" || -z "$PORT" ]]; then
  echo "Usage: wait-for-it.sh <host>:<port> -- <command>"
  exit 1
fi


# Wait for the service to be available
echo "Waiting for $HOST:$PORT..."

# Loop to check if the service is available
until nc -z -v -w30 $HOST $PORT; do
  if [[ $QUIET -eq 0 ]]; then
    echo "Waiting for $HOST:$PORT..."
  fi
  sleep 1
done

echo "$HOST:$PORT is available."

# Execute the provided command
exec $CMD