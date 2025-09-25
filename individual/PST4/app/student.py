#app/student.py
from app.user import User

class StudentUser(User):
    """Represents a student, inheriting from the base User class."""
    def __init__(self, user_id, name, enrolled_course_ids=None):
        # TODO: Call the parent class's __init__ method using super().
        super().__init__(user_id, name)
        # TODO: Initialize an empty list called 'enrolled_course_ids' to store the IDs of courses.
        self.enrolled_course_ids = enrolled_course_ids or []
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "enrolled_course_ids": self.enrolled_course_ids
        }
    
class Attendance:
    def __init__(self, id, lesson_id, status):
        self.id = id
        self.lesson_id = lesson_id
        self.status = status

class Lesson:
    def __init__(self, lesson_id, course_name, day, start_time, room=""):
        self.lesson_id = lesson_id
        self.course_name = course_name
        self.day = day
        self.start_time = start_time
        self.room = room

    def __str__(self):
        return f"{self.lesson_id} - {self.course_name} ({self.day} {self.start_time})"
