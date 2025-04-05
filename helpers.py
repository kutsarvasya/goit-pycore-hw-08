import pickle
from classes import AddressBook, Record, UserExistsError, PhoneNotFoundError, ValueErrorChangePhone, ValuePhoneError, ValueBirthdayError


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "User not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
        except UserExistsError:
            return "This user already exists."
        except PhoneNotFoundError:
            return "Phone number not found."
        except ValueErrorChangePhone:
            return "Give me name and old phone and new phone please."
        except ValuePhoneError:
            return "the phone number is not correct"
        except ValueBirthdayError:
            return "Invalid date format. Use DD.MM.YYYY"

    return inner


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, phone = args
    user = Record(name)
    user.add_phone(phone)
    contacts.add_record(user)
    return "Contact added."


@input_error
def change_contact(args, contacts):
    if len(args) != 3:
        raise ValueErrorChangePhone
    name, old_phone, new_phone = args
    user = contacts.find(name)
    user.edit_phone(old_phone, new_phone)
    return 'Updated'


@input_error
def show_phone(args, contacts):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    user = contacts.find(name)
    return [phone.value for phone in user.phones]


@input_error
def show_contacts(contacts):
    for name, record in contacts.data.items():
        print(record)


@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError
    name, date = args
    user = book.find(name)
    user.add_birthday(date)
    return 'added'


@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    user = book.find(name)
    if user.birthday:
        return user.birthday.value
    else:
        return "Birthday not added"


@input_error
def birthdays(args, book):
    return book.get_upcomming_birthdays()
