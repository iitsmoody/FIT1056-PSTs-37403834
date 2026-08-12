# MSMS.py - The In-Memory Prototype

# --- Data Models ---
class Student:
    """A blueprint for student objects. Holds their info."""
    def __init__(self, student_id, name):
        self.id = student_id
        self.name = name
        self.enrolled_in = []

class Teacher:
    """A blueprint for teacher objects."""
    def __init__(self, teacher_id, name, speciality):
        self.id = teacher_id
        self.name = name
        self.speciality = speciality

# --- In-Memory Databases ---
student_db = []
teacher_db = []
next_student_id = 1
next_teacher_id = 1



# --- Core Helper Functions ---
def add_teacher(name, speciality):
    """Creates a Teacher object, stores it in the database, and returns it."""
    global next_teacher_id
    new_teacher = Teacher(next_teacher_id, name, speciality)
    teacher_db.append(new_teacher)
    next_teacher_id += 1
    print(f"Core: Teacher '{name}' added successfully.")
    return new_teacher

def list_students():
    """Prints all students in the database."""
    print("\n--- Student List ---")
    if not student_db:
        print("No students in the system.")
        return
    for student in student_db:
        print(f"  ID: {student.id}, Name: {student.name}, Enrolled in: {student.enrolled_in}")

def list_teachers():
    """Prints all teachers in the database."""
    print("\n--- Teacher List ---")
    for teacher in teacher_db:
        print(f"  ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")

def find_students(term):
    """Finds students by name."""
    print(f"\n--- Finding Students matching '{term}' ---")

    results=[]

    for student in student_db:
        if term.lower() in student.name.lower():
            results.append(student)

    if not results:
        print("No matching students found.")
    else:
        for student in results:
            print(f"  ID : {student.id}, Name: {student.name}, Enrolled in: {student.enrolled_in}")

def find_teachers(term):
    """Finds teachers by name or speciality."""
    print(f"\n--- Finding Teachers matching '{term}' ---")

    results= []

    for teacher in  teacher_db:
        if term.lower() in teacher.name.lower() or term.lower() in  teacher.speciality.lower():
            results.append(teacher)

    if not results:
        print("No matching teachers found.")

    else:
        for teacher in results:
            print(f"  ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")


# --- Front Desk Functions ---
def find_student_by_id(student_id):
    """Returns the student with the matching ID, or None if no student is found."""
    for student in student_db:
        if student.id == student_id:
            return student
    return None

def front_desk_register(name, instrument):
    """High-level function to register a new student and enrol them."""
    global next_student_id

    # Remove accidental spaces around the user's input before validating it.
    name=name.strip()
    instrument=instrument.strip()

    # Stop registration before creating a student if required information is missing.
    if not name:
        print("Error: Student name cannot be empty.")
        return

    if not instrument:
        print("Error: Instrument name cannot be empty.")
        return

    new_student = Student(next_student_id, name)
    student_db.append(new_student)
    next_student_id += 1
    
    front_desk_enrol(new_student.id, instrument)
    print(
    f"Registration successful!\n"
    f"Student: {new_student.name}\n"
    f"Student ID: {new_student.id}\n"
    f"Enrolled in: {instrument}")


def front_desk_register_teacher(name, speciality):
    """Registers a new teacher and assigns them a unique teacher ID."""

    # Clean input before validating it.
    name = name.strip()
    speciality = speciality.strip()

    if not name:
        print("Error: Teacher name cannot be empty.")
        return

    if not speciality:
        print("Error: Teacher speciality cannot be empty.")
        return

    new_teacher = add_teacher(name, speciality)

    print(
        f"Teacher registration successful!\n"
        f"Teacher: {new_teacher.name}\n"
        f"Teacher ID: {new_teacher.id}\n"
        f"Speciality: {new_teacher.speciality}"
    )


def front_desk_enrol(student_id, instrument):
    """High-level function to enrol an existing student in an instrument."""
    student = find_student_by_id(student_id)

    if not student:
        print(f"Error: Student ID {student_id} not found.")
        return

    # Clean the instrument name and reject empty input.
    instrument=instrument.strip()

    if not instrument:
        print("Error: Instrument name cannot be empty.")
        return

    # Compare instrument names without considering capitalization.
    for enrolled_instrument in student.enrolled_in:
        if enrolled_instrument.lower() == instrument.lower():
            print(
                f"Error: {student.name} is already enrolled in '{enrolled_instrument}'.")
            return
        
    student.enrolled_in.append(instrument)
    print(
        f"Front Desk: Enrolled {student.name}"
        f"(Student ID: {student.id}) in '{instrument}'."
    )


def front_desk_lookup(term):
    """Searches for matching students and teachers using one search term."""
    term=term.strip()

    # Prevent an empty term from unintentionally matching every record.
    if not term:
        print ("Error: Search term cannot be empty.")
        return
    
    print(f"\n--- Performing lookup for '{term}' ---")
    find_students(term)
    find_teachers(term)

# --- Main Application ---
def main():
    """Runs the main interactive menu for the receptionist."""
    # Pre-populate some data for easy testing
    add_teacher("Dr. Keys", "Piano")
    add_teacher("Ms. Fret", "Guitar")

    while True:
        print("\n===== Music School Front Desk =====")
        print("1. Register New Student")
        print("2. Enrol Existing Student")
        print("3. Lookup Student or Teacher")
        print("4. (Admin) List all Students")
        print("5. (Admin) List all Teachers")
        print("6. (Admin) Register New Teacher")
        print("q. Quit")
        
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            name = input("Enter student name: ").strip()
            # Validate the name before asking for any further registration details.
            if not name:
                print("Error: Student name cannot be empty.")
                continue

            instrument = input("Enter instrument to enrol in: ").strip()

            #Do not attempt registration if an instrument was not provided.
            if not instrument:
                print ("Error: Instrument name cannot be empty.")
                continue

            front_desk_register(name, instrument)
        elif choice == '2':
            try:
                student_id = int(input("Enter student ID: "))            
            except ValueError:
                print("Invalid ID. Please enter a number.")
                continue
            # Check that the student exists before asking for an instrument.
            student = find_student_by_id(student_id)

            if not student:
                print(f"Error: Student ID {student_id} not found.")
                continue


            instrument = input("Enter instrument to enrol in: ").strip()

            if not instrument:
                print("Error: Instrument name cannot be empty.")
                continue

            front_desk_enrol(student_id, instrument)

        elif choice == '3':
            term = input("Enter search term: ").strip()

            # Prevent an empty search from matching every record in the system.
            if not term:
                print("Error: Search term cannot be empty.")
                continue
            front_desk_lookup(term)
        elif choice == '4':
            list_students()
        elif choice == '5':
            list_teachers()
        elif choice == '6':
            name= input("Enter teacher name: ").strip()

            # Validate the teacher name before asking for further details.
            if not name:
                print("Error: Teacher name cannot be empty.")
                continue
            speciality=input("Enter teacher speciality: ").strip()

            if not speciality:
                print("Error: teacher speciality cannot be empty.")
                continue

            front_desk_register_teacher(name,speciality)

        elif choice.lower() == 'q':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# --- Program Start ---
if __name__ == "__main__":
    main()
