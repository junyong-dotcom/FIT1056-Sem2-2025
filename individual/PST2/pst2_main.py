import json
import datetime

DATA_FILE = "msms.json"
app_data = {} # This global dictionary will hold ALL our data.

# --- Core Persistence Engine ---
def load_data(path=DATA_FILE):
    """Loads all application data from a JSON file."""
    global app_data
    try:
        with open(path, 'r') as f:
            # TODO: Use json.load(f) to load the file's content into the global 'app_data' variable.
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        # TODO: If the file doesn't exist, initialize 'app_data' with a default dictionary.
        # It should have keys like: "students", "teachers", "attendance", "next_student_id", "next_teacher_id".
        # The lists should be empty and the IDs should start at 1.
        app_data = {
            "students": [],
            "teachers": [],
            "courses": {},
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1,
            "next_course_id": 1
        }

def save_data(path=DATA_FILE):
    """Saves all application data to a JSON file."""
    # TODO: Open the file at 'path' in write mode ('w').
    # Use json.dump() to write the global 'app_data' dictionary to the file.
    # Use the 'indent=4' argument in json.dump() to make the file readable.
    with open(path, 'w') as f:
        json.dump(app_data, f, indent=4)
    print("Data saved successfully.")
                 
#Fragment 2.2
def add_teacher(name, speciality):  
    """Adds a teacher dictionary to the data store."""
    # TODO: Get the next teacher ID from app_data['next_teacher_id'].
    teacher_id = app_data['next_teacher_id']
    # TODO: Create a new teacher dictionary with 'id', 'name', and 'speciality' keys.
    new_teacher = {"id": teacher_id, "name": name, "speciality": speciality}
    # TODO: Append the new dictionary to the app_data['teachers'] list.
    app_data['teachers'].append(new_teacher)
    # TODO: Increment the 'next_teacher_id' in app_data.
    app_data['next_teacher_id'] += 1
    print(f"Core: Teacher '{name}' added.")

def add_student(name, enrolled_in=""):
    """Adds a student dictionary to the data store."""
    student_id = app_data['next_student_id']
    new_student = {
        "id": student_id,
        "name": name,
        "enrolled_in": [c.strip() for c in enrolled_in.split(",")] if enrolled_in else []
    }
    app_data['students'].append(new_student)
    app_data['next_student_id'] += 1
    print(f"Student '{name}' (ID: {student_id}) added successfully into course {enrolled_in}.")
    return student_id  

def add_course(course_name):
    """Adds a new course to the system"""
    if not course_name.strip():
        print("Course name cannot be empty.")
        return None
    
    if 'courses' not in app_data:
        app_data['courses'] = {}
    if 'next_course_id' not in app_data:
        app_data['next_course_id'] = 1

    course_id = app_data['next_course_id']
    app_data['courses'][course_id] = course_name.strip()
    app_data['next_course_id'] += 1
    print(f"New course [{course_name} with ID {course_id} has been successfully added.]")
    return course_id

def update_teacher(teacher_id, **fields):
    """Finds a teacher by ID and updates their data with provided fields."""
    # TODO: Loop through the app_data['teachers'] list.
    for teacher in app_data['teachers']:
        # TODO: If a teacher's 'id' matches teacher_id:
        if teacher['id'] == teacher_id:
            # Use the .update() method on the teacher dictionary to apply the 'fields'.
            teacher.update(fields)
            print(f"Teacher {teacher_id} updated.") 
            return
    print(f"Error: Teacher with ID {teacher_id} not found.")

def remove_teacher(teacher_id):
    """Removes a teacher from the date store."""
    app_data['teachers'] = [t for t in app_data['teachers'] if t['id'] != teacher_id]
    print(f"Teacher {teacher_id} is removed.")

def update_student(student_id, **fields):
    """Finds a student by ID and updates their data with provided fields."""
    for student in app_data['students']:
        if student['id'] == student_id:
            student.update(fields)
            print(f"Student {student_id} updated.")
            return
    print(f"Error: Student with ID {student_id} not found.")

def remove_student(student_id):
    """Removes a student from the data store."""
    app_data['students'] = [s for s in app_data['students'] if s['id'] != student_id]
    print(f"Student {student_id} is removed.")

#Fragment 2.3
def check_in(student_id, course_id, timestamp=None):
    """Records a student's attendance for a course."""
    
    course_name = app_data['courses'].get(course_id)

# I want to find student name with student ID entered"
    student = None
    for s in app_data['students']:
        if s['id'] == student_id:
            student = s
            break
    if not student:
        print(f"Error: Student ID {student_id} not found.")
        return
    if not course_name:
        print(f"Error: Course ID {course_id} not found.")
        return
    
    if timestamp is None:
        # TODO: Get the current time as a string using datetime.datetime.now().isoformat()
        timestamp = datetime.datetime.now().isoformat()
    
    # TODO: Create a check-in record dictionary.
    # It should contain 'student_id', 'course_id', and 'timestamp'.
    check_in_record = {
        "student_id": student_id,
        "student_name" : student['name'],
        "course_id": course_id,
        "course_name":  course_name,
        "timestamp": timestamp
    }
    # TODO: Append this new record to the app_data['attendance'] list.
    app_data['attendance'].append(check_in_record)
    print(f"Receptionist: Student {student['name']} with an ID {student_id} checked into {course_name} (ID: {course_id}).")

def print_student_card(student_id):
    """Creates a text file badge for a student."""
    # TODO: Find the student dictionary in app_data['students'].
    student_to_print = None
    for s in app_data['students']:
        if s['id'] == student_id:
            student_to_print = s
            break
    
    if student_to_print:
        # TODO: Create a filename, e.g., f"{student_id}_card.txt".
        filename = f"{student_id}_card.txt"
        # TODO: Open the file in write mode ('w').
        card_content = (
            "========================\n"
            f"  MUSIC SCHOOL ID BADGE\n"
            "========================\n"
            f"ID: {student_to_print['id']}\n"
            f"Name: {student_to_print['name']}\n"
            f"Enrolled In: {', '.join(student_to_print.get('enrolled_in', []))}\n"
        )

        with open(filename, 'w') as f:
            # Write the student's details to the file in a nice format.
            f.write(card_content)

        print("\n Saved this card to file:")
        print(card_content)
        print(f"Printed student card to {filename}.")

    else:
        print(f"Error: Could not print card, student {student_id} not found.")

# Fragment 2.4
def main():
    """Main function to run the MSMS application."""
    load_data() # Load all data from file at startup.

    while True:
        print("\n===== MSMS v2 (Persistent) =====")
        print("1. Check-in Student")
        print("2. Add Student")
        print("3. Add Teacher")
        print("4. Print Student Card")
        print("5. Update Teacher Info")
        print("6. Update Student Info")
        print("7. Remove Student")
        print("8. Remove Teacher")
        print("9. View Attendance Record")
        print("10. Add course(Accessible to staff only)")
        print("q. Quit and Save")
        
        choice = input("Enter your choice: ")
        
        made_change = False # A flag to track if we need to save
        if choice == '1':
            """Check-in Student"""
            student_id = int(input("Enter student ID: "))
            course_id = int(input("Enter course ID: "))
            check_in(student_id, course_id)
            # TODO: Get student_id and course_id from user, then call check_in().
            made_change = True

        elif choice == '2':
            """Add new Student"""
            name = input("Enter Student name: ")
            enrolled_in = input("Enter course enrolled in: ")
            add_student(name, enrolled_in)
            made_change = True

        elif choice == '3':
            """Add new Teacher"""
            name = input("Enter teacher's name: ")
            speciality = input("Enter teacher's speciality: ")
            add_teacher(name, speciality)
            made_change = True

        elif choice == '4':
            """Print Student card"""
            student_id = int(input("Enter student ID: "))
            print_student_card(student_id)
            # TODO: Get student_id, then call print_student_card().
            pass # No change made, so no save needed

        elif choice == '5':
            """Update Teacher info"""
            teacher_id = int(input("Enter teacher ID: "))
            name = input("Enter new teacher's name: ")
            teacher_speciality = input("Enter new teacher's speciality: ")

            fields = {}
            if name:
                fields['name'] = name
            if teacher_speciality:
                fields['speciality'] = teacher_speciality
            
            if fields:
                update_teacher(teacher_id, **fields)    
                made_change = True
            else:
                print("No changes made.")

        elif choice == '6':
            """Update Student info"""
            student_id  = int(input("Enter Student ID: "))
            name = input("Enter Student name: ")
            enrolled_in = input("Enter New Course to enrolled in: ")

            fields = {}
            if name:
                fields['name'] = name
            if enrolled_in:
                fields['enrolled_in'] = [c.strip() for c in enrolled_in.split(",")]

            if fields:
                update_student(student_id, **fields)
                made_change = True
            else:
                print("No changes made.")

        
        elif choice == '7':
            """Remove Student"""
            student_id = int(input("Enter student ID to remove: "))
            remove_student(student_id)
            # TODO: Get student_id, then call remove_student().
            made_change = True

        elif choice == '8':
            """Remove Teacher"""
            teacher_id = int(input("Enter teacher ID to remove: "))
            remove_teacher(teacher_id)
            made_change = True

        elif choice == '9':
            """Attendance Record"""
            print("\n ===Attendance Records===")
            if app_data['attendance']:
                for record in app_data['attendance']:
                    print(
                f"{record['timestamp']}: "
                f"{record.get('student_name')} (ID: {record['student_id']}) "
                f"attended {record.get('course_name')}"
            )
            else:
                print("No Attendance Recorded")

        elif choice == '10':
            """Add new course to this music school"""
            course_name = input("Enter course name: ").strip()
            if add_course(course_name) is not None:
                made_change = True

        elif choice.lower() == 'q':
            print("Saving final changes and exiting.")
            break

        else:
            print("Invalid choice.")
            
        if made_change:
            save_data() # Save the data immediately after any change.

    save_data() # One final save on exit.


# --- Program Start ---
if __name__ == "__main__":
    main()

# Course ID:
# 1. Piano
# 2. Guitar
# 3. Advanced Piano
# 4. Violin

#json list dict
#why dump
#iso TimeoutError
#validation constring (duplication)