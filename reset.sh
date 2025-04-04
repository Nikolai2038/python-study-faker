#!/bin/sh

main() {
  ./psql.sh ./sql/01_reset.sql || return "$?"
  ./psql.sh ./sql/02_create_tables.sql || return "$?"
  ./psql.sh ./sql/03_fill_tables.sql || return "$?"
}

main "${@}" || exit "$?"
