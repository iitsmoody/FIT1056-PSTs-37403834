# main.py - The View Layer
from app.schedule import ScheduleManager

def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""
    print(f"\n--- Daily Roster for {day} ---")
    # Notice: This code does not need to change. It doesn't care where the Course class lives.
    # It only talks to the manager.

    lessons = manager.get_lessons_for_day(day)

    if not lessons:
        print("No lessons scheduled for this day.")
        return

    for lesson in lessons:
        print(
            f"Course: {lesson['course_name']}, "
            f"Instrument: {lesson['instrument']}, "
            f"Time: {lesson['start_time']}, "
            f"Room: {lesson['room']}"
        )

        
def switch_course(manager, student_id, from_course_id, to_course_id):
    """Requests the manager to move a student between courses."""
    manager.switch_student_course(student_id, from_course_id, to_course_id)

def front_desk_list_students(manager):
    """Displays all registered students."""
    print("\n--- Student List ---")

    if not manager.students:
        print("No students in the system.")
        return

    for student in manager.students:
        print(
            f"ID: {student.id}, "
            f"Name: {student.name}, "
            f"Course IDs: {student.enrolled_course_ids}"
        )


def front_desk_list_teachers(manager):
    """Displays all registered teachers."""
    print("\n--- Teacher List ---")

    if not manager.teachers:
        print("No teachers in the system.")
        return

    for teacher in manager.teachers:
        print(
            f"ID: {teacher.id}, "
            f"Name: {teacher.name}, "
            f"Speciality: {teacher.speciality}"
        )


def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager() # Create ONE instance of the application brain.
    
    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("1. View Daily Lesson Roster")
        print("2. Switch Student Course")
        print("3. Register New Student")
        print("4. Register New Teacher")
        print("5. Enrol Student in Course")
        print("6. Search Student or Teacher")
        print("7. List All Students")
        print("8. List All Teachers")
        print("9. Update Student")
        print("10. Update Teacher")
        print("11. Remove Student")
        print("12. Remove Teacher")
        print("13. Check-in Student")
        print("14. Print Student Card")
        print("q. Quit")

        choice = input("Enter choice: ").strip()

        if choice == '1':
            day = input("Enter day (e.g., Monday): ")
            front_desk_daily_roster(manager, day)

        elif choice == '2':
            try:
                student_id = int(input("Enter student ID: "))
                from_course_id = int(input("Enter current course ID: "))
                to_course_id = int(input("Enter new course ID: "))

                switch_course(
                    manager,
                    student_id,
                    from_course_id,
                    to_course_id
                )

            except ValueError:
                print("Error: IDs must be numbers.")

        elif choice == '3':
            name = input("Enter student name: ")
            manager.register_student(name)

        elif choice == '4':
            name = input("Enter teacher name: ")
            speciality = input("Enter teacher speciality: ")
            manager.register_teacher(name, speciality)

        elif choice == '5':
            try:
                student_id = int(input("Enter student ID: "))
                course_id = int(input("Enter course ID: "))
                manager.enrol_student(student_id, course_id)

            except ValueError:
                print("Error: IDs must be numbers.")

        elif choice == '6':
            term = input("Enter search term: ").strip()

            if not term:
                print("Error: Search term cannot be empty.")

            else:
                students = manager.find_students(term)
                teachers = manager.find_teachers(term)

                print("\n--- Matching Students ---")

                if not students:
                    print("No matching students found.")
                else:
                    for student in students:
                        print(
                            f"ID: {student.id}, "
                            f"Name: {student.name}, "
                            f"Course IDs: {student.enrolled_course_ids}"
                        )

                print("\n--- Matching Teachers ---")

                if not teachers:
                    print("No matching teachers found.")
                else:
                    for teacher in teachers:
                        print(
                            f"ID: {teacher.id}, "
                            f"Name: {teacher.name}, "
                            f"Speciality: {teacher.speciality}"
                        )

        elif choice == '7':
            front_desk_list_students(manager)

        elif choice == '8':
            front_desk_list_teachers(manager)

        elif choice == '9':
            try:
                student_id = int(input("Enter student ID: "))
                new_name = input("Enter new student name: ")
                manager.update_student(student_id, new_name)

            except ValueError:
                print("Error: Student ID must be a number.")

        elif choice == '10':
            try:
                teacher_id = int(input("Enter teacher ID: "))

                new_name = input(
                    "Enter new teacher name "
                    "(leave blank to keep current): "
                )

                new_speciality = input(
                    "Enter new speciality "
                    "(leave blank to keep current): "
                )

                manager.update_teacher(
                    teacher_id,
                    new_name,
                    new_speciality
                )

            except ValueError:
                print("Error: Teacher ID must be a number.")

        elif choice == '11':
            try:
                student_id = int(
                    input("Enter student ID to remove: ")
                )

                manager.remove_student(student_id)

            except ValueError:
                print("Error: Student ID must be a number.")

        elif choice == '12':
            try:
                teacher_id = int(
                    input("Enter teacher ID to remove: ")
                )

                manager.remove_teacher(teacher_id)

            except ValueError:
                print("Error: Teacher ID must be a number.")

        elif choice == '13':
            try:
                student_id = int(input("Enter student ID: "))
                course_id = int(input("Enter course ID: "))

                manager.check_in(student_id, course_id)

            except ValueError:
                print("Error: IDs must be numbers.")

        elif choice == '14':
            try:
                student_id = int(input("Enter student ID: "))
                manager.print_student_card(student_id)

            except ValueError:
                print("Error: Student ID must be a number.")

        elif choice.lower() == 'q':
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
        
if __name__ == "__main__":
    main()