#!/bin/bash

# Allow CTRL+C to stop the container
trap cleanup 1 2 3 6 15

cleanup()
{
  echo "Caught Signal ... cleaning up."
  redis-cli shutdown
  echo "Done cleanup ... quitting."
  exit 1
}

# TODO: Proper redis config file
redis-server --daemonize yes

# Start the bit
dumb-init python telegram_bot/main.py &
  
# Start the service
# Using cd first to prevent the issue with open() & uvicorn --app-dir
cd service/src && uvicorn --host 0.0.0.0 main:app --log-level warning&
  
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?
