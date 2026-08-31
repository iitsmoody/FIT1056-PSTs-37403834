from app.user import User

class TeacherUser(User):
    """Represents a teacher."""
    def __init__(self, user_id, name, speciality):
        # Reuse the User constructor for the shared ID and name attributes.
        super().__init__(user_id, name)
        self.speciality = speciality

class Course:
    """Represents a single course offered by the school, linked to a teacher."""
    def __init__(self, course_id, name, instrument, teacher_id):
        self.id = course_id
        self.name = name
        self.instrument = instrument
        self.teacher_id = teacher_id

        # These lists track enrolled students and the course's scheduled lessons.
        self.enrolled_student_ids = []
        self.lessons = []