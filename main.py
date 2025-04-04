# ========================================
# Импортируем нужные пакеты
# ========================================
# Для генерации рандомных чисел
from random import Random

# Импортируем нужный пакет для фейкера
from faker import Faker

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

    print('retail_centers:')
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

        print('    id =', retail_center_id)
        print('    name =', name)
        print('    address =', address)

    print('shipped_items:')
    for item_num in range(shipped_items_number):
        retail_center_id = random.randint(1, retail_centers_number)

        # Вес между 1 и 30, два знака после запятой
        weight = round(random.uniform(0.1, 30.0), 2)

        dimension = round(random.uniform(100.0, 1000.0), 2)
        insurance_amt = round(random.uniform(500.0, 5000000.0), 2)
        destination = faker.address()
        final_delivery_date = faker.date()

        print('    item_num =', item_num)
        print('    weight =', weight)
        print('    dimension =', dimension)
        print('    insurance_amt =', insurance_amt)
        print('    destination =', destination)
        print('    final_delivery_date =', final_delivery_date)

    print('transportation_events:')
    for seq_number in range(transportation_events_number):
        transportation_event_type = faker.sentence(random.randint(1, 5))
        delivery_rout = faker.address()

        print('    seq_number =', seq_number)
        print('    type =', transportation_event_type)
        print('    delivery_rout =', delivery_rout)

    print('item_transportations:')
    for item_transportation_id in range(item_transportations_number):
        transportation_event_seq_number = random.randint(1, transportation_events_number)
        shipped_item_item_num = random.randint(1, shipped_items_number)

        # Размер текста должен быть не менее 5 символов для фейкера и не более 255, так как именно такое ограничение мы задаём в базе.
        # Заменяем переносы строк на пробелы - чтобы весь текст был на одной строке.
        comment = faker.text(
            max_nb_chars=random.randint(200, 255),
            ext_word_list=dictionary
        ).replace('\n', ' ')

        print('    transportation_event_seq_number =', transportation_event_seq_number)
        print('    comment =', comment)
        print('    shipped_item_item_num =', shipped_item_item_num)
