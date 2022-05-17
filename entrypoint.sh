#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

if [ "${SKIP_MIGRATIONS:-true}" != "true" ]; then
  echo "Running migrations..."
  alembic upgrade head
  echo "Database migrated"
fi

echo "Starting service"
gunicorn baracoda:create_app()
