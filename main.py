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

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager() # Create ONE instance of the application brain.
    
    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("1. View Daily Lesson Roster")
        print("2. Switch Student Course")
        print("q. Quit")

        choice = input("Enter choice: ")

        if choice == '1':
            day = input("Enter day (e.g., Monday): ")
            front_desk_daily_roster(manager, day)

        elif choice == '2':
            try:
                student_id = int(input("Enter student ID: "))
                from_course_id = int(input("Enter current course ID: "))
                to_course_id = int(input("Enter new course ID: "))

                switch_course(manager, student_id, from_course_id, to_course_id)

            except ValueError:
                print("Error: IDs must be numbers.")
    

        elif choice.lower() == 'q':
            break
        
if __name__ == "__main__":
    main()