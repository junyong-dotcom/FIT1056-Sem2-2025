# main.py - The View Layer
from app.schedule import ScheduleManager

def front_desk_daily_roster(manager, day):
    """Displays a simple list of lessons on a given day."""
    print(f"\n--- Daily Roster for {day} ---")
    lessons = manager.get_lessons_by_day(day)

    if not lessons:
        print("No lessons scheduled.")
        return

    for lesson in lessons:
        teacher = manager.find_teacher_by_id(lesson["teacher_id"])
        teacher_name = teacher.name if teacher else "Unknown"
        print(f"{lesson['course_id']} - {lesson['course_name']} | {teacher_name} | "
              f"{lesson['day']} {lesson['time']} @ {lesson['room']}")

def switch_course(manager, user_id, from_course_id, to_course_id):
        # TODO: Implement the logic to switch a student by calling methods on the manager.
        """Switch a student from one course to another."""
        success = manager.switch_student_course(user_id, from_course_id, to_course_id)
        if success:
            print(f"Student {user_id} switched from course {from_course_id} to {to_course_id}.")
        else:
            print("Error: Could not switch courses. Check IDs and try again.")

def add_student_view(manager):
    name = input("Enter student name: ")
    student = manager.add_student(name)
    print(f"Student added: {student.name} (ID: {student.id})")

def add_teacher_view(manager):
    name = input("Enter teacher name: ")
    speciality = input("Enter teacher speciality: ")
    teacher = manager.add_teacher(name, speciality)
    print(f"Teacher added: {teacher.name} (ID: {teacher.id}) - {teacher.speciality}")

def add_course_view(manager):
    name = input("Enter course name: ")
    instrument = input("Enter instrument: ")
    teacher_id = int(input("Enter teacher ID for the course: "))
    course = manager.add_course(name, instrument, teacher_id)
    print(f"Course added: {course.name} (ID: {course.id})")

def schedule_lesson_view(manager):
    course_id = int(input("Enter course ID to schedule lesson for: "))
    day = input("Enter day (e.g., Monday): ")
    start_time = input("Enter start time (HH:MM): ")
    room = input("Enter room (or leave blank for N/A): ") or "N/A"
    if manager.schedule_lesson(course_id, day, start_time, room):
        print("Lesson scheduled successfully.")
    else:
        print("Error: Invalid course ID.")

def view_student_courses_view(manager):
    student_id = int(input("Enter student ID: "))
    courses = manager.get_student_courses(student_id)
    if not courses:
        print("No courses found for this student.")
        return
    print(f"Courses for student {student_id}:")
    for course in courses:
        if course:
            print(f"- {course.id}: {course.name} ({course.instrument})")

def view_teacher_courses_view(manager):
    teacher_id = int(input("Enter teacher ID: "))
    courses = manager.get_teacher_courses(teacher_id)
    if not courses:
        print("No courses found for this teacher.")
        return
    print(f"Courses for teacher {teacher_id}:")
    for course in courses:
        print(f"- {course.id}: {course.name} ({course.instrument})")

def view_attendance_report_view(manager):
    course_id_input = input("Enter course ID (leave blank for all): ")
    student_id_input = input("Enter student ID (leave blank for all): ")

    course_id = int(course_id_input) if course_id_input else None
    student_id = int(student_id_input) if student_id_input else None

    report = manager.attendance_report(course_id, student_id)
    if not report:
        print("No attendance records found.")
        return

    print("Attendance Records:")
    for record in report:
        print(f"- Student {record['student_id']} | Course {record['course_id']} | Time {record['timestamp']}")

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager()  # Create ONE instance of the application brain.
    
    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("1. View Daily Roster")
        print("2. Switch Course")
        print("3. Add Student")
        print("4. Add Teacher")
        print("5. Add Course")
        print("6. Schedule Lesson")
        print("7. View Student Courses")
        print("8. View Teacher Courses")
        print("9. View Attendance Report")
        print("q. Quit")

        choice = input("Enter choice: ")
        
        if choice == '1':
            day = input("Enter day (e.g., Monday): ")
            front_desk_daily_roster(manager, day)
        elif choice == "2":
            student_id = int(input("Enter student ID: "))
            from_course_id = int(input("Enter course ID to leave: "))
            to_course_id = int(input("Enter new course ID: "))
            switch_course(manager, student_id, from_course_id, to_course_id)
        elif choice == "3":
            add_student_view(manager)
        elif choice == "4":
            add_teacher_view(manager)
        elif choice == "5":
            add_course_view(manager)
        elif choice == "6":
            schedule_lesson_view(manager)
        elif choice == "7":
            view_student_courses_view(manager)
        elif choice == "8":
            view_teacher_courses_view(manager)
        elif choice == "9":
            view_attendance_report_view(manager)
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()