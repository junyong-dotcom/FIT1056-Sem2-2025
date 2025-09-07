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
                       
    def check_in(self, user_id, course_id):
        """Records a student's attendance for a course after validation."""
    # This implementation remains the same, but it will now function correctly.
        student = self.find_student_by_id(user_id)
        course = self.find_course_by_id(course_id)
    
        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False
        
        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {"user_id": user_id, "course_id": course_id, "timestamp": timestamp}
    
    # This line will now work without causing an AttributeError.
        self.attendance_log.append(check_in_record)
        self._save_data() # This will now correctly save the attendance log.
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True

# TODO: Also implement find_student_by_id and find_course_by_id helper methods.
    def find_student_by_id(self, user_id):
        """Find and return a student object by ID, or None if not found."""
        for student in self.students:
            if student.id == user_id:
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

    def switch_student_course(self, user_id, from_course_id, to_course_id):
        """Switch a student from one course to another."""
        student = self.find_student_by_id(user_id)
        from_course = self.find_course_by_id(from_course_id)
        to_course = self.find_course_by_id(to_course_id)

        if not student:
            return False

        if not from_course_id or not to_course:
            return False  # invalid IDs

        if from_course_id in student.enrolled_course_ids:
            student.enrolled_course_ids.remove(from_course_id)
            if user_id in from_course.enrolled_student_ids:
                from_course.enrolled_student_ids.remove(user_id)
        else:
            return False

        if to_course_id not in student.enrolled_course_ids:
            student.enrolled_course_ids.append(to_course_id)
            if user_id not in to_course.enrolled_student_ids:
                to_course.enrolled_student_ids.append(user_id)

        self._save_data()
        return True

        
