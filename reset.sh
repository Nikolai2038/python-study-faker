#!/bin/bash

function main() {
  # ========================================
  # Generate ./sql/03_fill_tables.sql from ./sql/03_fill_tables.sql.example but with Python code
  # ========================================
  local sql_file_contents
  sql_file_contents="$(cat ./sql/03_fill_tables.sql.example)" || return "$?"

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
  echo "${sql_file_contents}" > ./sql/03_fill_tables.sql || return "$?"
  # ========================================

  ./psql.sh ./sql/01_reset.sql || return "$?"
  ./psql.sh ./sql/02_create_tables.sql || return "$?"
  ./psql.sh ./sql/03_fill_tables.sql || return "$?"
}

main "${@}" || exit "$?"
