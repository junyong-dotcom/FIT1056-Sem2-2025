#app/teacher.py
from app.user import User

class TeacherUser(User):
    """Represents a teacher."""
    # TODO: Implement the TeacherUser class, inheriting from User.
    # It should have an additional 'speciality' attribute in its __init__.
    def __init__(self, user_id, name, speciality):
        super().__init__(user_id, name)
        self.speciality = speciality

    def to_dict(self):
        return {
         "id": self.id,
        "name": self.name,
        "speciality": self.speciality
        }


class Course:
    """Represents a single course offered by the school, linked to a teacher."""
    def __init__(self, course_id, name, instrument, teacher_id, enrolled_student_ids=None, lessons=None):
        self.id = course_id
        self.name = name
        self.instrument = instrument
        self.teacher_id = teacher_id
        # TODO: Initialize two empty lists: 'enrolled_student_ids' and 'lessons'.
        self.enrolled_student_ids = enrolled_student_ids or []
        self.lessons = lessons or [] # This will hold lesson dictionaries

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "instrument": self.instrument,
            "teacher_id": self.teacher_id,
            "enrolled_student_ids": self.enrolled_student_ids,
            "lessons": self.lessons
        }

class Lesson:
    def __init__(self, lesson_id, course_name, day, start_time, room=""):
        self.lesson_id = lesson_id
        self.course_name = course_name
        self.day = day
        self.start_time = start_time
        self.room = room

    def to_dict(self):
        return {
            "lesson_id": self.lesson_id,
            "course_name": self.course_name,
            "day": self.day,
            "start_time": self.start_time,
            "room": self.room
        }
