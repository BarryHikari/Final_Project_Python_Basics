# Final_Project_Python_Basics
Second group's final project

Key project objectives


This application is the result of a team project within the Master of Science in Computer Science program conducted by GoIT and Woolf University.The techniques used in the project include the basics of programming in Python.


Technical project description



The team's task was to develop a Personal Assistant with a command-line interface that has the following skills defined.


1. Save contacts with names, addresses, phone numbers, emails and birthdays in your contact book.
2. View a list of contacts whose birthdays are within a specified number of days from the current date.
3. When creating or editing an entry, checking the correctness of the entered phone number and e-mail address and informing the user in case of an incorrect entry.
4. Searching for contacts among the contacts in the book.
5. Editing and deleting entries from the contact book.
6. Saving notes with text information.
7. Search by notes, edit and delete notes.
8. Data storage: All data (contacts, notes) should be stored on your hard drive in your user folder.
9. The assistant should restart without any data loss.



Additional features

A "personal assistant" should additionally be able to:

1. Add "tags" to your notes and keywords describing the topic and subject matter of the note;
2. Search and sort notes by keywords (tags);
3. The bot should analyze the entered text, try to guess what the user wants from it and propose the closest command to execute.

For users

Dear user, we are glad that you have chosen our Personal Assistant. The interface is implemented in the form of a command line and relies on text messages and commands that you can enter from the keyboard. The program handles incorrect input correctly without closing, so don't worry if you enter something incorrectly. To start using the application, type the command in the console. Here is the list of supported commands.

Supported Commands

- `add [name] [phone] [email] [address]`: Add a new contact with specified details.
- `search [name]`: Search for contacts by name.
- `remove_phone [name] [phone]`: Remove a phone number from a contact.
- `change_phone [name] [old phone] [new phone]`: Change a contact's phone number.
- `add_phone [name] [phone]`: Add a phone number to a contact.
- `add_email [name] [email]`: Add an email address to a contact.
- `add_address [name] [address]`: Add a physical address to a contact.
- `phone [name]`: Display phone numbers for a contact.
- `all`: Display all contacts in the address book.
- `add_birthday [name] [birth date]`: Add a birthday to a contact.
- `show_birthday [name]`: Show the birthday for a contact.
- `birthdays`: Display upcoming birthdays in the next week.
- `when_birthdays`: Show how many days until each contact's birthday.
- `delete_contact [name]`: Delete a contact.
- `add_notes [name] [note], [tag1, tag2, ...]`: Add notes with tags to a contact.
- `delete_notes [name] [note], [tag1, tag2, ...]`: Delete a notes.
- `find_notes_by_tag [tag]`: Find notes associated with a specific tag.
- `find_contacts_by_tag [tag]`: Find contacts associated with a specific tag.
- `hello`: Display a greeting message.
- `close` or `exit`: Save the address book to a file and exit the program.


To use the address book assistant, simply run the `main()` function. Follow the prompts to perform various operations on your contacts.

Thank you and we hope you enjoy using our application!