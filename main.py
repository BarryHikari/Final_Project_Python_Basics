from collections import UserDict, defaultdict
from datetime import datetime, timedelta
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if value:  
            self.value = value
        else:
            raise ValueError("Name field is required")

class Phone(Field):
    def __init__(self, value):
        if self.validate_phone(value):
            self.value = value
        else:
            raise ValueError("Invalid phone number: must be 10 digits")
    
    def validate_phone(self, phone):
        return len(str(phone)) == 10
    
class Email(Field):
    def __init__(self, value):
        if self.validate_email(value):
            self.value = value
        else:
            raise ValueError("Invalid email address")
    
    def validate_email(self, email):
        # Basic email validation, can be improved
        return "@" in email and "." in email
    
class Address(Field):
    def __init__(self, value):
        self.value = value

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

class Notes(Field):
    def __init__(self, value, tags=None):
        super().__init__(value)
        self.tags = set(tags) if tags else set()

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.discard(tag)

    def has_tags(self, tags):
        """Sprawdź, czy notatka zawiera wszystkie tagi z listy `tags`."""
        return self.tags.issuperset(tags)
    
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


class Birthday(Field):
    def __init__(self, value):
        if len(value) != 10 or not datetime.strptime(value, "%d.%m.%Y"):
            raise ValueError("Invalidd birthday format. DD.MM.YYYY required")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.addresses = []
        self.birthday = None
        self.notes = []

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    def add_note(self, note, tags=None):
        new_note = Notes(note, tags)
        self.notes.append(new_note)
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        
    def add_email(self, email):
        self.emails.append(Email(email))
        
    def add_address(self, address):
        self.addresses.append(Address(address))

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)

    def __str__(self):
        phone_info = '; '.join(str(p) for p in self.phones)
        email_info = '; '.join(str(e) for e in self.emails)
        address_info = '; '.join(str(a) for a in self.addresses)
        birthday_info = f"Birthday: {self.birthday.value}" if self.birthday else "No birthday set"
        return f"Contact name: {self.name.value}, phones: {phone_info}, emails: {email_info}, address: {address_info}, {birthday_info}"

class AddressBook(UserDict):

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
    def find_notes_by_tags(self, tags):
        """Znajdź wszystkie notatki zawierające wszystkie podane tagi."""
        found_notes = []
        for record in self.data.values():
            for note in record.notes:
                if note.has_tags(tags):
                    found_notes.append(note)
        return found_notes
    
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)

    def findname(self, name):
        found_contacts = []
        for contact_name, record in self.data.items():
            if name in contact_name:
                found_contacts.append(record)
        return found_contacts if found_contacts else None

    def remove_phone(self, name):
        if name in self.data:
            del self.data[name]
            print(f"Contact {name} deleted.")
        else:
            print("Contact not found.")

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def get_birthdays_per_week(self):
        birthdays_per_week = defaultdict(list)
        today = datetime.today().date()
        monday_of_next_week = today + timedelta(days=(7 - today.weekday()))
        for name, record in self.data.items():
            if record.birthday:
                birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                delta_days = (birthday_this_year - today).days
                birthday_weekday = birthday_this_year.weekday()
                if birthday_weekday >= 5:
                    birthday_weekday = 0  
                if delta_days < 7 : 
                    birthday_weekday_name = (monday_of_next_week + timedelta(days=birthday_weekday)).strftime("%A")
                    birthdays_per_week[birthday_weekday_name].append(name)
                    
        if any(birthdays_per_week.values()):
            print("Birthdays in the next week:")
            for day, names in birthdays_per_week.items():
                if names:
                    print(f"{day}: {', '.join(names)}")
        else:
            print("No birthdays in the next week.")

    def when_birthdays(book):
        today = datetime.today().date()
        for record in book.data.values():
            if record.birthday:
                birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                next_birthday = birthday.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)
                days_until_birthday = (next_birthday - today).days
                print(f"{record.name.value}'s birthday is on {record.birthday.value}. It's in {days_until_birthday} days.")

    def remove_contact(self, name):
        if name in self.data:
            del self.data[name]
            print(f"Contact {name} deleted.")
        else:
            print("Contact not found.")

    def remove_birthday(self, name):
        record = self.find(name)
        if record:
            if record.birthday:
                record.birthday = None
                print(f"Birthday removed for contact {name}")
            else:
                print(f"No birthday set for {name}")
        else:
            print(f"Contact {name} not found.")
            
def load_address_book_from_file(filename):
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        address_book = AddressBook()
        address_book.data = data
        return address_book
    except (FileNotFoundError, EOFError):
        return AddressBook()

def parse_input(user_input):
    try:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, args
    except ValueError:
        return None, None



def main():
    Globalfilename = 'Myaddressbook.dat'
    book = load_address_book_from_file(Globalfilename)
    print("Welcome to the assistant bot!")
    
    ''' 
        Start assistant commands:
        comand lists: add, remove_phone, change_phone, add_phone, add_email, add_address, phone, all, add_birthday, show_birthday, birthdays, hello, exit, close
    ''' 
    while True:
        user_input = input("Enter command: ").strip()
        command, args = parse_input(user_input)
        


        if command == "add":
            try:
                name, phone, email, address, *optional_args = args
                record = Record(name)
                record.add_phone(phone)
                record.add_email(email)
                record.add_address(address)             
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                if optional_args:
                    note = optional_args[0]
                    tags = optional_args[1:]  # Może być pusta, jeśli nie podano tagów
                    record.add_note(note, tags)
                    print(f"Contact {name} added with phone number {phone}, email {email}, address {address}, note: {note}, and tags: {' '.join(tags)}")
                else:
                    print(f"Contact {name} added with phone number {phone}, email {email}, and address {address}")
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                
                book.add_record(record)

            except ValueError as e:
                print(e)
                print("Invalid command format. Use 'add [name] [phone] [email] [address] [optional: note] [optional: tags...]'")

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                
        elif command == "add_note":
            try:
                name, note_content = args[0], args[1]
                tags = args[2:]
                record = book.find(name)
                if record:
                    record.add_note(note_content, tags)
                    print(f"Added note to {name}: {note_content} with tags: {', '.join(tags)}")
                else:
                    print(f"Contact {name} not found")
            except ValueError as e:
                print(e)
                print("Invalid command format. Use 'add_note [name] [note] [tag1] [tag2] ...'")

        elif command == "add_tag":
            try:
                name, note_index, tag = args
                note_index = int(note_index)  # Zakładając, że notatki są numerowane od 0
                record = book.find(name)
                if record:
                    record.notes[note_index].add_tag(tag)
                    print(f"Tag '{tag}' added to note {note_index} of contact {name}.")
                else:
                    print(f"Contact {name} not found.")
            except (ValueError, IndexError) as e:
                print(e)
                print("Invalid command format. Use 'add_tag [name] [note_index] [tag]'")

        elif command == "remove_tag":
            try:
                name, note_index, tag = args
                note_index = int(note_index)
                record = book.find(name)
                if record:
                    record.notes[note_index].remove_tag(tag)
                    print(f"Tag '{tag}' removed from note {note_index} of contact {name}.")
                else:
                    print(f"Contact {name} not found.")
            except (ValueError, IndexError) as e:
                print(e)
                print("Invalid command format. Use 'remove_tag [name] [note_index] [tag]'")

        elif command == "search_notes_by_tags":
            try:
                tags = args  # Przyjmuje wszystkie podane tagi
                found_notes = book.find_notes_by_tags(tags)
                if found_notes:
                    print("Found notes with specified tags:")
                for note in found_notes:
                    print(f"Note: {note.value}, Tags: {', '.join(note.tags)}")
                else:
                    print("No notes found matching the specified tags.")
            except ValueError as e:
                print(e)
                print("Invalid command format. Use 'search_notes_by_tags [tag1] [tag2] ...'")

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        elif command == "search":
            try:
                name = args[0]
                found_contacts = book.findname(name)
                if found_contacts:
                    print("Found contacts:")
                    for contact in found_contacts:
                        print(contact)
                else:
                    print("No contacts found matching the search criteria.")
            except IndexError:
                print("Invalid command format. Use 'search [name]'")

        elif command == "remove_phone":
            try:
                name, phone = args
                record = book.find(name)
                if record:
                    phone_found = record.find_phone(phone)
                    if phone_found:
                        record.remove_phone(phone)
                        record.add_phone("0000000000") #not remove only replace to 0000000000
                        print(f"Phone number {phone} removed for contact {name}.")
                    else:
                        print(f"Phone number {phone} not found for contact {name}.")
                else:
                    print(f"Contact {name} not found.")

            except ValueError as e:
                print(e)
                print("Invalid command format. Use 'remove-phone [name] [phone]'")

        elif command == "change_phone":
            try:
                name, old_phone, new_phone = args
                record = book.find(name)
                if record:
                    record.edit_phone(old_phone, new_phone)
                    print(f"Phone number changed from {old_phone} to {new_phone} for contact {name}")
                else:
                    print(f"Contact {name} not found")
            except ValueError as e:
                print(e)
                print("Invalid command format. Use 'change-phone [name] [old phone] [new phone]'")

        elif command == "add_phone":
            try:
                name, phone = args
                record = book.find(name)
                if record:
                    record.add_phone(phone)
                    print(f"Phone number {phone} added for contact {name}")
                else:
                    print(f"Contact {name} not found")
            except ValueError as e:
                print(e)
                print("Invalid command format. Use 'add-phone [name] [phone]'")

        elif command == "add_email":
            try:
                name, email = args
                record = book.find(name)
                if record:
                    record.add_email(email)
                    print(f"Email {email} added for contact {name}")
                else:
                    print(f"Contact {name} not found")
            except ValueError as e:
                print(e)
                print("Invalid command format. Use 'add-email [name] [email]'")

        elif command == "add_address":
            try:
                name, address = args
                record = book.find(name)
                if record:
                    record.add_address(address)
                    print(f"Address {address} added for contact {name}")
                else:
                    print(f"Contact {name} not found")
            except ValueError as e:
                print(e)
                print("Invalid command format. Use 'add-address [name] [address]'")

        elif command == "phone":
            try:
                name = args[0]
                record = book.find(name)
                if record:
                    print(f"Phone numbers for {name}: {', '.join(str(p) for p in record.phones)}")
                else:
                    print(f"Contact {name} not found.")
            except IndexError as e:
                print(e)
                print("Invalid command format. Use 'phone [name]'")

        elif command == "all":
            if book.data:
                print("All contacts:")
                for record in book.data.values():
                    print(record)
            else:
                print("No contacts in the address book.")

        elif command == "add_birthday":
            try:
                name, birthday = args
                record = book.find(name)
                if record:
                    record.add_birthday(birthday)
                    print(f"Birthday added for contact {name}")
                else:
                    print(f"Contact {name} not found")
                    
            except ValueError as e:
                print(e)
                print("Invalid command format. Use 'add-birthday [name] [birth date]'")

        elif command == "show_birthday":
            try:
                name = args[0]
                record = book.find(name)
                if record and record.birthday:
                    print(f"Birthday for {name}: {record.birthday}")
                elif record and not record.birthday:
                    print(f"No birthday set for {name}")
                else: 
                    print(f"Contact {name} not found.")
            except IndexError as e:
                print(e)
                print("Invalid command format. Use 'show-birthday [name]'")

        elif command == "birthdays":
            book.get_birthdays_per_week()
            
        elif command == "when_birthdays":
            book.when_birthdays()

        elif command == "delete_contact":
            try:
                name = args[0]
                book.remove_birthday(name)
                book.remove_contact(name)
            except IndexError:
                print("Invalid command format. Use 'delete_contact [name]'")

        elif command == "hello":
            print("How can I help you?")
        
        elif command in ["close", "exit"]:
            print("Goodbye!")
            book.save_to_file(Globalfilename)
            print("Saving address book and closing the app.")
            break

        else:
            print("Invalid command. Please try again")

if __name__ == "__main__":
    main()
