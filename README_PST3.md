# FIT1056-PSTs-37403834

## PST3 – Object-Oriented Music School Management System (MSMS)

This project upgrades the Music School Management System (MSMS) developed in PST2.

In PST2, the program was improved by adding JSON storage so that student, teacher, and attendance information could be saved and loaded again after the program was closed. The program also included features such as student and teacher registration, enrolment, searching, updating and removing records, student check-in, and student card generation.

However, most of the PST2 program was still procedural. Most of the functionality was written as functions that worked with dictionaries and lists.

PST3 changes the structure of the program by using Object-Oriented Programming (OOP). Students, teachers, and courses are now represented by classes and objects. The main system logic is controlled by the ScheduleManager class, while main.py is mainly responsible for displaying the menu, asking the user for input, and calling the correct manager methods.

PST3 also introduces courses, lesson schedules, daily lesson rosters, and the ability to switch students between courses.

The useful features previously developed in PST1 and PST2 were also kept where suitable and changed to work with the new PST3 structure.


## Features

The current PST3 system supports the following functionality:

- Register a new student and automatically assign them a unique student ID.
- Register a new teacher and automatically assign them a unique teacher ID.
- Enrol an existing student into an existing course.
- Prevent a student from being enrolled in the same course more than once.
- Search for students by name.
- Search for teachers by name or speciality.
- Perform case-insensitive and partial-text searches.
- Display all registered students and their enrolled course IDs.
- Display all teachers and their specialities.
- Update existing student information.
- Update existing teacher information.
- Remove students from the system.
- Remove teachers from the system.
- Remove deleted students from course enrolment lists.
- Check a student into a course.
- Automatically record the date and time of a student check-in.
- Print a student ID card to a text file.
- View the daily lesson roster for a selected day.
- Display the course name, instrument, start time, and room for lessons.
- Switch a student from one course to another.
- Save student, teacher, course, lesson, and attendance information to JSON.
- Load previously saved information when the program starts.
- Save changes after operations that change the system data.
- Handle invalid student and course IDs.
- Handle non-numeric IDs without crashing the program.
- Reject blank required input where validation is included.
- Provide a menu-driven command-line interface that continues running until the user chooses to quit.


## Project Structure

The PST3 program uses the following main files and folders:

app/
- user.py
- student.py
- teacher.py
- schedule.py

data/
- msms.json

main.py

README.md


## Project Components

The PST3 implementation is divided into four main parts.


### Fragment 3.1 – Model Layer

Fragment 3.1 introduces the main classes used to represent the information in the Music School Management System.

Instead of using only dictionaries to represent students and teachers, the program now creates objects.


### app/user.py

This file contains the User class.

The User class is the base class used for students and teachers.

It stores the information that both students and teachers have in common:

- User ID
- Name

StudentUser and TeacherUser can inherit this information from User instead of repeating the same code.


### app/student.py

This file contains the StudentUser class.

StudentUser inherits from the User class.

The student receives the ID and name attributes from User.

Each student also has an enrolled_course_ids list.

This list stores the IDs of the courses that the student is currently enrolled in.


### app/teacher.py

This file contains the TeacherUser class and the Course class.

TeacherUser also inherits from User.

A teacher stores:

- ID
- Name
- Speciality

The Course class represents a course offered by the music school.

Each course stores:

- Course ID
- Course name
- Instrument
- Teacher ID
- Enrolled student IDs
- Lessons

The enrolled_student_ids list stores the IDs of students who are enrolled in the course.

The lessons list stores lesson information such as:

- Lesson ID
- Day
- Start time
- Room


### Fragment 3.2 – ScheduleManager and Data Persistence

Fragment 3.2 introduces the ScheduleManager class inside schedule.py.

ScheduleManager is the main controller of the application.

It stores and manages:

- Students
- Teachers
- Courses
- Attendance information

It also contains the main system functionality such as registration, enrolment, searching, updating, removing records, course switching, check-in, and saving/loading data.


### Loading Data

When ScheduleManager is created, it loads data from:

data/msms.json

The JSON file contains normal dictionaries and lists.

The program converts the saved dictionaries into the correct Python objects.

Student dictionaries are converted into StudentUser objects.

Teacher dictionaries are converted into TeacherUser objects.

Course dictionaries are converted into Course objects.

After a student object is created, the saved enrolled course IDs are restored.

After a course object is created, the enrolled student IDs and lessons are also restored.

Attendance information is also loaded from the JSON file.


### Saving Data

While the program is running, students, teachers, and courses are stored as objects.

JSON cannot directly save these custom Python objects.

Before saving, the program converts the object information back into dictionaries.

The following information is saved:

- Students
- Teachers
- Courses
- Attendance

The information is written to data/msms.json.

This means that changes remain available after the program is closed and started again.


### Fragment 3.3 – Student Check-In

Fragment 3.3 adds the student course check-in functionality.

Two helper methods are used:

- find_student_by_id()
- find_course_by_id()

find_student_by_id() searches through the students and returns the student with the matching ID.

find_course_by_id() searches through the courses and returns the course with the matching ID.

If no matching student or course is found, the method returns None.


### check_in()

The check_in() method:

1. Finds the student using their ID.
2. Finds the course using its ID.
3. Checks that both the student and course exist.
4. Rejects the check-in if one of the IDs is invalid.
5. Creates the current date and time.
6. Creates an attendance record.
7. Adds the record to the attendance list.
8. Saves the updated data.

Each attendance record stores:

- Student ID
- Course ID
- Timestamp

This allows attendance information to remain saved after the program is restarted.


### Fragment 3.4 – Main Application and View Layer

Fragment 3.4 introduces the new main.py file.

main.py is responsible for interacting with the user.

It:

- Displays the menu.
- Asks the user for input.
- Accepts IDs and other required information.
- Displays results and error messages.
- Calls methods from ScheduleManager.

The program creates one ScheduleManager object when main() starts.

The same manager is then used while the menu continues running.

The main.py file does not directly load or save the JSON data. The main data handling is performed by ScheduleManager.


## New PST3 Scheduling Features

PST3 adds new scheduling functionality to the MSMS.


### Daily Lesson Roster

The daily lesson roster allows the user to enter a day such as Monday.

The program checks the lessons stored inside each course and finds the lessons that match the selected day.

The roster displays:

- Course name
- Instrument
- Start time
- Room

The day comparison is case-insensitive.


### Switching Student Courses

The course switching feature allows a student to move from one course to another.

The program:

1. Finds the student.
2. Finds the original course.
3. Finds the new course.
4. Checks that all IDs are valid.
5. Checks that the student is enrolled in the original course.
6. Removes the original course ID from the student.
7. Removes the student ID from the original course.
8. Adds the new course ID to the student.
9. Adds the student ID to the new course.
10. Saves the changes.

This makes sure that the student information and course information remain consistent.


## PST2 Features Kept in PST3

Useful functionality from PST1 and PST2 was kept and changed to work with the PST3 Object-Oriented structure.


### Student Registration

The system allows a new student to be registered using their name.

The program:

- Removes unnecessary spaces around the input.
- Checks that the name is not blank.
- Creates a new unique student ID.
- Creates a StudentUser object.
- Adds the student to the student list.
- Saves the updated data.
- Displays the student's new ID.


### Teacher Registration

The system allows a new teacher to be registered using:

- Name
- Speciality

The program checks that both values are provided.

A unique teacher ID is created and a TeacherUser object is added to the system.


### Course Enrolment

Students are now enrolled using course IDs instead of only using instrument names.

The program checks:

- That the student exists.
- That the course exists.
- That the student is not already enrolled in that course.

When enrolment succeeds:

- The course ID is added to the student's enrolled course list.
- The student ID is added to the course's enrolled student list.
- The updated data is saved.


### Searching

Students can be searched by name.

Teachers can be searched by name or speciality.

The searches are:

- Case-insensitive.
- Able to match part of a name or speciality.

An empty search term is rejected.


### Updating Records

The system allows student names to be updated.

Teacher names and specialities can also be updated.

When updating a teacher, a field can be left blank to keep the current value.


### Removing Records

Students and teachers can be removed using their IDs.

When a student is removed, their ID is also removed from course enrolment lists.

This prevents courses from continuing to store the ID of a student who no longer exists.


### Student Cards

The system can create a student ID card as a text file.

The student card contains:

- Student ID
- Student name
- Course names

The program uses the student's course IDs to find the names of the courses before creating the card.


## How to Run the Program

### Requirements

- Python 3
- A terminal or command-line environment


### Running the Program

1. Open a terminal.

2. Navigate to the msms-project folder.

For example:

cd "FIT1056-PSTs-37403834/Main Project/msms-project"

3. Run:

python main.py

4. The Music School Management System PST3 menu will appear.

The menu contains the following options:

1. View Daily Lesson Roster
2. Switch Student Course
3. Register New Student
4. Register New Teacher
5. Enrol Student in Course
6. Search Student or Teacher
7. List All Students
8. List All Teachers
9. Update Student
10. Update Teacher
11. Remove Student
12. Remove Teacher
13. Check-in Student
14. Print Student Card
q. Quit

5. Enter the number of the option you want to use.

6. Follow the instructions displayed by the program.

7. Enter q to exit the program.


### Important Note

The program expects the JSON data file to be located at:

data/msms.json

The terminal should therefore be inside the msms-project folder before running main.py.

If main.py is started from another folder, the program may not find the JSON data file.


## Testing the Program

The program was manually tested using the command-line menu.

The following manual test sequence was used to verify the main functionality:

1. Run main.py and confirm that the PST3 menu appears.

2. Display all students and confirm that the student information from msms.json loads correctly.

3. Display all teachers and confirm that the teacher information loads correctly.

4. View the daily roster for Monday and confirm that the correct lesson information is displayed.

5. Enter a day without lessons and confirm that the program displays an appropriate message.

6. Register a new student with a valid name and confirm that a unique student ID is assigned.

7. Attempt to register a student using blank input and confirm that the registration is rejected.

8. Register a new teacher with a valid name and speciality and confirm that a unique teacher ID is assigned.

9. Attempt to register a teacher with a blank name or speciality and confirm that the registration is rejected.

10. Enrol an existing student into an existing course.

11. Confirm that the course ID is added to the student's enrolment list.

12. Confirm that the student ID is added to the course's enrolment list.

13. Attempt to enrol the same student into the same course again and confirm that the duplicate enrolment is rejected.

14. Attempt enrolment using a student ID that does not exist and confirm that an error is displayed.

15. Attempt enrolment using a course ID that does not exist and confirm that an error is displayed.

16. Search for a student using their full name.

17. Search for a student using part of their name.

18. Search for a student using different capitalisation and confirm that the search is case-insensitive.

19. Search for a teacher using their name.

20. Search for a teacher using their speciality.

21. Attempt an empty search and confirm that it is rejected.

22. Switch a student from one existing course to another.

23. Confirm that the old course is removed from the student's enrolled course list.

24. Confirm that the new course is added to the student's enrolled course list.

25. Confirm that the student ID is removed from the old course.

26. Confirm that the student ID is added to the new course.

27. Attempt a course switch using an invalid student ID and confirm that it is rejected.

28. Attempt a course switch using an invalid course ID and confirm that it is rejected.

29. Check a valid student into a valid course.

30. Confirm that an attendance record is created.

31. Confirm that the current date and time is automatically stored in the attendance record.

32. Attempt check-in using an invalid student ID and confirm that it is rejected.

33. Attempt check-in using an invalid course ID and confirm that it is rejected.

34. Print a student card and confirm that a text file is created.

35. Open the student card and confirm that the student ID, name, and course names are displayed.

36. Update a student's name and confirm that the new information is displayed.

37. Update a teacher's name or speciality and confirm that the information changes correctly.

38. Leave one teacher update field blank and confirm that the existing value is kept.

39. Remove a test student and confirm that the student is no longer displayed.

40. Confirm that the removed student's ID is also removed from course enrolment lists.

41. Remove a test teacher and confirm that the teacher is no longer displayed.

42. Enter non-numeric text where a numeric ID is expected and confirm that an error message is displayed instead of the program crashing.

43. Enter an invalid menu option and confirm that the program displays an appropriate message and continues running.

44. Exit the program using q.

45. Run main.py again.

46. Confirm that previously saved student, teacher, course, enrolment, and attendance information is loaded from data/msms.json.


### Note

Unlike the original PST1 prototype, the application data is not lost when the program stops.

PST3 continues to use JSON persistence from PST2, but the JSON information is now converted into StudentUser, TeacherUser, and Course objects while the application is running.


## Design Choices and Assumptions

- The program uses Object-Oriented Programming to organise students, teachers, courses, and the main system logic.

- User is used as a base class because students and teachers both have an ID and name.

- StudentUser and TeacherUser inherit the shared information from User.

- ScheduleManager is used as the main controller of the application.

- One ScheduleManager object is created when the program starts and is used for the entire menu session.

- main.py is mainly responsible for user interaction and calls ScheduleManager methods to perform system operations.

- JSON is used for persistent storage because it can store the lists and dictionaries needed by the system in a readable format.

- The JSON data file is stored inside the data folder to separate saved data from the application code.

- Student, teacher, and course dictionaries loaded from JSON are converted into objects when the program starts.

- Objects are converted back into dictionaries before the information is saved to JSON.

- Students store enrolled course IDs instead of the free-text instrument enrolment structure used in PST2.

- Courses store enrolled student IDs so that the student and course enrolment information can be kept consistent.

- Searches remain case-insensitive so that differences in capitalisation do not prevent matching records from being found.

- Partial-text searching is kept from PST2 to make student and teacher lookup easier.

- Duplicate course enrolments are prevented.

- Changes to important application data are saved after successful operations.

- Student check-in records contain the student ID, course ID, and timestamp.

- Student cards are created as text files containing the student's ID, name, and course names.

- The application continues to use a command-line interface.


### Assumptions

- Student IDs are numeric.

- Teacher IDs are numeric.

- Course IDs are numeric.

- Each student has one unique student ID.

- Each teacher has one unique teacher ID.

- Each course has one unique course ID.

- Each teacher has one speciality.

- A student may be enrolled in multiple courses.

- A course may contain multiple students.

- Each course is linked to one teacher ID.

- Lesson information is stored inside the lessons list for each course.

- Required names and specialities are assumed to contain sensible values after the basic validation checks.

- Blank required values are rejected where validation is provided.

- The program is intended to be operated through the provided menu.

- data/msms.json is used to maintain the application data between sessions.

- main.py is expected to be run while the terminal is inside the msms-project directory.


## Limitations

- Input validation remains basic and does not validate every possible real-world name, speciality, or value.

- Each teacher currently stores one speciality.

- Student cards are generated as text files rather than graphical cards.

- The application continues to use a command-line interface and does not include a graphical user interface.

- JSON is used for persistence rather than a database.

- Lesson information is based on the lessons already stored inside the course data.

- The program does not currently provide a complete menu for creating new courses or lesson schedules.

- The program expects the correct working directory so that data/msms.json can be found.


## Additional Improvements

The improvements previously added in PST1 and PST2 were kept where they were still suitable and were changed to work with the PST3 Object-Oriented structure.

These include:

- Basic validation to prevent blank student names.

- Basic validation to prevent blank teacher names and specialities.

- Validation of empty search terms.

- Handling of non-numeric IDs through error messages instead of allowing the program to crash.

- Handling of student and course IDs that do not exist.

- Case-insensitive student searches.

- Case-insensitive teacher searches.

- Partial-text searching for student and teacher records.

- Searching teachers by both name and speciality.

- Duplicate enrolment protection.

- Clear messages when no matching student or teacher is found.

- Registration confirmation messages that display the assigned student or teacher ID.

- Student update functionality.

- Teacher update functionality.

- Student removal functionality.

- Teacher removal functionality.

- Removing deleted students from course enrolment lists.

- Validation before recording a student check-in.

- Automatic date and time recording for attendance.

- Student ID card generation.

- Persistent JSON storage.

- Saving after operations that change application data.

- Integration of the existing PST1 and PST2 front-desk features with the new PST3 Object-Oriented structure.


## Summary

PST3 continues the same Music School Management System developed in PST1 and PST2.

PST2 mainly solved the problem of data being lost after the program closed by introducing JSON persistence.

PST3 improves the internal structure of the program by introducing Object-Oriented Programming.

The system now uses:

- User
- StudentUser
- TeacherUser
- Course
- ScheduleManager

The program is separated into model files, the ScheduleManager controller, the main.py user interface, and the JSON data file.

PST3 also introduces courses, lessons, daily rosters, and course switching while keeping the useful student and teacher functionality developed in earlier stages.

This makes the application more organised and easier to continue improving in the later PST stages.