#!/bin/sh

main() {
  # ========================================
  # Generate ./sql/04_fill_tables.sql from ./sql/04_fill_tables.sql.example but with Python code
  # ========================================
  __sql_file_contents="$(cat ./sql/1_reset/04_fill_tables.sql.example)" || return "$?"

  # "True" or "False":
  # - Since "plpy.execute" does not support reading from STDIN, we always use "False" here
  __use_copy_instead_of_insert=False

  __python_file_contents="$(sed 's/print(sql)/plpy.execute(sql)/g;'"s/use_copy_instead_of_insert = .*/use_copy_instead_of_insert = ${__use_copy_instead_of_insert}/g" ./python/main.py)" || return "$?"

  # Replace placeholder
  __placeholder="PYTHON_CODE_PLACEHOLDER"

  __sql_file_contents_before="${__sql_file_contents%"${__placeholder}"*}" || return "$?"

  __sql_file_contents_after="${__sql_file_contents#*"${__placeholder}"}" || return "$?"

  __sql_file_contents="${__sql_file_contents_before}
${__python_file_contents}
${__sql_file_contents_after}"

  # shellcheck disable=SC2320
  echo "${__sql_file_contents}" > ./sql/1_reset/04_fill_tables.sql || return "$?"
  # ========================================

  ./shell/psql.sh ./sql/1_reset/01_wal_disable.sql || return "$?"
  sudo systemctl restart postgresql.service

  ./shell/psql.sh ./sql/1_reset/02_reset.sql || return "$?"
  ./shell/psql.sh ./sql/1_reset/03_create_tables.sql || return "$?"
  ./shell/psql.sh ./sql/1_reset/04_fill_tables.sql || return "$?"
  ./shell/psql.sh ./sql/1_reset/05_create_keys.sql || return "$?"
  ./shell/psql.sh ./sql/1_reset/06_analyze.sql || return "$?"

  ./shell/psql.sh ./sql/1_reset/07_wal_enable.sql || return "$?"
  sudo systemctl restart postgresql.service

  echo "Количество записей в каждой таблице:"
  ./shell/psql.sh ./sql/1_reset/08_print_counts.sql || return "$?"
}

main "${@}" || exit "$?"
