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