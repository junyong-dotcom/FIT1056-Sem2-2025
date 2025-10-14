import json
import csv
import datetime
from app.student import StudentUser
# Corrected Import: TeacherUser and Course now come from the same file.
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
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
                    id=s["id"],
                    name=s["name"],
                    enrolled_course_ids=s.get("enrolled_course_ids", [])
                )
                self.students.append(student)
                # TODO: For each dictionary in data['students'], create a StudentUser object and append to self.students.

                for t in data.get("teachers", []):
                    teacher = TeacherUser(
                    id=t["id"],
                    name=t["name"],
                    speciality=t.get("speciality", "")
                )
                self.teachers.append(teacher)
                # TODO: Do the same for teachers (creating TeacherUser objects).

                for c in data.get("courses", []):
                    course = Course(
                    id=c["id"],
                    name=c["name"],
                    instrument=c["instrument"],
                    teacher_id=c["teacher_id"],
                    enrolled_student_ids=c.get("enrolled_student_ids", []),
                    lessons=c.get("lessons", [])
                )
                self.courses.append(course)
                # TODO: Do the same for courses (creating Course objects).

                self.attendance = data.get("attendance", [])
                self.finance_log = data.get("finance_log", [])

        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""

        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
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
            return

        payment_record = {
            "student_id": student_id,
            "amount": amount,
            "method": method,
            "timestamp": datetime.datetime.now().isoformat()
        }

        self.finance_log.append(payment_record)
        self._save_data()
        print(f"💰 Payment of RM{amount} for student {student_id} recorded via {method}.")

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