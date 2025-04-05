# ========================================
# Импортируем нужные пакеты
# ========================================
# Для генерации рандомных чисел
from random import Random

# Импортируем нужный пакет для фейкера
from faker import Faker

# ========================================

# ========================================
# Инициализируем рандомайзеры
# ========================================
seed = 0

# Инициализация генератора случайных чисел
random = Random(seed)

# Указываем ключ генерации, чтобы при каждом вызове программы получать один и тот же результат
Faker.seed(seed)

# Инициализация фейкера:
# - Используем русскую локаль;
# - Отключаем разброс по частоте в реальном мире - для оптимизации.
faker = Faker('ru_RU', use_weighting=False)
# ========================================

# ========================================
# Settings
# ========================================
use_copy_instead_of_insert = True

# CSV delimiter for "COPY" commands
csv_delimiter = '|'

retail_centers_number = 10
shipped_items_number = 1000000
transportation_events_number = 10
item_transportations_number = shipped_items_number * transportation_events_number

# Будем использовать итерации, так как за раз может не хватить оперативной памяти
retail_centers_number_parts = 1
shipped_items_number_parts = 100
transportation_events_number_parts = 1
item_transportations_number_parts = shipped_items_number_parts

# Количество слов в словаре для заполнения поля "comment" в таблице "item_transportations"
words_in_dictionary = 1000


# ========================================

# Добавляет в указанную таблицу указанное количество строк, заполняя указанные столбцы при помощи указанной лямбда-функции
def fill_table(table_name, data_count, data_count_parts, field_names, generate_row):
    if (data_count % data_count_parts) != 0:
        raise ValueError("Data count must be divisible by data count parts")

    data_count_part_size = data_count // data_count_parts

    print(data_count_part_size)
    for data_iteration in range(data_count_parts):
        data_rows = []

        # Generate data
        for i in range(data_count_part_size):
            row = generate_row(data_count_part_size * data_iteration + i)
            if use_copy_instead_of_insert:
                data_rows.append(csv_delimiter.join(map(str, row)))
            else:
                data_rows.append(f"({', '.join(repr(v) for v in row)})")

        # Generate SQL
        if use_copy_instead_of_insert:
            sql = f"""COPY {table_name} ({', '.join(field_names)}) FROM STDIN WITH (FORMAT csv, DELIMITER '{csv_delimiter}', HEADER false);
{"\n".join(data_rows)}
\\."""
        else:
            sql = f"""INSERT INTO {table_name} ({', '.join(field_names)}) VALUES {", ".join(data_rows)};"""

        # This will be:
        # - In Python: Print SQL;
        # - In SQL: This will be replaced with "plpy.execute(sql)".
        print(sql)


# Генерирует название организации
def generate_retail_center():
    organization_type_id = random.randint(1, 4)
    if organization_type_id == 1:
        organization_type = 'ИП'
        name = faker.name()
    else:
        if organization_type_id == 2:
            organization_type = 'ЗАО'
        elif organization_type_id == 3:
            organization_type = 'ОАО'
        else:
            organization_type = 'ООО'

        name = ' '.join(faker.words(random.randint(1, 3))).title()

    return organization_type + ' "' + name + '"'


if __name__ == '__main__':
    # "retail_centers"
    fill_table(
        "retail_centers",
        retail_centers_number,
        retail_centers_number_parts,
        ['id', 'name', 'address'],
        lambda i: (
            i + 1,
            generate_retail_center(),
            faker.address()
        )
    )

    # "shipped_items"
    fill_table(
        "shipped_items",
        shipped_items_number,
        shipped_items_number_parts,
        ['item_num', 'retail_center_id', 'weight', 'dimension', 'insurance_amt', 'destination',
         'final_delivery_date'],
        lambda i: (
            i + 1,
            random.randint(1, retail_centers_number),
            round(random.uniform(0.1, 30.0), 2),
            round(random.uniform(100.0, 1000.0), 2),
            random.uniform(50, 5000) * 1000,
            faker.address(),
            faker.date()
        )
    )

    # "transportation_events"
    fill_table(
        "transportation_events",
        transportation_events_number,
        transportation_events_number_parts,
        ['seq_number', 'type', 'delivery_route'],
        lambda i: (
            i + 1,
            faker.sentence(random.randint(1, 5)),
            faker.address()
        )
    )

    # Генерируем словарь для заполнения поля "comment" в таблице "item_transportations"
    dictionary = faker.words(words_in_dictionary)

    # "item_transportations"
    fill_table(
        "item_transportations",
        item_transportations_number,
        item_transportations_number_parts,
        ['transportation_event_seq_number', 'shipped_item_item_num', 'comment'],
        lambda i: (
            (i % transportation_events_number) + 1,
            (i // transportation_events_number) + 1,
            faker.text(
                max_nb_chars=random.randint(200, 255),
                ext_word_list=dictionary
            ).replace('\n', ' ')
        )
    )
