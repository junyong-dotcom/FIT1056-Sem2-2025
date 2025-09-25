1. app/schedule.py
ScheduleManager class
    This is the main “brain” of the application. It handles all data operations and business logic for students, teachers, courses, lessons, and attendance.

__init__ method
    Initializes lists for students, teachers, courses, and attendance.
    Sets next_lesson_id to 1.
    Calls _load_data() to populate the lists from a JSON file (data/msms.json).

_load_data method
    Reads the JSON file and converts each dictionary into corresponding objects:
    StudentUser for students
    TeacherUser for teachers
    Course and its Lesson objects for courses
    Attendance objects for attendance records
    If the file doesn’t exist, it prints a message and starts with empty lists.

_save_data method
    Converts all objects back into dictionaries and saves them to the JSON file.
    Ensures all data persists between sessions.

Find methods (find_student, find_student_by_id, find_course_by_id, find_teacher_by_id)
    Search for a student/teacher/course by name or ID.
    Return the object if found, or None if not.

register_new_student method
    Registers a new student for a given instrument.
    Assigns the student to the first matching course for that instrument.
    Updates both the student and course objects.

Saves data using _save_data.

check_in method
    Records attendance for a student in a specific course.
    Appends a timestamped entry to the attendance list.
    Saves the updated data.

_attendance_on_day helper method
    Checks if a student has attendance for a given course on a specified day.

get_roster_for_day method
    Builds a list of all students scheduled on a specific day.
    Includes course, instrument, time, room, teacher, student, and attendance status.

2. app/student.py
StudentUser class
    Inherits from User.
    Adds enrolled_course_ids to track which courses a student is in.
    to_dict() converts the object to a dictionary for saving.

Attendance class
    Represents attendance for a lesson with id, lesson_id, and status.

Lesson class
    Represents a lesson in a course with day, start time, and optional room.
    Implements __str__ to display the lesson nicely.

3. app/teacher.py
TeacherUser class
    Inherits from User.
    Adds a speciality attribute (e.g., piano, violin).
    to_dict() converts it to a dictionary.

Course class
    Represents a course taught by a teacher.
    Attributes: id, name, instrument, teacher_id.
    Holds lists: enrolled_student_ids and lessons.
    to_dict() converts the object to a dictionary for saving.

4. app/user.py
User class
    Base class for all users (students, teachers).
    Has id and name.

5. gui/main_dashboard.py
This file sets up the Streamlit GUI.

show_teacher_management_page(manager)
    Search for teachers by name.
    Register new teachers.
    Remove existing teachers.
    List all teachers.

show_course_management_page(manager)
    Create new courses and assign a teacher.
    Enroll students in courses.
    List all courses with enrolled students.

show_attendance_reports_page(manager)
    Mark attendance for students for a specific lesson.
    Show all attendance records with course, student, teacher, date, time, room, and status.

launch() function
    Initializes the Streamlit GUI.
    Creates a ScheduleManager instance and stores it in st.session_state.
    Provides a sidebar menu to navigate between pages: Student, Teacher, Course, Attendance, Payments.

6. gui/roster_pages.py
show_roster_page(manager)
    Displays a daily roster with course, student, teacher, and attendance info.
    Allows students to check in for lessons.

7. gui/student_pages.py
show_student_management_page(manager)
    Search for students by name.
    Register new students for an instrument.
    Remove students by ID.
    Displays enrolled courses for students.

8. main.py
    Simply calls launch() to start the Streamlit GUI.