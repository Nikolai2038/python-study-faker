#!/bin/bash

function main() {
  # ========================================
  # Generate ./sql/04_fill_tables.sql from ./sql/04_fill_tables.sql.example but with Python code
  # ========================================
  local sql_file_contents
  sql_file_contents="$(cat ./sql/04_fill_tables.sql.example)" || return "$?"

  # "True" or "False":
  # - Since "plpy.execute" does not support reading from STDIN, we always use "False" here
  local use_copy_instead_of_insert=False

  local python_file_contents
  python_file_contents="$(sed 's/print(sql)/plpy.execute(sql)/g;'"s/use_copy_instead_of_insert = .*/use_copy_instead_of_insert = ${use_copy_instead_of_insert}/g" ./main.py)" || return "$?"

  # Replace placeholder
  local placeholder="PYTHON_CODE_PLACEHOLDER"

  local sql_file_contents_before
  sql_file_contents_before="${sql_file_contents%"${placeholder}"*}" || return "$?"

  local sql_file_contents_after
  sql_file_contents_after="${sql_file_contents#*"${placeholder}"}" || return "$?"

  sql_file_contents="${sql_file_contents_before}
${python_file_contents}
${sql_file_contents_after}"

  # shellcheck disable=SC2320
  echo "${sql_file_contents}" > ./sql/04_fill_tables.sql || return "$?"
  # ========================================

  ./psql.sh ./sql/01_wal_disable.sql || return "$?"
  sudo systemctl restart postgresql.service

  ./psql.sh ./sql/02_reset.sql || return "$?"
  ./psql.sh ./sql/03_create_tables.sql || return "$?"
  ./psql.sh ./sql/04_fill_tables.sql || return "$?"
  ./psql.sh ./sql/05_create_keys.sql || return "$?"
  ./psql.sh ./sql/06_analyze.sql || return "$?"

  ./psql.sh ./sql/07_wal_enable.sql || return "$?"
  sudo systemctl restart postgresql.service

  echo "Количество записей в каждой таблице:"
  ./psql.sh ./sql/08_print_counts.sql || return "$?"
}

main "${@}" || exit "$?"
