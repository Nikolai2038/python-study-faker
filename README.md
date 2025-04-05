# python-study-faker

Моё изучение построителя запросов PostgreSQL и интеграции PostgreSQL с Python (библиотека Faker для заполнения базы
данных).

## 1. Подготовка

1. Склонировать проект и перейти в папку с ним;
2. Инициализировать `venv`:

    ```sh
    python -m venv ./venv
    ```

3. Установить все зависимости:

   ```sh
   ./venv/bin/pip install -r requirements.txt
   ```

## 2. Настройка

Настройки можно поменять в файле `./main.py`:

```python
retail_centers_number = 10
shipped_items_number = 1000000
transportation_events_number = 10
item_transportations_number = shipped_items_number * transportation_events_number

retail_centers_number_parts = 1
shipped_items_number_parts = 100
transportation_events_number_parts = 1
item_transportations_number_parts = shipped_items_number_parts

# Количество слов в словаре для заполнения поля "comment" в таблице "item_transportations"
words_in_dictionary = 1000
```

## 3. Запуск

### 3.1. Вывод SQL-команд

Запустить проект в IDE или командой:

```sh
./venv/bin/python main.py
```

Вставки выводятся при помощи метода `COPY`.
Чтобы выводить `INSERT`, в файле `./main.py` изменить `use_copy_instead_of_insert` с `True` на `False`.

### 3.2. Выполнение SQL-команд

```sh
./reset.sh
```

Будет использовать вставки `INSERT` (всегда задаёт `use_copy_instead_of_insert = False`), так как `plpy.execute` не поддерживает чтение из `STDIN`

### 3.3. Создание полного дампа БД

```sh
./pg_dump.sh
```

Дамп будет создан в папке `./dumps`

### 3.4. Выполнение конкретного SQL-файла

```sh
./psql.sh <sql_file_path>
```

Данную команду также можно использовать для применения дампа - например:

```sh
/psql.sh ./dumps/ups_system_db_dump_2025-04-04_23-30-34.sql
```
