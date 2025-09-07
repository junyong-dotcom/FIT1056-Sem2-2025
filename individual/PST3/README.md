1. user.py
    - Base class for all users (students or teachers). User holds id and name. Acts as a parent class for StudentUser and TeacherUser.

2. student.py
    - Represents a student. Inherits from User using super(). Adds enrolled_course_ids to track the courses the student is enrolled in.
    - Defaults to an empty list if no courses are provided.

3. teacher.py
    - Represents teachers and courses. 
    - class TeacherUser: Inherits from User. Adds speciality to store the teacher’s area of expertise.
    - class Course: Stores course info: id, name, instrument, and assigned teacher. Tracks students enrolled and lessons scheduled.

4. schedule.py
    - Initialization and Data Loading
    - def __init__(self, data_path="data/msms.json"):
        - Loads saved data or starts clean.
        - Sets counters for new IDs.
    - def _save_data(self):
        - Converts objects to dictionaries and saves to JSON.
        - Ensures attendance, students, teachers, and courses persist.
    - def check_in(self, student_id, course_id):
        - Records attendance with timestamp.
        - Saves immediately to JSON.
    - def find_student_by_id(self, student_id):
      def find_course_by_id(self, course_id):
      def find_teacher_by_id(self, teacher_id):
        - Find helpers
        - Search for objects quickly by ID.
    - def add_student(self, name): 
      def update_student(self, student_id, ...):
      def remove_student(self, student_id): 
        - Add, update, and remove students/teachers.
        - Updates enrolled courses or assigned courses automatically.
    - def add_course(self, name, instrument, teacher_id): 
      def schedule_lesson(self, course_id, day, start_time, room="N/A"): 
      def get_lessons_by_day(self, day): 
      def get_lessons_by_room(self, room): 
        - Add courses, schedule lessons, or retrieve lessons by day/room.
    - def switch_student_course(self, student_id, from_course_id, to_course_id): 
        - Moves a student from one course to another, updating both student and course records.
    - def attendance_report(self, course_id=None, student_id=None): 
        - Returns attendance data.

5. pst3_main.py
    - user interface.
    - Front Desk / Daily Roster
        - def front_desk_daily_roster(manager, day): 
            -Shows lessons scheduled for a specific day.
            
    - Views
        - Functions like add_student_view, add_teacher_view, view_student_courses_view provide input prompts and display data.
        - Call ScheduleManager methods to perform actions.

    - Attendance Interface
        - def take_attendance(manager):
            - Iterates through students in a course.
            - Asks the user if each student is present.
            - Calls check_in to record attendance.

    - Main Menu
        - Displays options.
        - Calls the corresponding view function depending on user input.