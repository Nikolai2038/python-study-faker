from faker import Faker

faker = Faker()


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi(faker.first_name())
