#!/bin/sh

main() {
  # Create directory for dumps if not already
  mkdir --parents ./sql/0_dumps || return "$?"

  # Download dump
  PGPASSWORD='' pg_dump \
    --host=localhost \
    --port=5432 \
    --username=postgres \
    --dbname=imdb_test \
    --format=p \
    --encoding=UTF8 \
    --no-owner \
    --no-privileges \
    --clean \
    --create \
    --if-exists \
    --verbose \
    --compress=0 \
    --file="./sql/0_dumps/ups_system_db_dump_$(date +'%Y-%m-%d_%H-%M-%S').sql" || return "$?"
}

main "$@" || exit "$?"
