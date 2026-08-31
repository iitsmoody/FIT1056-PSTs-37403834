import json
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