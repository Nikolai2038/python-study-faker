# python-study-faker

Моё изучение построителя запросов PostgreSQL и интеграции PostgreSQL с Python (библиотека Faker для заполнения базы данных).

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

## 2. Запуск

### 2.1. Python

Запустить проект в IDE или командой:

```sh
./venv/bin/python main.py
```

### 2.2. SQL

#### 2.2.1. Сброс БД

```sh
./reset.sh
```
