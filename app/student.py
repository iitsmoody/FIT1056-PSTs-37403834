from app.user import User

class StudentUser(User):
    """Represents a student, inheriting from the base User class."""
    def __init__(self, user_id, name):
        # Reuse the User constructor to initialise the shared ID and name attributes.
        super().__init__(user_id, name)
        
        # Store the IDs of courses that this student is enrolled in.
        self.enrolled_course_ids = []