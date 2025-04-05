-- Восстанавливаем значения по умолчанию
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET archive_mode = 'off';
ALTER SYSTEM SET max_wal_senders = 10;
-- Несмотря на перезагрузку конфигурации, всё равно потребуется перезапустить службу Postgres
SELECT pg_reload_conf();

-- -- Вывод значений - Способ 1
-- select * from pg_settings where name = 'wal_level';
-- select * from pg_settings where name = 'archive_mode';
-- select * from pg_settings where name = 'max_wal_senders';

-- Вывод значений - Способ 2
SHOW wal_level;
SHOW archive_mode;
SHOW max_wal_senders;
