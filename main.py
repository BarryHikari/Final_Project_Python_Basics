from collections import UserDict, defaultdict
from datetime import datetime, timedelta
import pickle
from difflib import get_close_matches

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

class Notes(Field):
    def __init__(self, value):
        self.value = value

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
        self.notes = {} #Create dictionary to make notes and his tags.
        self.birthday = None

    def add_notes(self, note, tags):
        self.notes[note] = tags

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

    def edit_notes(self, old_note, new_note, new_tags=None):
        if old_note in self.notes:
            self.notes[new_note] = new_tags if new_tags is not None else self.notes[old_note]
            if old_note != new_note:
                del self.notes[old_note]
            print(f"Note edited successfully: {new_note}. Tags: {', '.join(new_tags if new_tags else [])}")
        else:
            print(f"Note '{old_note}' not found.")

    def delete_notes(self, note):
        if note in self.notes:
            del self.notes[note]
            print(f"Note '{note}' deleted successfully.")
        else:
            print(f"Note '{note}' not found.")

    def __str__(self):
        phone_info = '; '.join(str(p) for p in self.phones)
        email_info = '; '.join(str(e) for e in self.emails)
        address_info = '; '.join(str(a) for a in self.addresses)
        note_info = ''.join(f"{note}. TAGI: {', '.join(tags)}\n" for note, tags in self.notes.items())
        birthday_info = f"Birthday: {self.birthday.value}" if self.birthday else "No birthday set"
        return f"--------------------\nContact name: {self.name.value}, phones: {phone_info}, emails: {email_info}, address: {address_info}, {birthday_info}\nNotes:\n{note_info}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)

    def findname(self, name):
        name_lower = name.lower()  # Przekształć szukane imię do małych liter
        found_contacts = []
        for contact_name, record in self.data.items():
            if name_lower in contact_name.lower():  # Porównaj ignorując wielkość liter
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

    def find_notes_by_tag(self, tag):
        tag_lower = tag.lower()  # Przekształć szukany tag do małych liter
        found_notes = []
        for record in self.data.values():
            for note, tags in record.notes.items():
                # Przekształć tagi z notatek do małych liter przy porównywaniu
                if tag_lower in [t.lower() for t in tags]:
                    found_notes.append((record.name.value, note))
        return found_notes

    def find_contacts_by_tag(self, tag):
        tag_lower = tag.lower()  # Przekształć szukany tag do małych liter
        found_contacts = set()
        for record in self.data.values():
            for _, tags in record.notes.items():
                # Przekształć tagi z notatek do małych liter przy porównywaniu
                if tag_lower in [t.lower() for t in tags]:
                    found_contacts.add(record.name.value)
                    break  # Once a contact with the tag is found, break the loop
        return list(found_contacts)


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

def intelligent_analysis(command, available_commands):
    closest_match = get_close_matches(command, available_commands)
    if closest_match:
        return closest_match[0]
    else:
        return None

def main():
    Globalfilename = 'Myaddressbook3.dat'
    book = load_address_book_from_file(Globalfilename)
    print("Welcome to the assistant bot!")
    
    ''' 
        Start assistant commands:
        comand lists: ["add", "remove_phone", "change_phone", "add_phone", "add_email", "add_address", "phone", "all", "add_birthday", "show_birthday", "birthdays", "add_notes", "find_notes_by_tag", "find_contacts_by_tag", "edit_notes", "delete_notes", "hello", "exit", "close", "delete_contact"]
    ''' 
    available_commands = ["add", "remove_phone", "change_phone", "add_phone", "add_email", "add_address", "phone", "all", "add_birthday", "show_birthday", "birthdays", "when_birthdays", "add_notes", "find_notes_by_tag", "find_contacts_by_tag", "edit_notes", "delete_notes", "hello", "exit", "close", "delete_contact"]

    while True:
        user_input = input("Enter command: ").strip()
        command, args = parse_input(user_input)
        
        closest_command = intelligent_analysis(command, available_commands)
        if closest_command:
             if command != closest_command:
                print(f"Did you mean '{closest_command}'?")
            #continue
        
        if command == "add":
            try:
                input_str = ' '.join(args)
                name, phone, email, address = [part.strip() for part in input_str.split(";")]
                record = Record(name)
                record.add_phone(phone)
                record.add_email(email)
                record.add_address(address)
                book.add_record(record)
                print(f"Contact {name} added with phone {phone}, email {email}, and address {address}")
            except ValueError:
                print("Invalid command format. Use 'add [name]; [phone]; [email]; [address]'")

        elif command == "delete_contact":
            try:
                name = ' '.join(args).strip()
                book.remove_contact(name)  # This will invoke the remove_contact method correctly
            except ValueError:
                print("Invalid command format. Use 'delete_contact [name]'")
        
        elif command == "search":
            try:
                name = ' '.join(args).strip()
                found_contacts = book.findname(name)
                if found_contacts:
                    print("Found contacts:")
                    for contact in found_contacts:
                        print(contact)
                else:
                    print("No contacts found matching the search criteria.")
            except ValueError:
                print("Invalid command format. Use 'search [name]'")

        elif command == "remove_phone":
            try:
                input_str = ' '.join(args)
                name, phone = [part.strip() for part in input_str.split(";")]
                record = book.find(name)
                if record:
                    record.remove_phone(phone)
                    print(f"Phone number {phone} removed from contact {name}.")
                else:
                    print(f"Contact {name} not found.")
            except ValueError:
                print("Invalid command format. Use 'remove_phone [name]; [phone]'")

        elif command == "change_phone":
            try:
                input_str = ' '.join(args)
                name, old_phone, new_phone = [part.strip() for part in input_str.split(";")]
                record = book.find(name)
                if record:
                    record.edit_phone(old_phone, new_phone)
                    print(f"Phone number changed from {old_phone} to {new_phone} for contact {name}")
                else:
                    print(f"Contact {name} not found.")
            except ValueError:
                print("Invalid command format. Use 'change_phone [name]; [old_phone]; [new_phone]'")

        elif command == "add_phone":
            try:
                input_str = ' '.join(args)
                name, phone = [part.strip() for part in input_str.split(";")]
                record = book.find(name)
                if record:
                    record.add_phone(phone)
                    print(f"Phone number {phone} added to contact {name}.")
                else:
                    print(f"Contact {name} not found.")
            except ValueError:
                print("Invalid command format. Use 'add_phone [name]; [phone]'")

        elif command == "add_email":
            try:
                input_str = ' '.join(args)
                name, email = [part.strip() for part in input_str.split(";")]
                record = book.find(name)
                if record:
                    record.add_email(email)
                    print(f"Email {email} added to contact {name}.")
                else:
                    print(f"Contact {name} not found.")
            except ValueError:
                print("Invalid command format. Use 'add_email [name]; [email]'")

        elif command == "add_address":
            try:
                input_str = ' '.join(args)
                name, address = [part.strip() for part in input_str.split(";")]
                record = book.find(name)
                if record:
                    record.add_address(address)
                    print(f"Address {address} added to contact {name}.")
                else:
                    print(f"Contact {name} not found.")
            except ValueError:
                print("Invalid command format. Use 'add_address [name]; [address]'")

        elif command == "phone":
            try:
                name = ' '.join(args).strip()
                record = book.find(name)
                if record:
                    phone_info = '; '.join(str(p) for p in record.phones)
                    print(f"Phone numbers for {name}: {phone_info}")
                else:
                    print(f"Contact {name} not found.")
            except ValueError:
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
                input_str = ' '.join(args)
                name, birthday = [part.strip() for part in input_str.split(";")]
                record = book.find(name)
                if record:
                    record.add_birthday(birthday)
                    print(f"Birthday {birthday} added to contact {name}.")
                else:
                    print(f"Contact {name} not found.")
            except ValueError:
                print("Invalid command format. Use 'add_birthday [name]; [birthday]'")

        elif command == "show_birthday":
            try:
                name = ' '.join(args).strip()
                record = book.find(name)
                if record and record.birthday:
                    print(f"Birthday for {name}: {record.birthday}")
                elif record:
                    print(f"No birthday set for {name}")
                else:
                    print(f"Contact {name} not found.")
            except ValueError:
                print("Invalid command format. Use 'show_birthday [name]'")


        elif command == "birthdays":
            book.get_birthdays_per_week()
            
        elif command == "when_birthdays":
            book.when_birthdays()

        elif command == "delete_contact":
            try:
                name = ' '.join(args).strip()
                if name in book:
                    del book[name]
                    print(f"Contact {name} deleted successfully.")
                else:
                    print(f"Contact {name} not found.")
            except ValueError:
                print("Invalid command format. Use 'delete_contact [name]'")

        elif command == "add_notes":
            try:
                input_str = ' '.join(args)  # Combine all arguments into a single string
                name, rest = input_str.split(';', 1)  # Split into name and the rest at the first semicolon
                name = name.strip()
                note, *tags = [part.strip() for part in rest.split(";")]
                if name and note:
                    record = book.find(name)
                    if record:
                        tags = [tag.strip() for tag in tags] if tags else []
                        record.add_notes(note, tags)
                        print(f"Notes added for contact {name}")
                    else:
                        print(f"Contact {name} not found")
                else:
                    print("Missing required information for adding notes.")
            except ValueError:
                print("Invalid command format. Use 'add_notes [name]; [note]; [tag1; tag2; ...]'")

        elif command == "find_notes_by_tag": 
            try:
                tag = args[0]
                found_notes = book.find_notes_by_tag(tag)
                if found_notes:
                    print(f"Notes with tag '{tag}':")
                    for name, note in found_notes:
                        print(f"Contact: {name}, Note: {note}")
                else:
                    print(f"No notes found with tag '{tag}'")
            except IndexError:
                print("Invalid command format. Use 'find_notes_by_tag [tag]'")

        elif command == "find_contacts_by_tag":
            try:
                tag = args[0]
                found_contacts = book.find_contacts_by_tag(tag)
                if found_contacts:
                    print(f"Contacts with tag '{tag}':")
                    for contact in found_contacts:
                        print(contact)
                else:
                    print(f"No contacts found with tag '{tag}'")
            except IndexError:
                print("Invalid command format. Use 'find_contacts_by_tag [tag]'")

        elif command == "edit_notes":
            try:
                input_str = ' '.join(args)  # Combine all arguments back into a single string
                name, rest = input_str.split(';', 1)  # Split into name and the rest at the first semicolon
                name = name.strip()
                old_note, new_note, *tags = [part.strip() for part in rest.split(";")]
                if name and old_note and new_note:
                    record = book.find(name)
                    if record:
                        tags = [tag.strip() for tag in tags] if tags else []
                        record.edit_notes(old_note, new_note, tags)
                    else:
                        print(f"Contact {name} not found")
                else:
                    print("Missing required information for editing notes.")
            except ValueError:
                print("Invalid command format. Use 'edit_notes [name]; [old_note]; [new_note]; [tag1; tag2; ...]'")

        elif command == "delete_notes":
            try:
                input_str = ' '.join(args)  # Combine all arguments into a single string
                name, note = input_str.split(';', 1)  # Attempt to split input into name and note
                name = name.strip()
                note = note.strip()
                if name and note:
                    record = book.find(name)
                    if record:
                        record.delete_notes(note)
                        print(f"Note '{note}' deleted for contact {name}")
                    else:
                        print(f"Contact {name} not found")
                else:
                    print("Missing required information for deleting notes.")
            except ValueError:
                print("Invalid command format. Use 'delete_notes [name]; [note]'")

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


#to jest kod po dodaniu inteligentnego podpowiadania komend przez asystenta
#edycji i kasowaniu notatek
#poprawiony kod o podawanie komend przy użyciu ; aby można było imie i nazwisko podać etc.

# add Artur Laski; 0721199939 a@a.pl Katowice
# add Michal Misterkiewicz; 0999888777 michu@gmail.com Sosnowiec
# add Monika Misterkiewicz; 0505031265 m@m.pl Sosnowiec
# all
# search Mich
# search Misterk
# search Las
# remove ===> powinien podpowiedzieć komendę: Did you mean 'remove_phone'?
# remove_phone Michal 0999888777
# add_phone Michal 0777666555
# change_phone Michal 0777666555 0111222333
# add_email Michal m2@m.pl
# add_address Michal Krakow
# phone Michal Misterkiewicz
# add_birthday Michal Misterkiewicz 04.04.1983
# show_birthday Michal Misterkiewicz
# birthdays          ====>> if someone have a birthday in next week
# when_birthdays Michal Misterkiewicz
# delete_contact Michal Misterkiewicz
# add Michal Misterkiewicz 0999888777 michu@gmail.com Sosnowiec
# add_notes Michal Misterkiewicz; To jest pierwsza notatka od szwagra; family; c++; friend
# add_notes Monika Misterkiewicz; To jest testowa notatka rodzinna; family; wife
# find_notes_by_tag family
# find_contacts_by_tag wife
# edit_notes Monika Misterkiewicz; To jest testowa notatka rodzinna; To notes rodzinny; family; wife
# delete_notes Michał Misterkiewicz; To jest pierwsza notatka od szwagra
# hello
# close
# exit
