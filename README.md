# FIT1056-PSTs-37403834

## PST5 - Quality Assurance and Finance Music School Management System (MSMS)

This project is the fifth and final stage of my Music School Management System (MSMS), developed throughout the FIT1056 Practical Skills Tasks.

In PST3, I implemented the object-oriented backend using `ScheduleManager`, and in PST4, I developed a Streamlit graphical user interface (GUI). For PST5, I continued improving the same application by introducing financial management, logging, backups and automated testing.

The main goal of PST5 was to improve the reliability and functionality of the system while preserving the features developed in previous PSTs.

I also implemented additional improvements, including course management and the ability to add, update and cancel scheduled lessons directly through the GUI.

The completed application supports:

- Student registration, searching, updating and removal.
- Teacher registration, searching, updating and removal.
- Course creation, updating and removal.
- Student enrolment and course switching.
- Viewing scheduled lessons through the daily roster.
- Adding, updating and cancelling lessons.
- Student attendance check-in.
- Recording payments and viewing payment history.
- Exporting reports to CSV files through the backend.
- Logging important application events.
- Automatic and manual JSON backups.
- Automated backend testing using pytest.

---

## Project Structure

The project is organised into separate folders for the backend, GUI, data and tests.

```text
msms-project/
|
|-- app/
|   |-- schedule.py
|   |-- student.py
|   |-- teacher.py
|   |-- user.py
|
|-- data/
|   |-- backups/
|   |-- msms.json
|
|-- gui/
|   |-- course_pages.py
|   |-- finance_pages.py
|   |-- main_dashboard.py
|   |-- roster_pages.py
|   |-- student_pages.py
|   |-- teacher_pages.py
|
|-- tests/
|   |-- __init__.py
|   |-- test_schedule_manager.py
|
|-- main.py
|-- MSMS.py
|-- .gitignore
|-- README.md
```

The main files are:

- `main.py` - starts the Streamlit application and initialises the administrative functionality.
- `app/schedule.py` - contains `ScheduleManager` and the main business logic.
- `app/student.py` - contains the student class.
- `app/teacher.py` - contains the teacher and course classes.
- `app/user.py` - contains the base user class.
- `gui/main_dashboard.py` - provides the dashboard and navigation.
- `gui/student_pages.py` - contains student management.
- `gui/teacher_pages.py` - contains teacher management.
- `gui/course_pages.py` - contains course management.
- `gui/roster_pages.py` - contains the daily roster, lesson management and check-in.
- `gui/finance_pages.py` - contains payment recording and payment history.
- `tests/test_schedule_manager.py` - contains automated backend tests.
- `data/msms.json` - stores persistent application data.
- `data/backups/` - stores backup copies of the JSON file.

The PST5 instructions also specify an administrative utilities module, `app/admin_utils.py`, containing the logging and backup functions. This module should be included in the project if it is not already present.

---

## Main Dashboard

The main dashboard is implemented in `gui/main_dashboard.py`.

It provides navigation between the following pages:

- Dashboard
- Student Management
- Teacher Management
- Course Management
- Daily Roster
- Payments

The dashboard displays summary information about the music school, including registered students, teachers and courses.

I also added a manual backup option labelled **Backup Data Now**.

This allows administrators to create a backup without leaving the application.

The dashboard continues using the same `ScheduleManager` object across the different pages, so all pages work with the same application data.

---

## Student Management

The Student Management page remains in `gui/student_pages.py`.

I preserved the functionality developed in PST4, including:

- Finding a student.
- Registering a new student.
- Listing all students.
- Enrolling students in courses.
- Switching student courses.
- Updating student information.
- Removing students.
- Printing student cards.

The GUI continues calling the corresponding `ScheduleManager` methods instead of implementing the business logic itself.

For example:

```python
manager.register_new_student(...)
manager.enrol_student(...)
manager.update_student(...)
manager.remove_student(...)
```

I kept the student selection dropdowns and course filtering functionality introduced in PST4.

These features make the interface easier to use and help prevent invalid selections.

---

## Teacher Management

The Teacher Management page remains in `gui/teacher_pages.py`.

It supports:

- Finding teachers.
- Listing teachers.
- Registering teachers.
- Updating teacher information.
- Removing teachers.

The GUI uses the existing teacher management methods in `ScheduleManager`.

Teacher IDs are used internally to identify records, while the GUI displays readable information for administrators.

I kept this functionality unchanged where possible to avoid breaking the features developed in previous PSTs.

---

## Finance and Reporting Engine - Fragment 5.1

Fragment 5.1 required me to extend the backend with financial transactions and reporting.

I implemented this functionality in `app/schedule.py` inside the existing `ScheduleManager` class.

### Finance Log

I introduced a `finance_log` list to store payment records.

I updated the following methods to support this new data:

- `__init__()`
- `_load_data()`
- `_save_data()`

The finance log is loaded when the application starts and saved whenever the stored information changes.

This ensures payment records remain available between executions.

### Recording Payments

I implemented:

```python
record_payment(student_id, amount, method)
```

This method receives:

- `student_id` - the student making the payment.
- `amount` - the payment amount.
- `method` - the payment method.

The method checks whether the student exists and validates the payment information.

If the details are valid, it creates a payment record, adds it to the finance log and saves the updated data.

The method returns a result indicating whether the operation succeeded.

I kept this validation in the backend so that invalid payments cannot be accepted simply by bypassing the GUI.

### Payment History

I implemented:

```python
get_payment_history(student_id)
```

This method retrieves payment records associated with a particular student.

It searches the finance log and returns the matching records.

The Finance GUI uses this method when an administrator requests a student's payment history.

### CSV Reporting

I implemented:

```python
export_report(kind, out_path)
```

This method exports supported reports into CSV files.

The parameters are:

- `kind` - identifies the report type.
- `out_path` - specifies where the file should be saved.

I used Python's CSV functionality because CSV files can be opened in spreadsheet applications and are easy to inspect.

I kept reporting in the backend so it can be used independently of Streamlit.

---

## Finance GUI - Fragment 5.2

For Fragment 5.2, I created `gui/finance_pages.py` to replace the Payments placeholder from PST4.

The main function is:

```python
show_finance_page(manager)
```

The page contains two sections.

### Record New Payment

The administrator can:

1. Select a registered student.
2. Enter a payment amount.
3. Enter a payment method.
4. Submit the payment.

The student dropdown displays the student's ID and name.

This avoids requiring administrators to manually remember student IDs.

When the form is submitted, the GUI calls:

```python
manager.record_payment(student_id, amount, method)
```

If the payment succeeds, the application displays a success message.

If the details are invalid, it displays a warning or error.

I used a Streamlit form to group the payment information before submission.

### Student Payment History

The second section allows administrators to view previous payments.

The administrator selects a student and clicks **View Payment History**.

The GUI calls:

```python
manager.get_payment_history(student_id)
```

The returned records are displayed using a pandas DataFrame.

If the student has no payments, an informative message is displayed instead of an empty table.

### Finance GUI Design

I kept the finance GUI separate from the backend.

The GUI handles:

- Collecting user input.
- Displaying payment records.
- Showing success and error messages.

`ScheduleManager` handles:

- Validating payment information.
- Recording transactions.
- Retrieving payment history.
- Saving data.

This follows the same separation of responsibilities used throughout the application.

---

## Logging and Backups - Fragment 5.3

Fragment 5.3 required logging and backup functionality to improve the application's reliability.

The PST5 instructions specify two administrative functions:

```python
init_logger(log_file)
backup_data(data_path, backup_dir)
```

### Logging

The logging functionality uses Python's built-in `logging` module.

The application records important events in:

```text
msms.log
```

Logging is useful because it provides information about operations performed while the application is running.

The main logging levels are:

- `INFO` - normal operations.
- `WARNING` - events requiring attention.
- `ERROR` - errors or unsuccessful operations where appropriate.

For example, adding or updating a lesson produces an informational log message.

Cancelling a lesson records a warning containing the cancellation reason.

This makes it easier to understand what happened during an operation.

### Backups

The backup functionality creates copies of the application's JSON data.

The main file is:

```text
data/msms.json
```

Backups are stored in:

```text
data/backups/
```

The backup utility creates a separate copy of the data file with a timestamp.

This allows multiple backups to be distinguished from one another.

Backups are important because the application stores information about students, teachers, courses, attendance and payments.

Creating copies helps reduce the risk of losing information through accidental changes.

---

## Logging and Backup Integration - Fragment 5.4

After implementing the administrative utilities, I integrated them into the application.

### Startup Logging

The logging system is initialised when the application starts.

This allows important events to be recorded during normal operation.

### Backend Logging

I added logging statements to relevant backend methods.

For example, lesson creation, updates and cancellations record information about the operation.

Logging is handled by the backend rather than relying only on GUI messages.

This means the operations can still be logged when the methods are called directly.

### Automatic Startup Backup

The application creates a backup of the JSON data during startup.

I used Streamlit session state to prevent unnecessary repeated backups during ordinary GUI reruns.

This was important because Streamlit reruns the application when users interact with widgets.

### Manual Backup

I also added the **Backup Data Now** button.

This allows an administrator to create a backup manually before making important changes.

I included this as an additional usability improvement.

---

## Automated Testing Using pytest

PST5 also required an automated test suite.

I used pytest to test the backend functionality.

The tests are stored in:

```text
tests/test_schedule_manager.py
```

### Testing Approach

I followed the Arrange, Act, Assert pattern.

- **Arrange:** Prepare the required test data.
- **Act:** Call the method being tested.
- **Assert:** Check that the result matches the expected behaviour.

Each test focuses on a particular operation.

This makes it easier to identify which functionality has failed.

### Test Fixture

I used a fixture called:

```python
fresh_manager
```

This provides a fresh manager for testing.

It helps keep tests independent from one another and avoids relying on the application's normal data.

### Core Functionality

The test suite checks important backend operations.

This helps verify that the application continues working after adding new features.

### Additional Lesson Tests

I added three tests for the new lesson management functionality.

**test_add_lesson**

Checks that a new lesson can be added to a course and that its details are stored correctly.

**test_update_lesson**

Checks that an existing lesson can be updated.

**test_cancel_lesson**

Checks that a scheduled lesson can be removed.

### Running the Tests

From the `msms-project` directory, run:

```bash
../../.venv/Scripts/python.exe -m pytest tests/test_schedule_manager.py -v
```

The `-v` option displays detailed test results.

After adding the lesson management tests, my test suite contained 15 tests.

All 15 tests passed during development.

Automated testing is useful because I can rerun the tests after modifying the backend instead of manually checking every method.

---

## Daily Roster

The Daily Roster page is implemented in `gui/roster_pages.py`.

It displays scheduled lessons for a selected weekday.

The GUI calls:

```python
manager.get_lessons_for_day(day)
```

The results are displayed using a pandas DataFrame.

The table includes information such as:

- Course name.
- Instrument.
- Start time.
- Room.

If no lessons are scheduled for the selected day, the application displays an informative message.

I preserved this functionality from PST4 while adding the new lesson management features.

---

## Student Check-in

The Daily Roster page also contains Student Check-in.

The administrator selects a student and one of the courses they are enrolled in.

The GUI calls:

```python
manager.check_in(student_id, course_id)
```

The backend validates the operation and records attendance.

I kept the dynamic course filtering from PST4.

This means the course dropdown only displays courses associated with the selected student.

The check-in functionality remains available alongside the new lesson management features.

---

## JSON Persistence

The application continues using JSON to store its data.

The main file is:

```text
data/msms.json
```

`ScheduleManager` uses:

```python
_load_data()
_save_data()
```

to load and save the information.

The stored data includes:

- Students.
- Teachers.
- Courses.
- Enrolments.
- Scheduled lessons.
- Attendance records.
- Finance records.

When information changes, the updated data is saved.

This means the application retains its information between executions.

I continued using JSON because it was already part of the application architecture from PST2 and PST3.

---

## GUI and Backend Design

I continued using the same design approach introduced in PST4.

The Streamlit GUI is responsible for:

- Displaying information.
- Collecting input.
- Providing forms and dropdowns.
- Calling backend methods.
- Showing results.

The backend is responsible for:

- Validating information.
- Managing application records.
- Performing operations.
- Saving and loading data.
- Recording important events.

For example, the Finance GUI collects payment details, but `ScheduleManager` performs the actual payment recording.

Similarly, the lesson management GUI collects scheduling information, but `ScheduleManager` adds, updates or cancels the lesson.

This makes the application easier to maintain and allows the backend to be tested separately.

---

## Additional Improvements and Initiative

In addition to the required PST5 fragments, I implemented several improvements to make the application more complete.

### Course Management

I created:

```text
gui/course_pages.py
```

The page allows administrators to:

- Create courses.
- View courses.
- Update courses.
- Remove courses.

It uses the existing backend methods:

```python
create_course(...)
update_course(...)
remove_course(...)
```

I added this because courses are an important part of the music school system.

Students enrol in courses, teachers are associated with courses, and scheduled lessons belong to courses.

Providing course management through the GUI means administrators no longer need to manually modify JSON data.

### Schedule New Lesson

I implemented:

```python
add_lesson(course_id, day, start_time, room)
```

This method adds a lesson to an existing course.

It validates the course and required lesson information.

The lesson is stored as a dictionary inside the course's lessons list.

The updated data is then saved.

I added a Streamlit form where administrators can select a course, weekday, start time and room.

### Update Scheduled Lesson

I implemented:

```python
update_lesson(course_id, lesson_index, day, start_time, room)
```

This method updates an existing lesson.

It checks that the course and lesson exist before modifying the information.

The GUI allows the administrator to select an existing lesson and change its details.

I kept the course and lesson selectors outside the update form so that the displayed information updates when a different lesson is selected.

### Cancel Scheduled Lesson

I implemented:

```python
cancel_lesson(course_id, lesson_index, reason)
```

This method removes a scheduled lesson from a course.

It validates the course, lesson index and cancellation reason.

The updated data is saved, and the cancellation reason is recorded in the application log.

I also added a confirmation checkbox in the GUI to reduce accidental cancellations.

### Updated Daily Roster

The Daily Roster page now contains five sections:

1. View Daily Roster.
2. Schedule New Lesson.
3. Update Scheduled Lesson.
4. Cancel Scheduled Lesson.
5. Student Check-in.

This makes the page more practical because administrators can manage the schedule without editing the JSON file.

### Dashboard Improvements

I added Course Management to the main navigation and improved the dashboard overview.

I also included the manual backup option so that administrators can create backups directly through the GUI.

---

## How to Run the Program

The application uses:

- Python 3.
- Streamlit.
- pandas.
- pytest.

It also uses Python standard-library modules for JSON persistence, CSV reporting, logging and backups.

### Starting the Application

Open the `msms-project` directory in VS Code.

Run:

```bash
../../.venv/Scripts/python.exe -m streamlit run main.py
```

Streamlit starts a local server and displays a URL in the terminal.

Open the URL in a browser to access the application.

### Running Automated Tests

From the same directory, run:

```bash
../../.venv/Scripts/python.exe -m pytest tests/test_schedule_manager.py -v
```

This runs the backend test suite.

### Data and Log Files

The application data is stored in:

```text
data/msms.json
```

Backups are stored in:

```text
data/backups/
```

The application log is stored in:

```text
msms.log
```

The commands above use the virtual environment from my development setup. If using a different environment, the equivalent commands are `streamlit run main.py` and `pytest`.

---

## How to Use the Program

After starting the application, use the sidebar to navigate between the pages.

### Dashboard

View summary information and create a manual backup.

### Student Management

Register, search, list, enrol, update and remove students.

### Teacher Management

Register, search, list, update and remove teachers.

### Course Management

Create, view, update and remove courses.

### Daily Roster

View scheduled lessons, add lessons, update lessons, cancel lessons and record student attendance.

### Payments

Record student payments and view payment history.

---

## Manual Testing Performed

In addition to automated testing, I manually tested the Streamlit interface.

This was important because backend tests do not verify the complete user experience.

### Navigation Testing

- Opened the Dashboard.
- Navigated between the different pages.
- Confirmed the pages displayed correctly.
- Checked that the application continued using the same manager.

### Finance Testing

- Selected a registered student.
- Entered a payment amount and method.
- Submitted the payment.
- Viewed the student's payment history.
- Checked that the payment appeared.
- Checked the message displayed when a student had no payment history.

### Course Management Testing

- Created a temporary course.
- Checked that it appeared in the course list.
- Updated the course information.
- Checked that the updated information appeared.
- Removed the temporary course.

### Lesson Management Testing

- Created a temporary scheduled lesson.
- Checked that it appeared in the roster.
- Updated the lesson's day, time and room.
- Checked that the changes appeared.
- Cancelled the lesson with a reason.
- Confirmed the lesson was removed.

### Student Check-in Testing

- Selected a registered student.
- Checked the available enrolled courses.
- Selected a course.
- Completed the check-in.

### Backup Testing

- Started the application.
- Checked the startup backup behaviour.
- Used the manual backup option.
- Checked the backup directory.

### Automated Testing

I ran the pytest test suite after adding the new backend methods.

The final development run contained 15 passing tests.

### Test Data Cleanup

After testing the additional course and lesson features, I restored `data/msms.json` to its previously committed state.

This prevented temporary testing data from being included in the final application.

---

## Design Choices and Assumptions

### Design Choices

- I kept `ScheduleManager` responsible for the business logic.
- I separated the GUI into multiple Python files.
- I continued using JSON for persistent storage.
- I used student, teacher and course IDs to identify records.
- I used dropdown menus to reduce incorrect user input.
- I kept payment validation in the backend.
- I implemented CSV reporting independently of Streamlit.
- I used logging to record important operations.
- I added automatic and manual backups.
- I used pytest to test the backend.
- I added confirmation before cancelling lessons.
- I reused existing data structures when implementing lesson management.

### Assumptions

- The application is used by a music school administrator.
- Students, teachers and courses have unique IDs.
- Students can enrol in multiple courses.
- Courses can contain multiple scheduled lessons.
- Lessons store a weekday, start time and room.
- Administrators enter appropriate lesson times and room details.
- Payment amounts must be valid.
- Payments belong to registered students.
- The application has permission to read and write its data files.
- The program is started from the `msms-project` directory.

---

## Current Limitations

Although the application now supports more functionality, some limitations remain.

- The system uses JSON rather than a database.
- Lesson scheduling does not automatically detect room or teacher conflicts.
- Lesson times are entered as text without complete time-format validation.
- Cancelled lessons are removed from the active schedule, with the reason recorded in the log.
- CSV reporting is implemented in the backend but does not have a dedicated download interface.
- There is no separate login system for administrators, teachers and students.
- Automated testing focuses on the backend rather than browser-based GUI testing.

Possible future improvements include scheduling conflict detection, calendar-based lesson management, more detailed finance reports and user authentication.

---

## Summary

PST5 completes the development of my Music School Management System across the five FIT1056 Practical Skills Tasks.

The main required additions were:

- Finance and reporting functionality.
- A working Finance GUI.
- Logging and backups.
- Integration of administrative utilities.
- Automated testing using pytest.

I also implemented additional course management and lesson management functionality to make the application more complete.

I preserved the existing student management, teacher management, daily roster, attendance and JSON persistence functionality from previous PSTs.

Throughout PST5, I continued applying the concepts learned in FIT1056, including object-oriented programming, modularity, separation of concerns, validation, persistence and testing.

The final result is a more complete and reliable Music School Management System with a Streamlit interface and a testable Python backend.