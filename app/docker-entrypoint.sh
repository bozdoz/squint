#!/bin/bash

set -ex

waitfor() {
  local CMD="$1"
  local DELAY=10
  local MAX_TRIES=3
  local n=0

  while true; do
    sh -c "$CMD" && break || {
      if [ $n -lt $MAX_TRIES ]; then
        n=$((n+1))
        echo "Command failed. Attempt $n/$MAX_TRIES:"
        sleep $DELAY;
      else
        echo "The command has failed after $n attempts."
        exit 1
      fi
    }
  done
}

# production or dev commands
if [ "$1" == 'gunicorn' ] || [[ "$@" == *"runserver"* ]]; then
  waitfor "python manage.py migrate && \
    python manage.py createsu && \
    mkdir -p static_root && \
    python manage.py collectstatic --no-input"
fi

# dev command (populate the database)
if [[ "$@" == *"runserver"* ]]; then
  waitfor "python manage.py loaddata **/fixtures/*.json"
fi

exec "$@"
