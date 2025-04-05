from collections import UserDict
from datetime import datetime, timedelta


class UserExistsError(Exception):
    pass


class PhoneNotFoundError(Exception):

    pass


class ValueErrorChangePhone(Exception):
    pass


class ValuePhoneError(Exception):
    pass


class ValueBirthdayError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValuePhoneError
        super().__init__(value)

    def is_valid(self, phone):
        return len(phone) == 10 and phone.isdigit()


class Birthday(Field):
    def __init__(self, value):
        try:
            date_object = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(date_object)
        except ValueBirthdayError:
            raise ValueBirthdayError


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
            else:
                raise PhoneNotFoundError

    def add_birthday(self, value):

        self.birthday = Birthday(value)

    def add_phone(self, value):

        self.phones.append(Phone(value))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                print(f"Phone number {phone} removed.")
                return
        raise PhoneNotFoundError

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        raise PhoneNotFoundError

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value in self.data:
            raise UserExistsError
        self.data[record.name.value] = record

    def find(self, name):
        record = self.data.get(name)
        if not record:
            raise KeyError
        return record

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            print(f"contact {name} removed.")
        else:
            raise KeyError

    def get_upcomming_birthdays(self):

        user_birthday = []
        today = datetime.today().date()

        for _, user in self.data.items():

            if user.birthday:

                birthday_this_year = user.birthday.value.replace(
                    year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = user.birthday.value.replace(
                        year=today.year+1)
                days_until_birthday = (birthday_this_year - today).days

                if days_until_birthday <= 7:

                    if birthday_this_year.weekday() == 5:
                        birthday_this_year += timedelta(days=2)

                    if birthday_this_year.weekday() == 6:
                        birthday_this_year += timedelta(days=1)

                    user_birthday.append(
                        {"name": user.name.value, 'congratulation_date': birthday_this_year.strftime("%Y.%m.%d")})
        return user_birthday


# # # Створення нової адресної книги
# book = AddressBook()

# # # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")

# # # Додавання запису John до адресної книги
# book.add_record(john_record)

# # # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# john_record.add_birthday('01.04.2022')
# book.add_record(jane_record)


# # #     # Знаходження та редагування телефону для John
# # john = book.find("John")
# # john.edit_phone("1234567890", "1112223333")

# # john.remove_phone('1112223333')
# # print(john)


# # # Виведення: Contact name: John, phones: 1112223333; 5555555555

# # # Пошук конкретного телефону у записі John
# # found_phone = john.find_phone("5555555555")
# # print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# # # Видалення запису Jane
# # book.delete("Jane")
# print(book.get_upcomming_birthdays())
# # for name, record in book.data.items():
# #     print(record)
