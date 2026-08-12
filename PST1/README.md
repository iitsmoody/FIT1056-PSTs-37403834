# FIT1056-PSTs-37403834

## PST1 – Music School Management System (MSMS)

This project implements an in-memory prototype of a Music School Management System (MSMS). The program provides a command-line front desk interface that allows users to register students and teachers, enrol existing students in instruments, search for students and teachers, and display student and teacher records.

The system stores student and teacher information in memory while the program is running. The data is represented using Student and Teacher objects and is stored in lists.



## Features

The current PST1 prototype supports the following functionality:

- Register a new student and automatically assign them a unique student ID.
- Enrol a newly registered student in an instrument.
- Enrol an existing student in additional instruments using their student ID.
- Prevent duplicate instrument enrolments for the same student using case-insensitive comparison.
- Register new teachers through the admin menu and automatically assign them a unique teacher ID.
- Search for students by name.
- Search for teachers by name or speciality.
- Perform case-insensitive and partial-text searches.
- Display all registered students and their instrument enrolments.
- Display all teachers and their specialities.
- Validate required inputs such as student names, teacher names, instruments, specialities, and search terms so that blank values are not accepted.
- Handle non-numeric and non-existent student IDs when enrolling existing students.
- Provide clear student and teacher lookup results when no matching record is found.
- Provide a menu-driven command-line interface that continues running until the user chooses to quit.



## Project Components

The PST1 implementation is divided into four main parts:

### Fragment 1.1 – Data Models and In-Memory Storage
Defines the `Student` and `Teacher` classes used to represent the main entities in the system. It also creates the in-memory student and teacher data stores and maintains counters for assigning unique IDs.

### Fragment 1.2 – Core Helper Functions
Implements the core operations used to manage and search the system's data, including adding teachers, listing students and teachers, and searching for records.

### Fragment 1.3 – Front Desk Functions
Implements higher-level front desk operations for registering students, enrolling existing students in instruments, and performing lookups for students or teachers. The integrated prototype also extends these operations with teacher registration.

### Fragment 1.4 – Main Menu
Provides the command-line menu used to interact with the complete system. It connects the previous components and repeatedly accepts user choices until the user chooses to quit.



## How to Run the Program

### Requirements
- Python 3
- A terminal or command-line environment

### Running the Program
1. Open a terminal in the project directory.
2. Ensure the terminal is located inside the `msms-project` folder.
3. Run the following command:

```bash
python MSMS.py
```

4. The Music School Front Desk menu will appear in the terminal.
5. Enter one of the displayed menu options and press Enter to perform the corresponding operation.



## Testing the Program

The program can be tested manually through the command-line menu.

The following manual test sequence was used to verify the main functionality:

1. Register a new student with a valid name and instrument and confirm that a unique student ID is assigned.
2. Register multiple students, including students with the same name, and confirm that they receive different IDs.
3. Enrol an existing student in an additional instrument using their student ID.
4. Attempt to enrol the same student in the same instrument using different capitalisation and confirm that the duplicate enrolment is rejected.
5. Display all students and confirm that their names, IDs, and instrument enrolments are shown correctly.
6. Search for students using full and partial names and confirm that searches are case-insensitive.
7. Search for teachers using names and specialities and confirm that searches are case-insensitive.
8. Perform a search that matches only a student or only a teacher and confirm that the output clearly identifies which type of record has no matches.
9. Attempt an empty search and confirm that it is rejected.
10. Register a new teacher and confirm that a unique teacher ID is assigned.
11. Display all teachers and confirm that newly registered teachers appear in the teacher list.
12. Attempt registration with blank student names, teacher names, instruments, and teacher specialities and confirm that the invalid input is rejected.
13. Attempt to enrol a student using a non-numeric ID and confirm that an appropriate error message is displayed.
14. Attempt to enrol a student using a numeric ID that does not exist and confirm that the program rejects the ID before requesting an instrument.
15. Enter an invalid menu option and confirm that the program displays an appropriate message and continues running.
16. Select `q` to confirm that the program exits correctly.

### Note:
Because this version uses in-memory storage, test data is reset each time the program is restarted.



## Design Choices and Assumptions

- `Student` and `Teacher` classes are used to represent the two main types of records managed by the system.
- Student and teacher records are stored in Python lists (`student_db` and `teacher_db`) to provide simple in-memory storage for the PST1 prototype.
- Numeric ID counters are used to assign a unique ID to each new student and teacher during a program session.
- A student's `enrolled_in` attribute is stored as a list so that a student can be enrolled in more than one instrument.
- Searches are case-insensitive so that differences in capitalisation do not prevent a matching record from being found.
- Student lookup searches by name, while teacher lookup searches by both name and speciality.
- The system uses a command-line menu because PST1 focuses on implementing and demonstrating the core program logic.

### Assumptions

- User-entered names, instruments, and teacher specialities are assumed to contain sensible values after basic validation. Blank or whitespace-only values are rejected, but the prototype does not perform advanced validation such as checking whether names contain numbers or special characters.
- Each teacher is assumed to have one speciality in the current PST1 prototype.
- The system assumes that records only need to exist for the duration of the current program session because PST1 uses in-memory storage.
- The system is intended to be operated through the provided menu, with users selecting one of the available menu options.



## Limitations

- The system uses in-memory storage, so student and teacher data created during a session is lost when the program terminates.
- The prototype does not use a file or database for persistent storage.
- Input validation remains limited to basic checks. Blank or whitespace-only required values are rejected, but advanced validation of names, instruments, and specialities is not implemented.
- Each teacher currently stores only one speciality.
- The system provides a command-line interface only and does not include a graphical user interface (GUI).


## Additional Improvements

After completing the initial PST1 functionality, several additional improvements were implemented and tested to improve usability and robustness:

- Added basic validation to prevent blank or whitespace-only student names, teacher names, instruments, specialities, and search terms.
- Added early validation in the menu so invalid information is rejected before unnecessary follow-up information is requested.
- Added protection against duplicate instrument enrolments using case-insensitive comparison.
- Improved lookup output so student and teacher search results clearly indicate which type of record has or has not been matched.
- Improved registration confirmation messages to display useful information such as the newly assigned student or teacher ID.
- Added teacher registration through the admin menu using the existing teacher data model and ID system.
- Improved student ID handling so non-numeric and non-existent IDs are rejected before requesting an instrument.
- Added whitespace handling using `strip()` so accidental spaces around user input do not affect normal operation.