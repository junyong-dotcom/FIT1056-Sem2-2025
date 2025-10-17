#app/schedule.py
import json
import csv
import datetime
import logging
from app.student import StudentUser, Attendance
# Corrected Import: TeacherUser and Course now come from the same file.
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance = []
        self.finance_log = []
        self.next_lesson_id = 1
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # The logic here remains the same, but the source of the Course class has changed.

                for s in data.get("students", []):
                    student = StudentUser(
                    user_id=s["id"],
                    name=s["name"],
                    enrolled_course_ids=s.get("enrolled_course_ids", [])
                )
                    self.students.append(student)
                # TODO: For each dictionary in data['students'], create a StudentUser object and append to self.students.

                for t in data.get("teachers", []):
                    teacher = TeacherUser(
                    user_id=t["id"],
                    name=t["name"],
                    speciality=t.get("speciality", "")
                )
                    self.teachers.append(teacher)
                # TODO: Do the same for teachers (creating TeacherUser objects).

                for c in data.get("courses", []):
                    course = Course(
                    course_id=c["id"],
                    name=c["name"],
                    instrument=c["instrument"],
                    teacher_id=c["teacher_id"],
                    enrolled_student_ids=c.get("enrolled_student_ids", []),
                    lessons=c.get("lessons", [])
                )
                    self.courses.append(course)
                # TODO: Do the same for courses (creating Course objects).

                raw_att = data.get("attendance", [])
                self.attendance = []
                for a in raw_att:
                    if isinstance(a, dict):
                        # create Attendance object and copy fields
                        att = Attendance(
                            a.get("id", 0),
                            a.get("lesson_id"),
                            a.get("status", "Present")
                        )
                        att.student_id = a.get("student_id")
                        att.course_id = a.get("course_id")
                        att.timestamp = a.get("timestamp")
                        self.attendance.append(att)
                    else:
                        self.attendance.append(a)

                self.finance_log = data.get("finance_log", [])

        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""

        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [
                {
                **c.__dict__,
                "lessons": [l if isinstance(l, dict) else l.__dict__ for l in c.lessons]
                } for c in self.courses
            ],
            "attendance": [
            a.__dict__ if hasattr(a, "__dict__") else a for a in self.attendance
            ],
            "finance_log": self.finance_log  
        }

        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        # The logic here remains the same.
        # TODO: Create a 'data_to_save' dictionary.
        # Convert self.students, self.teachers, and self.courses into lists of dictionaries.
        # Write the result to the JSON file.
        print(" Data saved successfully.")

    def record_payment(self, student_id, amount, method):
        """Adds a payment record to the finance log."""
        student_exists = any(s.id == student_id for s in self.students)
        if not student_exists:
            print(f"Error: No student found with ID {student_id}")
            logging.error(f"Failed payment: student ID {student_id} not found.")
            return

        payment_record = {
            "student_id": student_id,
            "amount": amount,
            "method": method,
            "timestamp": datetime.datetime.now().isoformat()
        }

        self.finance_log.append(payment_record)
        self._save_data()
        print(f"Payment of RM{amount} for student {student_id} recorded via {method}.")
        logging.info(f"Payment recorded: RM{amount} by student {student_id} via {method}.")

    def cancel_lesson(self, lesson_id, reason):
        """Cancels a lesson and logs the event."""
        found = False
        for course in self.courses:
            for lesson in course.lessons:
                if lesson["lesson_id"] == lesson_id:
                    course.lessons.remove(lesson)
                    found = True
                    break
            if found:
                break

        self._save_data()

        if found:
            print(f"Lesson {lesson_id} cancelled: {reason}")
            logging.warning(f"Lesson {lesson_id} cancelled. Reason: {reason}")
        else:
            print(f"Lesson {lesson_id} not found.")
            logging.error(f"Failed to cancel: lesson {lesson_id} not found.")

    def get_payment_history(self, student_id):
        """Returns a list of all payments for a given student."""
        return [p for p in self.finance_log if p['student_id'] == student_id]

    def export_report(self, kind, out_path):
        """Exports a log to a CSV file."""
        print(f"Exporting {kind} report to {out_path}...")

        if kind == "finance":
            data_to_export = self.finance_log
            headers = ["student_id", "amount", "method", "timestamp"]
        elif kind == "attendance":
            data_to_export = getattr(self, "attendance", [])
            headers = ["student_id", "course_id", "timestamp"]
        else:
            print("Error: Unknown report type.")
            return

        with open(out_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data_to_export)

        print(f"{kind.capitalize()} report exported successfully to {out_path}.")

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

    def check_in(self, student_id, course_id, lesson_id):
        course = self.find_course_by_id(course_id)
        if not course or student_id not in course.enrolled_student_ids:
            return False
        
        # Check if lesson exists
        lesson = next((l for l in course.lessons if l["lesson_id"] == lesson_id), None)
        if not lesson:
            return False
        
        for a in self.attendance:
            if getattr(a, "student_id", None) == student_id and getattr(a, "lesson_id", None) == lesson_id:
                return True

        new_id = max((getattr(a, "id", 0) for a in self.attendance), default=0) + 1
        new_att = Attendance(new_id, lesson_id, "Present")
        new_att.student_id = student_id
        new_att.course_id = course_id
        new_att.timestamp = datetime.datetime.now().isoformat()

        self.attendance.append(new_att)
        self._save_data()
        return True


    def _attendance_on_day(self, student_id, course_id, day_name):
        """
        Check if a student has an attendance entry for a course on a given day.
        day_name should be like "Monday", "Tuesday", etc.
        """ 
        for a in self.attendance:
                a_student = a.get("student_id") if isinstance(a, dict) else getattr(a, "student_id", None)
                a_course  = a.get("course_id")  if isinstance(a, dict) else getattr(a, "course_id", None)
                if a_student == student_id and a_course == course_id:
                    return "Yes"
        return "No"

    def get_roster_for_day(self, day_name):
            roster = []
            for c in self.courses:
                teacher = self.find_teacher_by_id(c.teacher_id)
                for lesson in c.lessons:
                    if lesson["day"].strip().lower() != day_name.lower():
                        continue
                    if not c.enrolled_student_ids:
                        roster.append({
                            "Course": c.name,
                            "Instrument": c.instrument,
                            "Time": lesson["start_time"],
                            "Room": lesson.get("room", ""),
                            "Teacher": teacher.name if teacher else "",
                            "Student": "No students enrolled",
                            "CheckedIn": ""
                        })
                    else:
                        for sid in c.enrolled_student_ids:
                            student = self.find_student_by_id(sid)
                            roster.append({
                                "Course": c.name,
                                "Instrument": c.instrument,
                                "Time": lesson["start_time"],
                                "Room": lesson.get("room", ""),
                                "Teacher": teacher.name if teacher else "",
                                "Student": student.name if student else f"ID {sid}",
                                "CheckedIn": self._attendance_on_day(sid, c.id, day_name)
                            })
            return roster
            
    def add_lesson_to_course(self, course_id, day, start_time, room=""):
        course = self.find_course_by_id(course_id)
        if not course:
            return None
        lesson_id = self.next_lesson_id
        self.next_lesson_id += 1
        course.lessons.append({
            "lesson_id": lesson_id,
            "course_name": course.name,
            "day": day,
            "start_time": start_time,
            "room": room
        })
        self._save_data()
        return lesson_id
