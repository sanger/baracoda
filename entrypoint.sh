#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

if [ "${SKIP_MIGRATIONS:-true}" != "true" ]; then
  echo "Running migrations..."
  flask db upgrade
  echo "Database migrated"
fi

echo "Starting service"
gunicorn baracoda:create_app()
