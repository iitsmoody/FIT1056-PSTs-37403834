# MSMS.py - The In-Memory Prototype

# --- Data Models ---
class Student:
    """A blueprint for student objects. Hold their info."""
    def __init__(self,student_id,name):
        self.id=student_id
        self.name=name
        self.enrolled_in=[]


student1= Student(1,"Mohammed")

print(student1.id)
print(student1.name)
print(student1.enrolled_in)