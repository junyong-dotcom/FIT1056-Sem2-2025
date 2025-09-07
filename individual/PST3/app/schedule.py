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
        # TODO: Initialize the new attendance_log attribute as an empty list.
        self.attendance_log = []
        
        self.next_student_id = 1
        self.next_teacher_id = 1
        self.next_course_id = 1

        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                print("Data loaded successfully.")
                # TODO: Load students, teachers, and courses as before.
                #Load students
                self.students = [

                    StudentUser(user_id=s["id"], name=s["name"], enrolled_course_ids=s.get("enrolled_course_ids", []))
                    for s in data.get("students", [])
                ]

                self.teachers = [
                    TeacherUser(user_id=t["id"], name=t["name"], speciality=t["speciality"])
                    for t in data.get("teachers", [])
                ]

                self.courses = []
                for c in data.get("courses", []):
                    course = Course(
                        course_id=c["id"],
                        name=c["name"],
                        instrument=c["instrument"],
                        teacher_id=c["teacher_id"]
                    )
                    course.enrolled_student_ids = c.get("enrolled_student_ids", [])
                    course.lessons = c.get("lessons", [])
                    self.courses.append(course)
                # TODO: Correctly load the attendance log.
                # Use .get() with a default empty list to prevent errors if the key doesn't exist.
        
                self.attendance_log = data.get("attendance", [])
                self.next_student_id = data.get("next_student_id", 1)
                self.next_teacher_id = data.get("next_teacher_id", 1)
                self.next_course_id = data.get("next_course_id", 1)

        except FileNotFoundError:         
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        # TODO: Create a 'data_to_save' dictionary.
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            # TODO: Add the attendance_log to the dictionary to be saved.  
            # ... (next_id counters) ...
            "attendance": self.attendance_log,
            "next_student_id": self.next_student_id,
            "next_teacher_id": self.next_teacher_id,
            "next_course_id": self.next_course_id,
        }
        # TODO: Write 'data_to_save' to the JSON file.
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
    
    # This line will now work without causing an AttributeError.
        self.attendance_log.append(check_in_record)
        self._save_data() # This will now correctly save the attendance log.
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True

# TODO: Also implement find_student_by_id and find_course_by_id helper methods.
    def find_student_by_id(self, student_id):
        """Find and return a student object by ID, or None if not found."""
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def find_course_by_id(self, course_id):
        """Find and return a course object by ID, or None if not found."""
        for course in self.courses:
            if course.id == course_id:
                return course
        return None
    
    def get_lessons_by_day(self, day):
        """Return all lessons scheduled on a given day, with course + teacher info."""
        lessons_for_day = []
        for course in self.courses:
            for lesson in course.lessons:
                if lesson["day"].lower() == day.lower():
                    lessons_for_day.append({
                        "course_id": course.id,
                        "course_name": course.name,
                        "teacher_id": course.teacher_id,
                        "day": lesson["day"],
                        "time": lesson["start_time"],
                        "room": lesson.get("room", "N/A")
                    })
        return lessons_for_day


    def find_teacher_by_id(self, teacher_id):
        """Find and return a teacher object by ID, or None if not found."""
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                return teacher
        return None

    def switch_student_course(self, student_id, from_course_id, to_course_id):
        """Switch a student from one course to another."""
        student = self.find_student_by_id(student_id)
        from_course = self.find_course_by_id(from_course_id)
        to_course = self.find_course_by_id(to_course_id)

        if not student:
            return False

        if not from_course_id or not to_course:
            return False  # invalid IDs

        if from_course_id in student.enrolled_course_ids:
            student.enrolled_course_ids.remove(from_course_id)
            if student_id in from_course.enrolled_student_ids:
                from_course.enrolled_student_ids.remove(student_id)
        else:
            return False

        if to_course_id not in student.enrolled_course_ids:
            student.enrolled_course_ids.append(to_course_id)
            if student_id not in to_course.enrolled_student_ids:
                to_course.enrolled_student_ids.append(student_id)

        self._save_data()
        return True

    def add_student(self, name):
        student = StudentUser(user_id=self.next_student_id, name=name)
        self.students.append(student)
        self.next_student_id += 1
        self._save_data()
        return student

    def add_teacher(self, name, speciality):
        teacher = TeacherUser(user_id=self.next_teacher_id, name=name, speciality=speciality)
        self.teachers.append(teacher)
        self.next_teacher_id += 1
        self._save_data()
        return teacher

    def add_course(self, name, instrument, teacher_id):
        course = Course(course_id=self.next_course_id, name=name, instrument=instrument, teacher_id=teacher_id)
        self.courses.append(course)
        self.next_course_id += 1
        self._save_data()
        return course
    
    def update_student(self, student_id, new_name=None, new_enrolled_courses=None):
        """Update student's name and/or enrolled courses."""
        student = self.find_student_by_id(student_id)
        if not student:
            return False
        if new_name:
            student.name = new_name
        if new_enrolled_courses is not None:
            for course in self.courses:
                if student_id in course.enrolled_student_ids and course.id not in new_enrolled_courses:
                    course.enrolled_student_ids.remove(student_id)
            for cid in new_enrolled_courses:
                course = self.find_course_by_id(cid)
                if course and student_id not in course.enrolled_student_ids:
                    course.enrolled_student_ids.append(student_id)
            student.enrolled_course_ids = new_enrolled_courses
        self._save_data()
        return True

    def remove_student(self, student_id):
        """Remove a student and update all enrolled courses."""
        student = self.find_student_by_id(student_id)
        if not student:
            return False
        for course in self.courses:
            if student_id in course.enrolled_student_ids:
                course.enrolled_student_ids.remove(student_id)
        self.students = [s for s in self.students if s.id != student_id]
        self._save_data()
        return True
    
    def update_teacher(self, teacher_id, new_name=None, new_speciality=None):
            """Update teacher's name and/or speciality."""
            teacher = self.find_teacher_by_id(teacher_id)
            if not teacher:
                return False
            if new_name:
                teacher.name = new_name
            if new_speciality:
                teacher.speciality = new_speciality
            self._save_data()
            return True

    def remove_teacher(self, teacher_id):
        """Remove a teacher and update all associated courses."""
        teacher = self.find_teacher_by_id(teacher_id)
        if not teacher:
            return False
        for course in self.courses:
            if course.teacher_id == teacher_id:
                course.teacher_id = None  
        self.teachers = [t for t in self.teachers if t.id != teacher_id]
        self._save_data()
        return True


    def schedule_lesson(self, course_id, day, start_time, room="N/A"):
        course = self.find_course_by_id(course_id)
        if not course:
            return False
        lesson_id = len(course.lessons) + 1
        course.lessons.append({"lesson_id": lesson_id, "day": day, "start_time": start_time, "room": room})
        self._save_data()
        return True

    def get_student_courses(self, student_id):
        student = self.find_student_by_id(student_id)
        if not student:
            return []
        return [self.find_course_by_id(cid) for cid in student.enrolled_course_ids]

    def get_teacher_courses(self, teacher_id):
        return [course for course in self.courses if course.teacher_id == teacher_id]

    def attendance_report(self, course_id=None, student_id=None):
        report = []
        for record in self.attendance_log:
            if course_id and record["course_id"] != course_id:
                continue
            if student_id and record["student_id"] != student_id:
                continue
            report.append(record)
        return report

#extra functionality
    def get_lessons_by_room(self, room):
        """Return all lessons scheduled in a specific room."""
        lessons_in_room = []
        for course in self.courses:
            for lesson in course.lessons:
                if lesson.get("room", "").lower() == room.lower():
                    lessons_in_room.append({
                        "course_id": course.id,
                        "course_name": course.name,
                        "teacher_id": course.teacher_id,
                        "day": lesson["day"],
                        "time": lesson["start_time"],
                        "room": lesson.get("room", "N/A")
                    })
        return lessons_in_room
