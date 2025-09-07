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

def main():
        """Main function to run the MSMS application."""
        manager = ScheduleManager() # Create ONE instance of the application brain.
        
        while True:
            print("\n===== MSMS v3 (Object-Oriented) =====")
            print("1. View Daily Roster")
            print("2. Switch Course")
            print("q. Quit")

            # TODO: Create a menu for the new PST3 functions.
            # Get user input and call the appropriate view function, passing 'manager' to it.
            choice = input("Enter choice: ")
            if choice == '1':
                day = input("Enter day (e.g., Monday): ")
                front_desk_daily_roster(manager, day)

            elif choice == "2":
                student_id = int(input("Enter student ID: "))
                from_course_id = int(input("Enter course ID to leave: "))
                to_course_id = int(input("Enter new course ID: "))
                switch_course(manager, student_id, from_course_id, to_course_id)

            elif choice.lower() == 'q':
                break

            else:
                print("Invalid choice. Try again.")

            
if __name__ == "__main__":
    main()