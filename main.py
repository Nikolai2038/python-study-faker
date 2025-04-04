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

use_copy_instead_of_insert = True
csv_delimiter = '|'

if __name__ == '__main__':
    # TODO: Нужно 10 записей
    retail_centers_number = 3
    # TODO: Нужно 1 млн. записей
    shipped_items_number = 3
    # TODO: Нужно 10 записей
    transportation_events_number = 3
    # TODO: Нужно 10 млн. записей
    item_transportations_number = 3

    # Количество слов в словаре для заполнения поля "comment" в таблице "item_transportations"
    words_in_dictionary = 1000

    # Генерируем словарь для заполнения поля "comment" в таблице "item_transportations"
    dictionary = faker.words(words_in_dictionary)

    # ========================================
    # "retail_centers"
    # ========================================
    retail_centers_data = []

    # DEBUG:
    # print('retail_centers:')

    for retail_center_id in range(retail_centers_number):
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

        name = organization_type + ' "' + name + '"'
        address = faker.address()

        # DEBUG:
        # print('    id =', retail_center_id)
        # print('    name =', name)
        # print('    address =', address)

        if use_copy_instead_of_insert:
            retail_centers_data.append(f"{retail_center_id}{csv_delimiter}{name}{csv_delimiter}{address}")
        else:
            retail_centers_data.append(f"({retail_center_id}, '{name}', '{address}')")

    if use_copy_instead_of_insert:
        sql = f"""COPY retail_centers (id, name, address) FROM STDIN WITH (FORMAT csv, DELIMITER '{csv_delimiter}', HEADER false);
{"\n".join(retail_centers_data)}
\\."""
    else:
        sql = f"""INSERT INTO retail_centers (id, name, address) VALUES {",".join(retail_centers_data)};"""

    print(sql)
    # plpy.execute(sql)
    # ========================================

    # ========================================
    # "shipped_items"
    # ========================================
    shipped_items_data = []

    # DEBUG:
    # print('shipped_items:')

    for item_num in range(shipped_items_number):
        retail_center_id = random.randint(1, retail_centers_number)

        # Вес между 1 и 30, два знака после запятой
        weight = round(random.uniform(0.1, 30.0), 2)

        dimension = round(random.uniform(100.0, 1000.0), 2)
        insurance_amt = round(random.uniform(500.0, 5000000.0), 2)
        destination = faker.address()
        final_delivery_date = faker.date()

        # DEBUG:
        # print('    item_num =', item_num)
        # print('    weight =', weight)
        # print('    dimension =', dimension)
        # print('    insurance_amt =', insurance_amt)
        # print('    destination =', destination)
        # print('    final_delivery_date =', final_delivery_date)

        if use_copy_instead_of_insert:
            shipped_items_data.append(f"{item_num}{csv_delimiter}{retail_center_id}{csv_delimiter}{weight}{csv_delimiter}{dimension}{csv_delimiter}{insurance_amt}{csv_delimiter}{destination}{csv_delimiter}{final_delivery_date}")
        else:
            shipped_items_data.append(f"({item_num}, '{retail_center_id}', '{weight}', '{dimension}', '{insurance_amt}', '{destination}', '{final_delivery_date}')")

    if use_copy_instead_of_insert:
        sql = f"""COPY shipped_items (item_num, retail_center_id, weight, dimension, insurance_amt, destination, final_delivery_date) FROM STDIN WITH (FORMAT csv, DELIMITER '{csv_delimiter}', HEADER false);
{"\n".join(shipped_items_data)}
\\."""
    else:
        sql = f"""INSERT INTO shipped_items (item_num, retail_center_id, weight, dimension, insurance_amt, destination, final_delivery_date) VALUES {",".join(shipped_items_data)};"""

    print(sql)
    # plpy.execute(sql)
    # ========================================

    # ========================================
    # "transportation_events"
    # ========================================
    transportation_events_data = []

    # DEBUG:
    # print('transportation_events:')

    for seq_number in range(transportation_events_number):
        transportation_event_type = faker.sentence(random.randint(1, 5))
        delivery_rout = faker.address()

        # DEBUG:
        # print('    seq_number =', seq_number)
        # print('    type =', transportation_event_type)
        # print('    delivery_rout =', delivery_rout)

        if use_copy_instead_of_insert:
            transportation_events_data.append(f"{seq_number}{csv_delimiter}{transportation_event_type}{csv_delimiter}{delivery_rout}")
        else:
            transportation_events_data.append(f"({seq_number}, '{transportation_event_type}', '{delivery_rout}')")

    if use_copy_instead_of_insert:
        sql = f"""COPY transportation_events (seq_number, type, delivery_route) FROM STDIN WITH (FORMAT csv, DELIMITER '{csv_delimiter}', HEADER false);
{"\n".join(transportation_events_data)}
\\."""
    else:
        sql = f"""INSERT INTO transportation_events (seq_number, type, delivery_route) VALUES {",".join(transportation_events_data)};"""

    print(sql)
    # plpy.execute(sql)
    # ========================================

    # ========================================
    # "item_transportations"
    # ========================================
    item_transportations_data = []

    # DEBUG:
    # print('item_transportations:')

    for item_transportation_id in range(item_transportations_number):
        transportation_event_seq_number = random.randint(1, transportation_events_number)
        shipped_item_item_num = random.randint(1, shipped_items_number)

        # Размер текста должен быть не менее 5 символов для фейкера и не более 255, так как именно такое ограничение мы задаём в базе.
        # Заменяем переносы строк на пробелы - чтобы весь текст был на одной строке.
        comment = faker.text(
            max_nb_chars=random.randint(200, 255),
            ext_word_list=dictionary
        ).replace('\n', ' ')

        # DEBUG:
        # print('    transportation_event_seq_number =', transportation_event_seq_number)
        # print('    comment =', comment)
        # print('    shipped_item_item_num =', shipped_item_item_num)

        if use_copy_instead_of_insert:
            item_transportations_data.append(f"{transportation_event_seq_number}{csv_delimiter}{shipped_item_item_num}{csv_delimiter}{comment}")
        else:
            item_transportations_data.append(f"({transportation_event_seq_number}, '{shipped_item_item_num}', '{comment}')")

    if use_copy_instead_of_insert:
        sql = f"""COPY item_transportations (transportation_event_seq_number, shipped_item_item_num, comment) FROM STDIN WITH (FORMAT csv, DELIMITER '{csv_delimiter}', HEADER false);
{"\n".join(item_transportations_data)}
\\."""
    else:
        sql = f"""INSERT INTO item_transportations (transportation_event_seq_number, shipped_item_item_num, comment) VALUES {",".join(item_transportations_data)};"""

    print(sql)
    # plpy.execute(sql)
    # ========================================
