Overview

This project acts as a simplified backend for an educational management system, combining:
- **Data management:** JSON-based persistent storage
- **Business logic:** Course registration, payments, and attendance
- **Utilities:** Logging and automated backups
- **Testing:** Pytest verification of system logic
- **Frontend :** Streamlit-based GUI

#app/user.py
- user_id → Unique integer identifier.
- name → User’s display name.
- Acts as a parent class to StudentUser and TeacherUser.

#app/student.py
- **Class: StudentUser**
    -Inherits from User and adds enrollment tracking.
- Inherits base id and name.
- Maintains a list of course IDs the student is enrolled in.
- Uses to_dict() for JSON serialization

- **Class: Attendance**
    - Stores attendance data.
- Each attendance record links to a specific lesson_id.
- status can be "Present" or "Absent".

- **Class: Lesson**
    - Represents one scheduled class session.
- Each lesson belongs to a Course.
- Optional room supports flexible scheduling.

#app/teacher.py
- **Class: TeacherUser**
    - Inherits from User, adds speciality.
- speciality field identifies the teacher’s instrument or subject area.

- **Class: Course**
    - Represents a course linked to one teacher.
- Each Course can have multiple Lesson dictionaries and enrolled students.
- Method to_dict() converts it for JSON export.

- **Class: Lesson**
    - Alternative representation for lesson creation and export.

#app/admin_utils.py
- **Function: init_logger()**
    - Configures centralized logging to file.
    - Includes timestamp, log level, and message.
    - Appends rather than overwrites the existing log file.

- **Function: backup_data()**
    - Ensures backup directory exists.
    - Creates timestamped backup file.
    - Logs all actions (success or failure).
    - Returns True or False depending on outcome.

#app/schedule.py
- **Class: ScheduleManager**
    - Central class that integrates all other models.
    - __init__(): Initializes all major data lists and loads saved data.
    - _load_data(): Reads data from JSON into objects.
        - Iterates through JSON keys: "students", "teachers", "courses" "attendance", "finance_log".
        - Constructs StudentUser, TeacherUser, and Course instances.
    - _save_data(): Writes the current state back to JSON.
        - Converts all objects into dictionaries.
        - Serializes to msms.json with indent=4 for readability.
        - Called after every modification (e.g. payments, new lessons).
    - record_payment(): Logs a payment and updates finance_log.
        - Validates student ID.
        - Records payment with timestamp.
        - Appends record and saves data.
        - Logs success or failure to file.
    - cancel_lesson(): Removes a scheduled lesson by lesson_id.
        - Searches every course’s lessons list.
        - Logs cancellation reason or error.
    - get_payment_history(): Retrieves all finance records for one student ID.
    - export_report(): Exports attendance or finance data to CSV format.
        - Determines headers based on report type.
        - Uses csv.DictWriter to generate report.
        - Supports finance and attendance.
    - find_student() / find_student_by_id() / find_course_by_id() / find_teacher_by_id()
    : Utility search methods for locating records by name or ID.
    - register_new_student(): Registers a student and auto-enrolls them in a matching course.
        - Generates a new unique ID.
        - Ensures both course and student lists stay synchronized.
        - Saves changes immediately.
    - check_in(): Marks attendance for a given student–lesson pair.
        - Ensures lesson and student exist.
        - Prevents duplicate check-ins.
        - Creates a new Attendance object when valid.
    - _attendance_on_day(): verifies attendance for a specific date.
    - get_roster_for_day(): compiles a daily schedule
    - add_lesson_to_course(): Appends a new lesson dictionary into the selected course.
        - Auto-increments lesson_id.
        - Saves after each update.

#gui/student_pages.py
- **Function: show_student_management_page(manager)**
    - Renders the Student Management interface in Streamlit.
    - Provides three main blocks:
        1. Find a Student
            - Uses a text input for name search.
            - Calls manager.find_student() and displays matching students.
            - Shows enrolled instruments for each found student.
        2. Register Student
            - Streamlit form to register a new student.
            - Lists available instruments from manager.courses.
            - Calls manager.register_new_student(name, instrument) to create and store a new record.
            - Displays success, warning, or error messages based on result.
        3. Remove Student
            - Form to remove a student by ID.
            - On submission, removes the student from manager.students and all relevant courses’ enrollment lists.
            - Calls manager._save_data() to persist changes.

#gui/teacher_management (inside main_dashboard.py)
- **Function: show_teacher_management_page(manager)**
    - Manages teacher registration, removal, and search.
    - Key sections:
        1. Find a Teacher
            - Text input for name search.
            - Filters manager.teachers and displays matching entries.
        2. Register Teacher
            - Streamlit form for new teacher registration.
            - Generates a unique ID automatically.
            - Imports and creates TeacherUser instance, appends to manager.teachers, saves data.
            - Uses Streamlit’s st.balloons() for visual feedback.
        3. Remove Teacher
            - Dropdown to choose teacher to delete.
            - Removes from manager.teachers and saves changes.
        4. List All Teachers
            - Displays all registered teachers in a readable format.

#gui/course_management (inside main_dashboard.py)
- **Function: show_course_management_page(manager)**
    - Controls course creation, lesson management, enrollment, and teacher assignment.
    - Core actions via radio buttons:
        1. Create Course
            - Form collects course name, instrument, and optional teacher.
            - Creates Course object, appends to manager.courses, and saves.
            - Temporarily stores new course in session for immediate lesson creation.
        2. Add Lesson (after course creation)
            - Form to specify day, start time, and room.
            - Automatically assigns a unique lesson ID.
            - Saves lesson data under the selected course.
        3. Update Lesson
            - Select course → view or update its lesson schedule.
            - Allows modification of day/time/room.
            - Updates and saves to disk.
        4. Enroll Student in Course
            - Links a student to a selected course.
            - Updates both course.enrolled_student_ids and student.enrolled_course_ids.
            - Ensures bidirectional consistency.
        5. Assign Teacher to Course
            - Matches teachers based on instrument speciality.
            - Updates course.teacher_id.
        6. Remove Course
            - Removes a selected course and persists the change.
        7. All Courses Section
            - Displays all course details (teacher, instrument, students) in a Streamlit table.

#gui/roster_pages.py
- **Function: show_roster_page(manager)**
    - Displays and manages the Daily Roster view.
    - Main parts:
        1. Roster Overview
            - Dropdown to select a weekday.
            - Calls manager.get_roster_for_day(day) to get scheduled lessons.
            - Displays in a DataFrame with columns: Course, Instrument, Time, Teacher, Student, Checked-in status.
        2. Student Check-in
            - Form with dropdowns for student, course, and lesson.
            - Validates enrollment and calls manager.check_in(student_id, course_id, lesson_id).
            - Shows success/failure messages dynamically.

#gui/finance_pages.py
- **Function: show_finance_page(manager)**
    - Handles all financial record-keeping through Streamlit UI.
    - Two primary components:
        1. Record New Payment
            - Selectbox to choose a student.
            - Numeric and text input for amount and method.
            - Calls manager.record_payment(student_id, amount, method).
            - Displays confirmation message on success.
        2. View Payment History
            - Selectbox to choose student.
            - Calls manager.get_payment_history(student_id).
            - Converts returned list of dicts to a Pandas DataFrame and displays it.

#gui/attendance_reports_page (inside main_dashboard.py)
- **Function: show_attendance_reports_page(manager)**
    - Provides tools to record and review student attendance.
    - Core sections:
        1. Mark Attendance
            - Select student and available lesson (based on enrollment).
            - Choose status: Present / Absent / Late.
            - Updates or creates an Attendance record.
            - Saves updates via manager._save_data().
        2. Attendance Records Table
            - Compiles attendance logs with course, teacher, date, time, and room info.
            - Displays as an interactive DataFrame for easy review.

#gui/main_dashboard.py
- **Function: launch()**
    - Serves as the main entry point for the entire Streamlit application.
    - Steps:
        1. Sets page config and initializes logging with init_logger().
        2. Performs backup with backup_data().
        3. Creates a single ScheduleManager instance and stores it in st.session_state.
        4. Displays sidebar navigation using st.sidebar.radio():
            - Student Management, Course Management, Teacher Management, Daily Roster, Payments, Attendance Reports
        5. Dynamically calls the appropriate rendering function based on user selection.
        6. Includes a “Backup Now” button to trigger manual backups.

#tests/test_schedule_manager.py 
    - This file contains six high-quality pytest tests covering all major functions of ScheduleManager.
Test 1: test_create_course_by_appending
        - Ensures a new Course object can be appended and saved successfully.
        - Validates correct attributes (name, instrument).

Test 2: test_record_payment_and_history
        - Adds a student, records a payment, and retrieves payment history.
        - Asserts data integrity and proper ISO timestamp formatting.

Test 3: test_get_payment_history_no_results
        - Verifies that the method safely returns an empty list when no records exist.

Test 4: test_add_lesson_to_course
        - Adds a course, then a lesson.
        - Confirms that the new lesson is properly stored under the correct course.

Test 5: test_cancel_lesson_removes_from_course
        - Adds a lesson to a course, then cancels it.
        - Asserts that the lesson is removed from the course’s lessons list.

Test 6: test_check_in_success_and_failure
        - Tests both a successful and failed check-in.
        - Ensures correct attendance object creation for valid enrollments.
        - Returns False for invalid students.

#main.py
- init_logger()
    - Initializes application logging to record system events (startups, data saves, user actions).
    - This ensures maintainability and troubleshooting capability.

- backup_data()
    - Creates a backup of msms.json to avoid accidental data loss before the session starts.

- launch()
    - Starts the Streamlit GUI (from gui/main_dashboard.py), allowing user interaction.