#!/bin/sh

main() {
  if [ "$#" -lt 1 ]; then
    echo "Usage: ${0} <sql_file_path>" >&2
    return 1
  fi

  __file_name="${1}" && shift || return "$?"
  if [ -z "${__file_name}" ]; then
    echo "File \"${__file_name}\" does not exist!" >&2
    return 1
  fi

  # Close current connections
  PGPASSWORD='' psql --variable=ON_ERROR_STOP=on \
    --host=localhost \
    --port=5432 \
    --username=postgres \
    --dbname=postgres \
    -c "SELECT pg_terminate_backend(pid) FROM (SELECT pid FROM pg_stat_activity WHERE datname='ups_system_db');" || return "$?"

  # Execute SQL-file
  PGPASSWORD='' psql --variable=ON_ERROR_STOP=on \
    --host=localhost \
    --port=5432 \
    --username=postgres \
    --dbname=postgres \
    < "${__file_name}" || return "$?"
}

main "${@}" || exit "$?"
