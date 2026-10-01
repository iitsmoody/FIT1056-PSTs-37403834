# FIT1056-PSTs-37403834

## PST4 - Streamlit GUI Music School Management System (MSMS)

This project is the fourth stage of the Music School Management System (MSMS) developed throughout the FIT1056 PSTs.

In PST3, the main functionality of the system was handled through the ScheduleManager and the program was operated through a command-line interface. In PST4, I added a Streamlit graphical user interface on top of the existing backend.

The main goal of my PST4 implementation was to improve the user experience without rewriting the business logic that was already working in PST3. The Streamlit pages call methods from ScheduleManager, while ScheduleManager continues to handle students, teachers, courses, attendance and JSON persistence.

I also wanted the move from the command-line interface to the GUI to not remove functionality that I had already implemented in previous PSTs. Because of this, in addition to completing the required PST4 GUI functionality, I added GUI access to the student and teacher management features that were available in PST3.

The system now provides GUI pages for:

- Student management
- Teacher management
- Daily lesson roster
- Student check-in
- A Payments placeholder for PST5


## Project Structure

The main files used in PST4 are:

- main.py - launches the Streamlit application.
- PST3_main.py - keeps the previous PST3 command-line interface for reference.
- gui/main_dashboard.py - controls the main Streamlit layout and page navigation.
- gui/student_pages.py - contains the student management interface.
- gui/teacher_pages.py - contains the teacher management interface.
- gui/roster_pages.py - contains the daily roster and student check-in interface.
- app/schedule.py - contains ScheduleManager and the main business logic.
- app/student.py - contains the StudentUser class.
- app/teacher.py - contains TeacherUser and Course.
- app/user.py - contains the base User class.
- data/msms.json - stores the persistent MSMS data.


## Main Dashboard

The main dashboard is implemented in gui/main_dashboard.py.

It creates the Streamlit application and provides sidebar navigation between the different sections of the system.

The available pages are:

- Student Management
- Teacher Management
- Daily Roster
- Payments (stub)

The dashboard creates a ScheduleManager when the application first starts and stores it inside Streamlit session state.

This means the same manager object can continue to be used while the user moves between the different pages instead of creating a new ScheduleManager every time Streamlit reruns the application.

The Payments page is intentionally a placeholder because payment functionality is planned for PST5.


## Student Management

The Student Management page is implemented in gui/student_pages.py.

It contains the student-related functionality of the system.


### Find a Student

The user can search for a student by entering part or all of their name.

The search uses:

manager.find_students(term)

The search is case-insensitive.

For each matching student, the GUI displays:

- Student ID
- Student name
- Enrolled course or courses
- Instrument for each enrolled course

If the student has no current enrolments, the GUI displays this instead of failing.

If there are no matches, the user receives a "No students found" message.


### Register New Student

A new student can be registered from the GUI.

The user selects:

- The student's first instrument
- The exact course for that instrument
- The student's name

The instrument choices are created dynamically from the courses currently stored in ScheduleManager.

After an instrument is selected, the course list only shows courses matching that instrument.

For example, selecting Piano can show:

- Beginner Piano
- Intermediate Piano

The GUI then passes the selected course ID to:

manager.register_new_student(name, instrument, course_id)

If registration succeeds, the student is created, enrolled into the selected course and the changes are saved to the JSON file.


### List All Students

The Student Management page also displays all currently registered students.

For each student it shows:

- Student ID
- Student name
- Current course enrolments

The course names are found from the student's enrolled course IDs using ScheduleManager.


### Enrol Student in Course

An existing student can be enrolled into an additional course.

The GUI first allows the user to select a student.

It then filters the available courses so that courses the student is already enrolled in are not shown again.

The enrolment is completed using:

manager.enrol_student(student_id, course_id)

The backend also performs its own validation before saving the enrolment.


### Switch Student Course

A student can switch from one course to another through the GUI.

The user selects:

- A student
- One of the student's current courses
- A new course

The current course dropdown only contains courses the student is actually enrolled in.

The new course dropdown only contains courses the student is not already enrolled in.

The switch is completed using:

manager.switch_student_course(student_id, from_course_id, to_course_id)

The backend removes the student from the original course and adds them to the new course before saving the changes.


### Update Student

The GUI allows the name of an existing student to be changed.

The user selects the student and enters the updated name.

The change is completed using:

manager.update_student(student_id, new_name)

The ScheduleManager validates the new name and saves the updated information.


### Remove Student

An existing student can be removed from the system.

The GUI displays a warning before the removal.

The removal uses:

manager.remove_student(student_id)

The backend removes the student from the student list and also removes their ID from courses they were enrolled in.

The updated data is then saved.


### Print Student Card

The user can select a student and generate their student card.

This uses:

manager.print_student_card(student_id)

The card is created as a text file using the student's ID as the filename.

For example:

1_card.txt

The generated card contains:

- Student ID
- Student name
- Current courses

The generated card files are output files and are not required to remain permanently in the repository.


## Teacher Management

I added gui/teacher_pages.py so that the teacher management functionality already available through ScheduleManager could also be accessed through the PST4 GUI.


### Find a Teacher

Teachers can be searched by either:

- Name
- Speciality

The GUI uses:

manager.find_teachers(term)

The search is case-insensitive.

For each matching teacher, the GUI displays:

- Teacher ID
- Teacher name
- Speciality


### List All Teachers

The page displays all teachers currently stored in the system.

For each teacher it shows:

- Teacher ID
- Teacher name
- Speciality


### Register New Teacher

The user can enter:

- Teacher name
- Teacher speciality

The GUI then calls:

manager.register_teacher(name, speciality)

ScheduleManager validates the input, creates the next available teacher ID, creates the teacher and saves the updated data.


### Update Teacher

An existing teacher can be selected and their details can be changed.

The user can update:

- Teacher name
- Teacher speciality

The update uses:

manager.update_teacher(teacher_id, new_name, new_speciality)

The changes are then saved through ScheduleManager.


### Remove Teacher

The GUI also provides the ability to remove a teacher.

The selected teacher is removed using:

manager.remove_teacher(teacher_id)

A warning is displayed before the removal is performed.


## Daily Roster

The Daily Roster page is implemented in gui/roster_pages.py.

The user can select:

- Monday
- Tuesday
- Wednesday
- Thursday
- Friday

The GUI calls:

manager.get_lessons_for_day(day)

The returned lessons are displayed in a Pandas DataFrame.

The displayed columns are renamed to make them easier for the user to understand:

- Course
- Instrument
- Start Time
- Room

If there are no lessons for the selected day, the GUI displays a message instead of an empty table.


## Student Check-in

The Daily Roster page also provides the student check-in interface.

Instead of requiring the user to manually type student and course IDs, the GUI uses dropdown menus.

Students are displayed using both their ID and name.

For example:

1 - Alice Johnson

Including the ID avoids problems if two students have the same name.

After a student is selected, the course dropdown only contains courses that the selected student is actually enrolled in.

The check-in is completed using:

manager.check_in(student_id, course_id)

The backend performs another validation to confirm:

- The student exists
- The course exists
- The student is enrolled in the selected course

If all validation succeeds, an attendance record containing the student ID, course ID and current timestamp is added to the attendance log and saved to JSON.

This means the GUI helps prevent invalid input while the backend still performs its own validation.


## JSON Persistence

The project continues to use data/msms.json for persistent storage.

When ScheduleManager starts, _load_data() reads the JSON data and recreates the student, teacher and course objects.

The JSON file stores:

- Students
- Teachers
- Courses
- Lessons
- Course enrolments
- Attendance records

When information is changed, ScheduleManager uses _save_data() to write the updated objects and attendance information back to the JSON file.

This means changes such as registrations, enrolments, updates, removals, course switches and check-ins are not only changed in the GUI. They are also persisted to the data file.


## GUI and Backend Design

One of the main design choices in PST4 was to keep the GUI and business logic separate.

The Streamlit files are mainly responsible for:

- Displaying information
- Getting input from the user
- Providing dropdowns and forms
- Showing success, warning and error messages
- Calling the appropriate ScheduleManager methods

ScheduleManager remains responsible for:

- Finding students and courses
- Registering users
- Managing enrolments
- Switching courses
- Updating users
- Removing users
- Recording attendance
- Saving and loading data

This avoids unnecessarily duplicating the business logic inside the GUI.

For example, the GUI filters the check-in course dropdown so the user only sees courses they are enrolled in. However, ScheduleManager.check_in() still checks the enrolment itself.

This provides validation at both the presentation layer and the business logic layer.


## Additional Improvements and Initiative

In addition to implementing the main PST4 GUI requirements, I made several improvements to make the GUI more complete and to maintain the functionality developed in previous PSTs.


### PST3 Functionality Available Through the GUI

Instead of only exposing the minimum student registration, search, roster and check-in functionality, I added GUI access to the management features that were already available in PST3.

This includes:

- Listing all students
- Enrolling an existing student in another course
- Switching a student's course
- Updating students
- Removing students
- Printing student cards
- Searching teachers
- Listing all teachers
- Registering teachers
- Updating teachers
- Removing teachers

This allows the Streamlit interface to act as a more complete replacement for the previous command-line menu rather than losing functionality when moving to a GUI.


### Exact Course Selection During Registration

The original registration process could identify a course using the student's selected instrument.

However, the data contains more than one course for some instruments. For example, Piano has both Beginner Piano and Intermediate Piano.

I updated register_new_student() so it can optionally receive a specific course ID:

register_new_student(name, instrument, course_id=None)

The GUI allows the user to select the exact course they want.

The optional default value keeps the method compatible with code that only provides the student's name and instrument.


### Dynamic Course Filtering

Course dropdowns are filtered based on the current situation.

Examples include:

- Registration only shows courses matching the selected instrument.
- Enrolment only shows courses the student is not already enrolled in.
- Course switching only shows the student's current courses as the source course.
- The destination course only shows courses the student is not already enrolled in.
- Check-in only shows courses the student is enrolled in.

This reduces invalid choices before they reach the backend.


### Check-in Validation

I also added an enrolment check inside ScheduleManager.check_in().

Even though the GUI already filters the available courses, the backend independently verifies that the selected student is enrolled in the selected course.

This means invalid attendance cannot be recorded simply by bypassing the GUI.


### User-Friendly Student Selection

Where students are selected for management operations, the GUI displays both their ID and name.

For example:

1 - Alice Johnson

This makes the selection clearer and prevents students with identical names from overwriting each other when the options are mapped to IDs.


### Empty Data Handling

The GUI checks situations where information may not be available.

Examples include:

- No students registered
- No teachers registered
- No lessons on a selected day
- No student search results
- No teacher search results
- A student with no course enrolments
- A student already enrolled in every available course
- A student with no other available course to switch to

Instead of crashing or displaying invalid controls, the GUI provides an appropriate message.


## How to Run the Program

The program should be run from the msms-project directory.

The standard Streamlit command is:

streamlit run main.py

On my current development environment, I can also run Streamlit directly using the Python executable from the project virtual environment:

../../.venv/Scripts/python.exe -m streamlit run main.py

Streamlit will start the application and provide a local address that can be opened in a browser.


## How to Use the Program

After the application starts, use the sidebar to move between:

1. Student Management
2. Teacher Management
3. Daily Roster
4. Payments (stub)

Student Management can be used to search, register, list, enrol, switch, update, remove and print cards for students.

Teacher Management can be used to search, list, register, update and remove teachers.

Daily Roster can be used to view lessons for a selected weekday and check students into courses.

Payments currently displays a placeholder because this functionality is planned for PST5.


## Manual Testing Performed

After completing the implementation, I manually tested the complete application.

The following tests were performed.


### Navigation Testing

1. Opened Student Management.
2. Opened Teacher Management.
3. Opened Daily Roster.
4. Opened the Payments placeholder.
5. Switched between the pages and confirmed that the application continued running without errors.


### Student Search Testing

1. Searched for "Ali".
2. Confirmed Alice Johnson was returned.
3. Confirmed both of Alice's enrolled courses were displayed.
4. Searched for "bob" using lowercase letters.
5. Confirmed Bob Williams was returned, showing that the search is case-insensitive.
6. Searched for "XYZ".
7. Confirmed that the GUI displayed "No students found."


### Student Registration Testing

1. Selected Piano as the first instrument.
2. Confirmed both Beginner Piano and Intermediate Piano were available.
3. Registered a temporary PST4 test student specifically into Intermediate Piano.
4. Confirmed the registration succeeded.
5. Refreshed the displayed page and confirmed the student was listed with Intermediate Piano.


### Student Enrolment Testing

1. Selected the temporary PST4 test student.
2. Confirmed courses they were already enrolled in were excluded from the available course choices.
3. Enrolled the student into Acoustic Guitar Fundamentals.
4. Confirmed the enrolment succeeded.
5. Confirmed the student then had both course enrolments.


### Course Switching Testing

1. Selected the temporary test student.
2. Selected Intermediate Piano as the current course.
3. Selected Beginner Piano as the new course.
4. Completed the course switch.
5. Confirmed Intermediate Piano was removed.
6. Confirmed Beginner Piano was added.
7. Confirmed the student's other Acoustic Guitar Fundamentals enrolment remained unchanged.


### Student Update Testing

1. Selected the temporary student.
2. Changed the student's name.
3. Confirmed the update succeeded.
4. Refreshed the page and confirmed the updated name was displayed.


### Student Card Testing

1. Generated a card for the temporary test student.
2. Confirmed the text file was created successfully.
3. Generated a card for an existing student as an additional test.
4. Confirmed the generated student information and course information were correct.
5. Removed the generated test files after confirming that the feature worked.


### Teacher Search Testing

1. Searched for "Evelyn".
2. Confirmed Dr. Evelyn Keys was returned.
3. Searched for "Piano".
4. Confirmed Dr. Evelyn Keys was also returned because Piano matches the teacher's speciality.
5. Searched for "XYZ".
6. Confirmed the GUI displayed "No teachers found."


### Teacher Management Testing

1. Registered a temporary teacher named PST4 Test Teacher with a Violin speciality.
2. Confirmed the teacher appeared in the teacher list.
3. Updated the teacher's name and speciality.
4. Refreshed the page and confirmed the new information was displayed.
5. Removed the temporary teacher.
6. Confirmed the teacher was no longer displayed.


### Daily Roster Testing

The weekday selector was tested for each available day.

The expected lesson information was displayed for Monday, Tuesday and Wednesday.

Thursday and Friday correctly displayed that there were no lessons scheduled.


### Student Check-in Testing

1. Selected the temporary test student.
2. Confirmed the course dropdown only displayed courses the student was currently enrolled in.
3. Confirmed the course the student had switched away from was no longer available.
4. Checked the student into Beginner Piano.
5. Confirmed the check-in succeeded.
6. Confirmed the backend validation accepted the valid enrolment.


### Student Removal Testing

1. Selected the temporary test student.
2. Removed the student.
3. Confirmed the student disappeared from the student list.
4. Confirmed the application continued to operate normally after the removal.


### Test Data Cleanup

Temporary students, teachers, attendance changes and generated student-card files were only used to test the functionality.

After testing was completed, data/msms.json was restored so that the temporary testing data was not included in the final project data.


## Design Choices and Assumptions

The following design choices and assumptions were used in PST4.

- ScheduleManager remains the main controller for the application's business logic.
- Streamlit is used as the presentation layer.
- The GUI calls existing ScheduleManager methods instead of reimplementing the same logic.
- The ScheduleManager is stored in st.session_state so the same manager object remains available while navigating the application.
- JSON remains the persistence method used by the previous PST.
- A student may be enrolled in multiple courses.
- A student may only check in to a course they are enrolled in.
- Course selection is based on the courses currently available in ScheduleManager.
- Student IDs and teacher IDs continue to be generated by the existing backend.
- The GUI uses IDs internally even when more readable names are shown to the user.
- The Payments page is intentionally left as a PST5 placeholder.


## Current Limitations

The current implementation has some limitations which could be improved in a future PST.

- Some information displayed earlier on a Streamlit page does not visually refresh immediately after an update or enrolment is completed later on the same page. The actual change is still saved correctly. Navigating to another page and returning refreshes the displayed information. Improving automatic GUI refresh behaviour is planned for PST5.

- Payments are not implemented because this functionality is planned for PST5.

- Student cards are currently generated as text files rather than a graphical or printable card format.

- The project continues to use a JSON file rather than a database, which is appropriate for the current project size but would be less suitable for a much larger system.

- Course and lesson creation are not currently managed through the PST4 GUI. The GUI operates using the courses and lessons already stored in the system.

- Removing a teacher does not automatically reassign any courses that reference that teacher. Teacher removal should therefore be used carefully for teachers who are currently assigned to courses.

These limitations do not prevent the implemented PST4 functionality from operating, but they identify areas that could be improved as the MSMS continues to develop.


## Summary

PST4 changes the Music School Management System from a mainly command-line based system into a Streamlit graphical application while continuing to use the object-oriented backend developed in PST3.

The required student registration, student search, daily roster and student check-in functionality are available through the GUI.

I also extended the interface so that the previous student and teacher management functionality can continue to be used through Streamlit instead of being lost when moving away from the command-line interface.

The final PST4 system therefore combines:

- The existing ScheduleManager business logic
- JSON persistence
- Streamlit navigation and forms
- Student management
- Teacher management
- Daily lesson roster
- Attendance check-in
- Input filtering and backend validation
- Additional GUI access to functionality developed in previous PSTs

The project is structured so that the GUI remains separate from the main business logic, making it easier to continue extending the system in future PSTs.