from collections import UserDict

class Field:
    """Базовий клас для полів запису."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту (обов'язкове поле)."""
    pass


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією формату (10 цифр)."""
    def __init__(self, value):
        # Перевірка, що номер складається рівно з 10 цифр
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Номер телефону має складатися з 10 цифр.")
        super().__init__(value)


class Record:
    """Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []  # Список об'єктів Phone

    def add_phone(self, phone_str):
        """Додає номер телефону до запису."""
        phone_obj = Phone(phone_str)
        self.phones.append(phone_obj)

    def remove_phone(self, phone_str):
        """Видаляє номер телефону з запису."""
        for phone in self.phones:
            if phone.value == phone_str:
                self.phones.remove(phone)
                return f"Телефон {phone_str} видалено."
        return "Телефон не знайдено."

    def edit_phone(self, old_phone, new_phone):
        """Редагує номер телефону: замінює old_phone на new_phone."""
        for phone in self.phones:
            if phone.value == old_phone:
                # Створюємо новий об'єкт Phone для валідації нового номера
                new_phone_obj = Phone(new_phone)
                phone.value = new_phone_obj.value
                return f"Телефон {old_phone} змінено на {new_phone}."
        return "Телефон не знайдено."

    def find_phone(self, phone_str):
        """Пошук номера телефону в записі."""
        for phone in self.phones:
            if phone.value == phone_str:
                return phone.value
        return "Телефон не знайдено."

    def __str__(self):
        phones_str = '; '.join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    """Клас для зберігання та управління записами адресної книги."""
    def add_record(self, record):
        """Додає запис до адресної книги.
        Ключем є ім'я контакту у нижньому регістрі.
        """
        self.data[record.name.value.lower()] = record

    def find(self, name):
        """Знаходить запис за ім'ям (пошук нечутливий до регістру)."""
        return self.data.get(name.lower(), "Запис не знайдено.")

    def delete(self, name):
        """Видаляє запис за ім'ям (пошук нечутливий до регістру)."""
        if name.lower() in self.data:
            del self.data[name.lower()]
            return f"Запис {name} видалено."
        return "Запис не знайдено."


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print("Всі записи в адресній книзі:")
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    if isinstance(john, Record):
        print(john.edit_phone("1234567890", "1112223333"))
        print(john)  # Очікуване виведення: Contact name: John, phones: 1112223333; 5555555555

        # Пошук конкретного телефону у записі John
        found_phone = john.find_phone("5555555555")
        print(f"{john.name.value}: {found_phone}")  # Очікуване виведення: John: 5555555555

    # Видалення запису Jane
    print(book.delete("Jane"))
