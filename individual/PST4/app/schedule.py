#app/schedule.py
import json
from datetime import datetime
from app.student import StudentUser, Attendance, Lesson
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance = []
        self.next_lesson_id = 1
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # The logic here remains the same, but the source of the Course class has changed.

                # TODO: For each dictionary in data['students'], create a StudentUser object and append to self.students.
            self.students = [
            StudentUser(s["id"], s["name"], s.get("enrolled_course_ids", []))
            for s in data.get("students", [])
            ]

                # TODO: Do the same for teachers (creating TeacherUser objects).
            self.teachers = [
            TeacherUser(t["id"], t["name"], t["speciality"])
            for t in data.get("teachers", [])
            ]

                # TODO: Do the same for courses (creating Course objects).
            self.courses = []
            for c in data.get("courses", []):
                course = Course(c["id"], c["name"], c["instrument"], c["teacher_id"])
                course.enrolled_student_ids = c.get("enrolled_student_ids", [])
                course.lessons = [
                    Lesson(l["lesson_id"], course.name, l["day"], l["start_time"])
                    for l in c.get("lessons", [])
                ]
                self.courses.append(course)

            self.attendance = [
                Attendance(a["id"], a["lesson_id"], a["status"])
                for a in data.get("attendance", [])
            ]

        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        # The logic here remains the same.
        # TODO: Create a 'data_to_save' dictionary.
        # Convert self.students, self.teachers, and self.courses into lists of dictionaries.
        data_to_save = {
            "students": [
                {"id": s.id, "name": s.name, "enrolled_course_ids": s.enrolled_course_ids}
                for s in self.students
            ],
            "teachers": [
                {"id": t.id, "name": t.name, "speciality": t.speciality}
                for t in self.teachers
            ],
            "courses": [
                {
                    "id": c.id,
                    "name": c.name,
                    "instrument": c.instrument,
                    "teacher_id": c.teacher_id,
                    "enrolled_student_ids": c.enrolled_student_ids,
                    "lessons": [
                        {
                            "lesson_id": l.lesson_id,
                            "course_name": l.course_name,
                            "day": l.day,
                            "start_time": l.start_time,
                            "room": l.room
                        }
                        for l in c.lessons
                    ],
                }
                for c in self.courses
            ],

            "attendance": [a.__dict__ for a in self.attendance]
        }

        # Write the result to the JSON file.
        with open(self.data_path, "w") as f:
            json.dump(data_to_save, f, indent=4)

    def find_student(self, name_query):
        if not name_query:
            return []
        q = name_query.strip().lower()
        return [s for s in self.students if q in s.name.lower()]

    def find_student_by_id(self, student_id):
        for s in self.students:
            if s.id == student_id:
                return s
        return None

    def find_course_by_id(self, course_id):
        for c in self.courses:
            if c.id == course_id:
                return c
        return None

    def find_teacher_by_id(self, teacher_id):
        for t in self.teachers:
            if t.id == teacher_id:
                return t
        return None
    
    def register_new_student(self, name, instrument):
        name = name.strip()
        instrument = instrument.strip()
        if not name or not instrument:
            return None

        matching_courses = [c for c in self.courses if c.instrument.lower() == instrument.lower()]
        if not matching_courses:
            return None

        new_id = max((s.id for s in self.students), default=0) + 1
        new_student = StudentUser(new_id, name, enrolled_course_ids=[])
        self.students.append(new_student)

        course = matching_courses[0]
        if new_student.id not in course.enrolled_student_ids:
            course.enrolled_student_ids.append(new_student.id)
        if course.id not in new_student.enrolled_course_ids:
            new_student.enrolled_course_ids.append(course.id)

        self._save_data()
        return new_student

    def check_in(self, student_id, course_id, day=None):
        course = self.find_course_by_id(course_id)
        student = self.find_student_by_id(student_id)
        if course is None or student is None:
            return False

        if student_id not in course.enrolled_student_ids:
            return False

        timestamp = datetime.now().isoformat()
        self.attendance.append({
            "student_id": student_id,
            "course_id": course_id,
            "timestamp": timestamp
        })
        self._save_data()
        return True

    def _attendance_on_day(self, student_id, course_id, day_name):
        """
        Helper: return True if there is an attendance entry for (student, course) whose timestamp falls on day_name.
        day_name should be e.g. "Monday".
        """
        for a in self.attendance:
            if a.get("student_id") == student_id and a.get("course_id") == course_id:
                ts = a.get("timestamp")
                try:
                    dt = datetime.fromisoformat(ts)
                except Exception:
                    continue
                if dt.strftime("%A") == day_name:
                    return True
        return False

    def get_roster_for_day(self, day_name):
        roster = []
        for c in self.courses:
            teacher = self.find_teacher_by_id(c.teacher_id)
            for lesson in c.lessons:
                if lesson.day != day_name:
                    continue
                for sid in c.enrolled_student_ids:
                    student = self.find_student_by_id(sid)
                    roster.append({
                        "Course": c.name,
                        "Instrument": c.instrument,
                        "Time": lesson.start_time,
                        "Room": getattr(lesson, "room", ""),
                        "Teacher": teacher.name if teacher else "",
                        "Student": student.name if student else f"ID {sid}",
                        "CheckedIn": self._attendance_on_day(sid, c.id, day_name)
                    })
        return roster
