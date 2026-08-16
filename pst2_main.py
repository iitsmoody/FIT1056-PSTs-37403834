# pst2_main.py - The Persistent Application

import json
import datetime

DATA_FILE = "msms.json"
app_data = {} # This global dictionary will hold ALL our data.

# --- Core Persistence Engine ---
def load_data(path=DATA_FILE):
    """Loads all application data from a JSON file."""
    global app_data
    try:
        with open(path, 'r') as f:
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }

def save_data(path=DATA_FILE):
    """Saves all application data to a JSON file."""
    with open(path, 'w') as f:
        json.dump(app_data, f, indent=4)
    print("Data saved successfully.")



# --- Full CRUD for Core Data ---
# Note: We are now working with lists of dictionaries, not lists of objects.

def add_teacher(name, speciality):
    """Adds a teacher dictionary to the data store."""
    teacher_id = app_data['next_teacher_id']

    new_teacher = {
        "id": teacher_id,
        "name": name,
        "speciality": speciality
    }

    app_data['teachers'].append(new_teacher)
    app_data['next_teacher_id'] += 1

    print(f"Core: Teacher '{name}' added.")


def update_teacher(teacher_id, **fields):
    """Finds a teacher by ID and updates their data with provided fields."""
    for teacher in app_data['teachers']:
        if teacher['id'] == teacher_id:
            teacher.update(fields)
            print(f"Teacher {teacher_id} updated.")
            return

    print(f"Error: Teacher with ID {teacher_id} not found.")


def remove_teacher(teacher_id):
    """Removes a teacher from the data store."""
    for teacher in app_data['teachers']:
        if teacher['id'] == teacher_id:
            app_data['teachers'].remove(teacher)
            print(f"Teacher {teacher_id} removed.")
            return

    print(f"Error: Teacher with ID {teacher_id} not found.")


def update_student(student_id, **fields):
    """Finds a student by ID and updates their data with provided fields."""
    for student in app_data['students']:
        if student['id'] == student_id:
            student.update(fields)
            print(f"Student {student_id} updated.")
            return

    print(f"Error: Student with ID {student_id} not found.")


def remove_student(student_id):
    """Removes a student from the data store."""
    for student in app_data['students']:
        if student['id'] == student_id:
            app_data['students'].remove(student)
            print(f"Student {student_id} removed.")
            return

    print(f"Error: Student with ID {student_id} not found.")



# --- New Receptionist Features ---
def check_in(student_id, course_id, timestamp=None):
    """Records a student's attendance for a course."""
    if timestamp is None:
        timestamp = datetime.datetime.now().isoformat()

    check_in_record = {
        "student_id": student_id,
        "course_id": course_id,
        "timestamp": timestamp
    }

    app_data['attendance'].append(check_in_record)
    print(f"Receptionist: Student {student_id} checked into {course_id}.")


def print_student_card(student_id):
    """Creates a text file badge for a student."""
    student_to_print = None

    for student in app_data['students']:
        if student['id'] == student_id:
            student_to_print = student
            break

    if student_to_print:
        filename = f"{student_id}_card.txt"

        with open(filename, 'w') as f:
            f.write("========================\n")
            f.write("  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student_to_print['id']}\n")
            f.write(f"Name: {student_to_print['name']}\n")
            f.write(
                f"Enrolled In: {', '.join(student_to_print.get('enrolled_in', []))}\n"
            )

        print(f"Printed student card to {filename}.")
    else:
        print(
            f"Error: Could not print card, student {student_id} not found."
        )



# --- Refactored PST1 Helper Functions ---

def list_students():
    """Prints all students stored in app_data."""
    print("\n--- Student List ---")

    if not app_data['students']:
        print("No students in the system.")
        return

    for student in app_data['students']:
        print(
            f"  ID: {student['id']}, "
            f"Name: {student['name']}, "
            f"Enrolled in: {student.get('enrolled_in', [])}"
        )


def list_teachers():
    """Prints all teachers stored in app_data."""
    print("\n--- Teacher List ---")

    if not app_data['teachers']:
        print("No teachers in the system.")
        return

    for teacher in app_data['teachers']:
        print(
            f"  ID: {teacher['id']}, "
            f"Name: {teacher['name']}, "
            f"Speciality: {teacher['speciality']}"
        )


def find_students(term):
    """Finds students by name using a case-insensitive search."""
    print(f"\n--- Finding Students matching '{term}' ---")

    results = []

    for student in app_data['students']:
        if term.lower() in student['name'].lower():
            results.append(student)

    if not results:
        print("No matching students found.")
    else:
        for student in results:
            print(
                f"  ID: {student['id']}, "
                f"Name: {student['name']}, "
                f"Enrolled in: {student.get('enrolled_in', [])}"
            )


def find_teachers(term):
    """Finds teachers by name or speciality using a case-insensitive search."""
    print(f"\n--- Finding Teachers matching '{term}' ---")

    results = []

    for teacher in app_data['teachers']:
        if (
            term.lower() in teacher['name'].lower()
            or term.lower() in teacher['speciality'].lower()
        ):
            results.append(teacher)

    if not results:
        print("No matching teachers found.")
    else:
        for teacher in results:
            print(
                f"  ID: {teacher['id']}, "
                f"Name: {teacher['name']}, "
                f"Speciality: {teacher['speciality']}"
            )


def find_student_by_id(student_id):
    """Returns the student dictionary with the matching ID, or None if not found."""
    for student in app_data['students']:
        if student['id'] == student_id:
            return student

    return None


def front_desk_register(name, instrument):
    """Registers a new student and immediately enrols them in an instrument."""
    name = name.strip()
    instrument = instrument.strip()

    if not name:
        print("Error: Student name cannot be empty.")
        return

    if not instrument:
        print("Error: Instrument name cannot be empty.")
        return

    student_id = app_data['next_student_id']

    new_student = {
        "id": student_id,
        "name": name,
        "enrolled_in": []
    }

    app_data['students'].append(new_student)
    app_data['next_student_id'] += 1

    front_desk_enrol(student_id, instrument)

    print(
        f"Registration successful!\n"
        f"Student: {new_student['name']}\n"
        f"Student ID: {new_student['id']}\n"
        f"Enrolled in: {instrument}"
    )


def front_desk_register_teacher(name, speciality):
    """Registers a new teacher and assigns them a unique teacher ID."""
    name = name.strip()
    speciality = speciality.strip()

    if not name:
        print("Error: Teacher name cannot be empty.")
        return

    if not speciality:
        print("Error: Teacher speciality cannot be empty.")
        return

    teacher_id = app_data['next_teacher_id']

    add_teacher(name, speciality)

    print(
        f"Teacher registration successful!\n"
        f"Teacher: {name}\n"
        f"Teacher ID: {teacher_id}\n"
        f"Speciality: {speciality}"
    )


def front_desk_enrol(student_id, instrument):
    """Enrols an existing student in an instrument."""
    student = find_student_by_id(student_id)

    if not student:
        print(f"Error: Student ID {student_id} not found.")
        return

    instrument = instrument.strip()

    if not instrument:
        print("Error: Instrument name cannot be empty.")
        return

    for enrolled_instrument in student.get('enrolled_in', []):
        if enrolled_instrument.lower() == instrument.lower():
            print(
                f"Error: {student['name']} is already enrolled in "
                f"'{enrolled_instrument}'."
            )
            return

    student.setdefault('enrolled_in', []).append(instrument)

    print(
        f"Front Desk: Enrolled {student['name']} "
        f"(Student ID: {student['id']}) in '{instrument}'."
    )


def front_desk_lookup(term):
    """Searches for matching students and teachers using one search term."""
    term = term.strip()

    if not term:
        print("Error: Search term cannot be empty.")
        return

    print(f"\n--- Performing lookup for '{term}' ---")
    find_students(term)
    find_teachers(term)



# --- Main Application Loop ---
def main():
    """Main function to run the MSMS application."""
    load_data()  # Load all saved data when the program starts.

    while True:
        print("\n===== Music School Management System - PST2 =====")
        print("1. Register New Student")
        print("2. Enrol Existing Student")
        print("3. Lookup Student or Teacher")
        print("4. List All Students")
        print("5. List All Teachers")
        print("6. Register New Teacher")
        print("7. Check-in Student")
        print("8. Print Student Card")
        print("9. Update Teacher")
        print("10. Remove Teacher")
        print("11. Update Student")
        print("12. Remove Student")
        print("q. Quit and Save")

        choice = input("Enter your choice: ").strip()

        made_change = False

        if choice == '1':
            name = input("Enter student name: ")
            instrument = input("Enter instrument to enrol in: ")
            front_desk_register(name, instrument)
            made_change = True

        elif choice == '2':
            try:
                student_id = int(input("Enter student ID: "))
                instrument = input("Enter instrument to enrol in: ")
                front_desk_enrol(student_id, instrument)
                made_change = True
            except ValueError:
                print("Error: Student ID must be a number.")

        elif choice == '3':
            term = input("Enter search term: ")
            front_desk_lookup(term)

        elif choice == '4':
            list_students()

        elif choice == '5':
            list_teachers()

        elif choice == '6':
            name = input("Enter teacher name: ")
            speciality = input("Enter teacher speciality: ")
            front_desk_register_teacher(name, speciality)
            made_change = True

        elif choice == '7':
            try:
                student_id = int(input("Enter student ID: "))
                course_id = input("Enter course ID: ").strip()

                if not course_id:
                    print("Error: Course ID cannot be empty.")
                elif find_student_by_id(student_id) is None:
                    print(f"Error: Student ID {student_id} not found.")
                else:
                    check_in(student_id, course_id)
                    made_change = True

            except ValueError:
                print("Error: Student ID must be a number.")

        elif choice == '8':
            try:
                student_id = int(input("Enter student ID: "))
                print_student_card(student_id)
            except ValueError:
                print("Error: Student ID must be a number.")

        elif choice == '9':
            try:
                teacher_id = int(input("Enter teacher ID: "))
                new_name = input(
                    "Enter new teacher name (leave blank to keep current): "
                ).strip()
                new_speciality = input(
                    "Enter new speciality (leave blank to keep current): "
                ).strip()

                fields = {}

                if new_name:
                    fields["name"] = new_name

                if new_speciality:
                    fields["speciality"] = new_speciality

                if fields:
                    update_teacher(teacher_id, **fields)
                    made_change = True
                else:
                    print("No changes entered.")

            except ValueError:
                print("Error: Teacher ID must be a number.")

        elif choice == '10':
            try:
                teacher_id = int(input("Enter teacher ID to remove: "))
                remove_teacher(teacher_id)
                made_change = True
            except ValueError:
                print("Error: Teacher ID must be a number.")

        elif choice == '11':
            try:
                student_id = int(input("Enter student ID: "))
                new_name = input(
                    "Enter new student name (leave blank to keep current): "
                ).strip()

                if new_name:
                    update_student(student_id, name=new_name)
                    made_change = True
                else:
                    print("No changes entered.")

            except ValueError:
                print("Error: Student ID must be a number.")

        elif choice == '12':
            try:
                student_id = int(input("Enter student ID to remove: "))
                remove_student(student_id)
                made_change = True
            except ValueError:
                print("Error: Student ID must be a number.")

        elif choice.lower() == 'q':
            print("Saving final changes and exiting.")
            break

        else:
            print("Invalid choice. Please try again.")

        if made_change:
            save_data()

    save_data()


# --- Program Start ---
if __name__ == "__main__":
    main()