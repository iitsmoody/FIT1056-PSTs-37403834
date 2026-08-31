import json
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []

        # ... (next_id counters) ...
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)

                # Convert each saved student dictionary into a StudentUser object.
                for student_data in data["students"]:
                    student = StudentUser(
                        student_data["id"],
                        student_data["name"]
                    )

                    student.enrolled_course_ids = student_data["enrolled_course_ids"]
                    self.students.append(student)

                # Convert each saved teacher dictionary into a TeacherUser object.
                for teacher_data in data["teachers"]:
                    teacher = TeacherUser(
                        teacher_data["id"],
                        teacher_data["name"],
                        teacher_data["speciality"]
                    )

                    self.teachers.append(teacher)


                # Convert each saved course dictionary into a Course object.
                for course_data in data["courses"]:
                    course = Course(
                        course_data["id"],
                        course_data["name"],
                        course_data["instrument"],
                        course_data["teacher_id"]
                    )

                    course.enrolled_student_ids = course_data["enrolled_student_ids"]
                    course.lessons = course_data["lessons"]

                    self.courses.append(course)


                # Load attendance records. If none exist, use an empty list.
                self.attendance_log = data.get("attendance", [])

        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""

        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            "attendance": self.attendance_log,

            # ... (next_id counters) ...
        }

        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)


    def check_in(self, student_id, course_id):
        """Records a student's attendance for a course after validation."""
        # This implementation remains the same, but it will now function correctly.
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False
        
        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}
    
        # Store the attendance record and immediately save it to the JSON file.
        self.attendance_log.append(check_in_record)
        self._save_data() # This will now correctly save the attendance log.
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True
    

    def find_student_by_id(self, student_id):
        """Finds and returns a student by ID, or None if no student is found."""
        for student in self.students:
            if student.id == student_id:
                return student

        return None


    def find_course_by_id(self, course_id):
        """Finds and returns a course by ID, or None if no course is found."""
        for course in self.courses:
            if course.id == course_id:
                return course

        return None


    def get_lessons_for_day(self, day):
        """Returns all course lessons scheduled for the given day."""
        lessons_for_day = []

        for course in self.courses:
            for lesson in course.lessons:
                if lesson["day"].lower() == day.lower():
                    lessons_for_day.append({
                        "course_name": course.name,
                        "instrument": course.instrument,
                        "start_time": lesson["start_time"],
                        "room": lesson["room"]
                    })

        return lessons_for_day


    def switch_student_course(self, student_id, from_course_id, to_course_id):
        """Moves a student from one course to another."""
        student = self.find_student_by_id(student_id)
        from_course = self.find_course_by_id(from_course_id)
        to_course = self.find_course_by_id(to_course_id)

        if not student or not from_course or not to_course:
            print("Error: Invalid student or course ID.")
            return False

        if from_course_id not in student.enrolled_course_ids:
            print("Error: Student is not enrolled in the original course.")
            return False

        student.enrolled_course_ids.remove(from_course_id)

        if student_id in from_course.enrolled_student_ids:
            from_course.enrolled_student_ids.remove(student_id)

        student.enrolled_course_ids.append(to_course_id)
        to_course.enrolled_student_ids.append(student_id)

        self._save_data()

        print(
            f"Success: {student.name} switched from "
            f"{from_course.name} to {to_course.name}."
        )
        return True


    def register_student(self, name):
        """Registers a new student and saves the updated data."""
        name = name.strip()

        if not name:
            print("Error: Student name cannot be empty.")
            return False

        # Find the next available student ID.
        new_id = 1
        for student in self.students:
            if student.id >= new_id:
                new_id = student.id + 1

        new_student = StudentUser(new_id, name)
        self.students.append(new_student)

        self._save_data()

        print(
            f"Student registration successful!\n"
            f"Student: {new_student.name}\n"
            f"Student ID: {new_student.id}"
        )
        return True


    def register_teacher(self, name, speciality):
        """Registers a new teacher and saves the updated data."""
        name = name.strip()
        speciality = speciality.strip()

        if not name:
            print("Error: Teacher name cannot be empty.")
            return False

        if not speciality:
            print("Error: Teacher speciality cannot be empty.")
            return False

        # Find the next available teacher ID.
        new_id = 1
        for teacher in self.teachers:
            if teacher.id >= new_id:
                new_id = teacher.id + 1

        new_teacher = TeacherUser(new_id, name, speciality)
        self.teachers.append(new_teacher)

        self._save_data()

        print(
            f"Teacher registration successful!\n"
            f"Teacher: {new_teacher.name}\n"
            f"Teacher ID: {new_teacher.id}\n"
            f"Speciality: {new_teacher.speciality}"
        )
        return True


    def enrol_student(self, student_id, course_id):
        """Enrols an existing student into an existing course."""
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        if not student:
            print(f"Error: Student ID {student_id} not found.")
            return False

        if not course:
            print(f"Error: Course ID {course_id} not found.")
            return False

        if course_id in student.enrolled_course_ids:
            print(
                f"Error: {student.name} is already enrolled in "
                f"{course.name}."
            )
            return False

        student.enrolled_course_ids.append(course_id)

        if student_id not in course.enrolled_student_ids:
            course.enrolled_student_ids.append(student_id)

        self._save_data()

        print(
            f"Success: {student.name} enrolled in "
            f"{course.name}."
        )
        return True


    def find_students(self, term):
        """Returns students whose names match the search term."""
        results = []

        for student in self.students:
            if term.lower() in student.name.lower():
                results.append(student)

        return results


    def find_teachers(self, term):
        """Returns teachers matching a name or speciality search."""
        results = []

        for teacher in self.teachers:
            if (
                term.lower() in teacher.name.lower()
                or term.lower() in teacher.speciality.lower()
            ):
                results.append(teacher)

        return results


    def update_student(self, student_id, new_name):
        """Updates the name of an existing student."""
        student = self.find_student_by_id(student_id)

        if not student:
            print(f"Error: Student ID {student_id} not found.")
            return False

        new_name = new_name.strip()

        if not new_name:
            print("Error: Student name cannot be empty.")
            return False

        student.name = new_name
        self._save_data()

        print(f"Student {student_id} updated successfully.")
        return True


    def update_teacher(self, teacher_id, new_name, new_speciality):
        """Updates an existing teacher's details."""
        teacher = None

        for current_teacher in self.teachers:
            if current_teacher.id == teacher_id:
                teacher = current_teacher
                break

        if not teacher:
            print(f"Error: Teacher ID {teacher_id} not found.")
            return False

        new_name = new_name.strip()
        new_speciality = new_speciality.strip()

        if new_name:
            teacher.name = new_name

        if new_speciality:
            teacher.speciality = new_speciality

        self._save_data()

        print(f"Teacher {teacher_id} updated successfully.")
        return True


    def remove_student(self, student_id):
        """Removes a student and their course enrolments."""
        student = self.find_student_by_id(student_id)

        if not student:
            print(f"Error: Student ID {student_id} not found.")
            return False

        # Remove the student from any courses they were enrolled in.
        for course in self.courses:
            if student_id in course.enrolled_student_ids:
                course.enrolled_student_ids.remove(student_id)

        self.students.remove(student)
        self._save_data()

        print(f"Student {student_id} removed successfully.")
        return True


    def remove_teacher(self, teacher_id):
        """Removes an existing teacher from the system."""
        teacher = None

        for current_teacher in self.teachers:
            if current_teacher.id == teacher_id:
                teacher = current_teacher
                break

        if not teacher:
            print(f"Error: Teacher ID {teacher_id} not found.")
            return False

        self.teachers.remove(teacher)
        self._save_data()

        print(f"Teacher {teacher_id} removed successfully.")
        return True


    def print_student_card(self, student_id):
        """Creates a text-file ID card for a student."""
        student = self.find_student_by_id(student_id)

        if not student:
            print(
                f"Error: Could not print card, "
                f"student {student_id} not found."
            )
            return False

        course_names = []

        for course_id in student.enrolled_course_ids:
            course = self.find_course_by_id(course_id)

            if course:
                course_names.append(course.name)

        filename = f"{student_id}_card.txt"

        with open(filename, 'w') as f:
            f.write("========================\n")
            f.write("  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student.id}\n")
            f.write(f"Name: {student.name}\n")
            f.write(f"Courses: {', '.join(course_names)}\n")

        print(f"Printed student card to {filename}.")
        return True