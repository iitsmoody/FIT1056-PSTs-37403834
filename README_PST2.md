# FIT1056-PSTs-37403834

## PST2 – Persistent Music School Management System (MSMS)

This project upgrades the Music School Management System (MSMS) developed in PST1. The program provides a command-line interface that allows users to register students and teachers, enrol existing students in instruments, search for students and teachers, display records, update and remove records, check students into courses, and print student ID cards. 

Unlike PST1, where student and teacher information was only stored in memory while the program was running, PST2 uses a JSON file to provide persistent storage. This means that student, teacher, and attendance data can be saved and loaded again when the program is restarted.

The system now stores its main data inside the global `app_data` dictionary. Student and teacher records are represented as dictionaries and stored in lists inside `app_data`.The system stores student and teacher information in memory while the program is running. The data is represented using Student and Teacher objects and is stored in lists.



## Features

The current PST2 system supports the following functionality:

- Register a new student and automatically assign them a unique student ID.
- Enrol a newly registered student in an instrument.
- Enrol an existing student in additional instruments using their student ID.
- Prevent duplicate instrument enrolments for the same student using case-insensitive comparison.
- Register new teachers and automatically assign them a unique teacher ID.
- Search for students by name.
- Search for teachers by name or speciality.
- Perform case-insensitive and partial-text searches.
- Display all registered students and their instrument enrolments.
- Display all teachers and their specialities.
- Update existing student information.
- Update existing teacher information.
- Remove students from the system.
- Remove teachers from the system.
- Check a student into a course and record the check-in in the attendance data.
- Automatically record the date and time of a student check-in.
- Print a student ID card to a text file.
- Save student, teacher, attendance, and ID data to `msms.json`.
- Load previously saved data when the program starts.
- Save changes after operations that modify the system data.
- Validate required inputs such as student names, teacher names, instruments, specialities, course IDs, and search terms.
- Handle non-numeric and non-existent IDs where required.
- Provide a menu-driven command-line interface that continues running until the user chooses to quit.


## Project Components

The PST2 implementation is divided into four main parts:

### Fragment 2.1 – Core Persistence Engine
Introduces persistent storage using the `app_data` dictionary and the `msms.json` file. The `load_data()` function loads previously saved application data when the program starts. If the file does not exist, the program creates the default data structure. The `save_data()` function writes the current application data to the JSON file.

### Fragment 2.2 – Refactoring and Expanding CRUD Operations
Refactors the data-management functions so that they work with dictionaries stored inside `app_data` instead of the in-memory objects used in PST1. It includes teacher creation and adds operations for updating and removing students and teachers.

### Fragment 2.3 – Receptionist Features
Adds two new receptionist features. The `check_in()` function records a student's course check-in and timestamp in the attendance list. The `print_student_card()` function creates a text file containing the student's ID, name, and instrument enrolments.

### Fragment 2.4 – Main Application
Integrates the PST1 functionality and the new PST2 functionality into the final command-line menu. The application loads saved data when it starts, allows the user to perform the available operations, saves data after changes, and performs a final save when the user quits.



## How to Run the Program

### Requirements
- Python 3
- A terminal or command-line environment

### Running the Program
1. Open a terminal in the project directory.
2. Ensure the terminal is located inside the `msms-project` folder.
3. Run the following command:

```bash
python pst2_main.py
```

4. The Music School Management System PST2 menu will appear in the terminal.
5. Enter one of the displayed menu options and press Enter to perform the corresponding operation.
6. Enter `q` to save the current data and exit the program.



## Testing the Program

The program can be tested manually through the command-line menu.

The following manual test sequence was used to verify the main functionality:

1. Register a new student with a valid name and instrument and confirm that a unique student ID is assigned.
2. Register a new teacher and confirm that a unique teacher ID is assigned.
3. Display all students and confirm that the new student appears with the correct ID and instrument.
4. Display all teachers and confirm that the new teacher appears with the correct ID and speciality.
5. Enrol an existing student in an additional instrument using their student ID.
6. Attempt to enrol the same student in the same instrument using different capitalisation and confirm that the duplicate enrolment is rejected.
7. Search for students and teachers using full or partial search terms and confirm that the searches are case-insensitive.
8. Attempt an empty search and confirm that it is rejected.
9. Check a valid student into a course and confirm that an attendance record is created.
10. Print a student card and confirm that a text file containing the student's details is created.
11. Update a teacher's information and confirm that the updated information is displayed.
12. Update a student's information and confirm that the updated information is displayed.
13. Attempt to use a non-numeric student or teacher ID where a numeric ID is required and confirm that an appropriate error message is displayed.
14. Attempt to use a student ID that does not exist and confirm that an appropriate error message is displayed.
15. Remove a student and confirm that the student is no longer displayed.
16. Remove a teacher and confirm that the teacher is no longer displayed.
17. Enter an invalid menu option and confirm that the program displays an appropriate message and continues running.
18. Select `q` and confirm that the application saves the data and exits correctly.
19. Run `pst2_main.py` again and confirm that previously saved student, teacher, enrolment, and attendance data is loaded from `msms.json`.

### Note:
Unlike PST1, the data is not reset when the program is restarted. The application saves its data to `msms.json` and loads it again the next time the program is run.



## Design Choices and Assumptions

- A global `app_data` dictionary is used as the main data store for the application.
- Student and teacher records are represented as dictionaries and stored in lists inside `app_data`.
- Attendance records are stored in the `attendance` list inside `app_data`.
- The `next_student_id` and `next_teacher_id` values are stored in `app_data` so that unique IDs can continue correctly after the program is restarted.
- JSON is used to save the application data because it allows the program's dictionary and list data to be stored in a readable file.
- A student's `enrolled_in` value is stored as a list so that a student can be enrolled in more than one instrument.
- Searches are case-insensitive so that differences in capitalisation do not prevent a matching record from being found.
- Student lookup searches by name, while teacher lookup searches by both name and speciality.
- Duplicate instrument enrolments are checked using a case-insensitive comparison.
- Student check-ins contain the student ID, course ID, and timestamp.
- Student cards are created as text files containing the student's ID, name, and current instrument enrolments.
- The system continues to use a command-line menu so that the PST1 functionality and new PST2 functionality can be accessed from one application.

### Assumptions

- User-entered names, instruments, specialities, and course IDs are assumed to contain sensible values after basic validation.
- Blank or whitespace-only required values are rejected where validation is provided.
- Each teacher is assumed to have one speciality.
- A student may be enrolled in multiple instruments.
- The program is intended to be operated through the provided menu.
- The `msms.json` file is used by the program to maintain data between sessions.



## Limitations

- Input validation remains limited to basic checks. The program does not perform advanced validation of names, instruments, specialities, or course IDs.
- Each teacher currently stores only one speciality.
- Student cards are generated as text files rather than formatted graphical cards.
- The system provides a command-line interface only and does not include a graphical user interface (GUI).
- The application uses a JSON file for persistence rather than a database.


## Additional Improvements

The improvements previously added in PST1 were kept where they were still suitable and were adjusted to work with the new PST2 data structure.

These include:

- Basic validation to prevent blank or whitespace-only student names, teacher names, instruments, specialities, course IDs, and search terms where required.
- Protection against duplicate instrument enrolments using case-insensitive comparison.
- Case-insensitive and partial-text searching for student and teacher records.
- Clear lookup output when no matching student or teacher is found.
- Registration confirmation messages that display the assigned student or teacher ID.
- Teacher registration through the main menu.
- Handling of non-numeric IDs through error messages instead of allowing the program to crash.
- Validation of student IDs before recording a student check-in.
- Whitespace handling using `strip()` so accidental spaces around user input do not affect normal operation.
- Integration of the existing PST1 student registration, enrolment, lookup, listing, and teacher registration functionality with the new persistent PST2 data model.