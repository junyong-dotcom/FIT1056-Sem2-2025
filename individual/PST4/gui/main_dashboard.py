# gui/main_dashboard.py
import streamlit as st
from app.schedule import ScheduleManager
from app.student import Attendance
from app.teacher import Course
from gui.student_pages import show_student_management_page
from gui.roster_pages import show_roster_page

def show_teacher_management_page(manager):
    st.header("Teacher Management")
     # --- Search Section ---
    st.subheader("Find a Teacher")
    search_name = st.text_input("Enter teacher name")
    if st.button("Search Teacher"):
        teachers = [t for t in manager.teachers if search_name.lower() in t.name.lower()]
        if teachers:
            for t in teachers:
                st.success(f"Found: {t.name}, Speciality: {t.speciality}")
        else:
            st.warning("Teacher not found.")

    st.subheader("Manage Teachers")
    action = st.radio("Choose action:", ["Register Teacher", "Remove Teacher"])

    if action == "Register Teacher":
        with st.form("teacher_registration_form"):
            reg_name = st.text_input("Teacher Name")
            reg_speciality = st.text_input("Speciality (e.g., Piano, Guitar, Violin)")
            submitted = st.form_submit_button("Register Teacher")
            
            if submitted:
                if reg_name and reg_speciality:
                    new_id = max((t.id for t in manager.teachers), default=0) + 1
                    from app.teacher import TeacherUser
                    new_teacher = TeacherUser(new_id, reg_name.strip(), reg_speciality.strip())
                    manager.teachers.append(new_teacher)
                    manager._save_data()
                    st.success(f"Successfully registered {reg_name}!")
                    st.balloons()
                else:
                    st.warning("Please enter both a name and a speciality.")

    elif action == "Remove Teacher":
        with st.form("teacher_removal_form"):
            remove_name = st.text_input("Teacher Name to Remove")
            submitted = st.form_submit_button("Remove Teacher")

            if submitted:
                teacher = next((t for t in manager.teachers if t.name.lower() == remove_name.strip().lower()), None)
                if teacher:
                    manager.teachers.remove(teacher)
                    manager._save_data()
                    st.success(f"Removed teacher: {teacher.name}")
                else:
                    st.error("No teacher found with that name.")

    # --- List All Teachers Section ---
    st.subheader("All Teachers")
    if manager.teachers:
        for t in manager.teachers:
            st.write(f"**{t.name}** — {t.speciality}")
    else:
        st.info("No teachers registered yet.")


def show_course_management_page(manager):
    st.header("Course Management")
    action = st.radio("Choose action:", ["Create Course", "Enroll Student in Course"])

    if action == "Create Course":
        with st.form("create_course_form"):
            course_name = st.text_input("Course Name")
            instrument = st.text_input("Instrument")
            
            teacher_list = {f"{t.name} ({t.speciality})": t.id for t in manager.teachers}
            teacher_name = st.selectbox("Assign Teacher", list(teacher_list.keys())) if teacher_list else None
            
            submitted = st.form_submit_button("Create Course")

            if submitted:
                if course_name and instrument and teacher_name:
                    new_id = max((c.id for c in manager.courses), default=0) + 1
                    teacher_id = teacher_list[teacher_name]
                    new_course = Course(new_id, course_name.strip(), instrument.strip(), teacher_id)
                    manager.courses.append(new_course)
                    manager._save_data()
                    st.success(f"Successfully created course: {course_name} ({instrument})")
                else:
                    st.warning("Please fill in all fields and select a teacher.")

    elif action == "Enroll Student in Course":
        with st.form("enroll_student_form"):
            student_list = {f"{s.id} - {s.name}": s.id for s in manager.students}
            selected_student = st.selectbox("Select Student", list(student_list.keys())) if student_list else None

            course_list = {f"{c.id} - {c.name} ({c.instrument})": c.id for c in manager.courses}
            selected_course = st.selectbox("Select Course", list(course_list.keys())) if course_list else None

            submitted = st.form_submit_button("Enroll Student")

            if submitted:
                if selected_student and selected_course:
                    sid = student_list[selected_student]
                    cid = course_list[selected_course]
                    student = manager.find_student_by_id(sid)
                    course = manager.find_course_by_id(cid)

                    if course and student:
                        if sid not in course.enrolled_student_ids:
                            course.enrolled_student_ids.append(sid)
                        if cid not in student.enrolled_course_ids:
                            student.enrolled_course_ids.append(cid)
                        manager._save_data()
                        st.success(f"Enrolled {student.name} (ID: {sid}) into {course.name}")
                    else:
                        st.error("Invalid student or course selected.")
                else:
                    st.warning("Please select both a student and a course.")

    # --- List All Courses ---
    st.subheader("All Courses")
    if manager.courses:
        rows = []
        for c in manager.courses:
            teacher = manager.find_teacher_by_id(c.teacher_id)
            student_names = [manager.find_student_by_id(sid).name for sid in c.enrolled_student_ids if manager.find_student_by_id(sid)]
            rows.append({
                "ID": c.id,
                "Name": c.name,
                "Instrument": c.instrument,
                "Teacher": teacher.name if teacher else "N/A",
                "Students": ", ".join(student_names) if student_names else "None"
            })
        st.table(rows)
    else:
        st.info("No courses available yet.")

def show_attendance_reports_page(manager):
    st.header("Attendance Reports")

    # --- Mark Attendance ---
    with st.form("mark_attendance_form"):
        # --- Select Student ---
        student_list = {s.name: s.id for s in manager.students}
        selected_student_name = st.selectbox("Select Student", list(student_list.keys()))
        selected_student_id = student_list.get(selected_student_name)

        # --- Select Lesson ---
        lesson_list = {}
        for course in manager.courses:
            teacher = manager.find_teacher_by_id(course.teacher_id)
            for l in course.lessons:
                # Only show lessons where student is enrolled
                if selected_student_id in course.enrolled_student_ids:
                    lesson_label = (
                        f"Lesson {l.lesson_id} - {course.name} "
                        f"with {teacher.name if teacher else 'Unknown'} "
                        f"({l.day} {l.start_time}, {l.room})"
                    )
                    lesson_list[lesson_label] = (course.id, l.lesson_id)

        selected_lesson = st.selectbox(
            "Select Lesson", list(lesson_list.keys())
        ) if lesson_list else None

        # --- Attendance Status ---
        status = st.radio("Attendance Status", ["Present", "Absent", "Late"], key="attendance_status")

        submitted = st.form_submit_button("Save Attendance")

        if submitted:
            if selected_student_id and selected_lesson:
                course_id, lesson_id = lesson_list[selected_lesson]
                new_id = max((a.id for a in manager.attendance), default=0) + 1
                new_att = Attendance(new_id, lesson_id, status)
                new_att.student_id = selected_student_id  
                manager.attendance.append(new_att)
                manager._save_data()
                st.success(f"Attendance recorded: {selected_student_name} → {selected_lesson} → {status}")
            else:
                st.warning("Please select a student and a lesson.")

    # --- Show Attendance Records ---
    st.subheader("Attendance Records")
    if manager.attendance:
        rows = []
        for a in manager.attendance:
            course = next((c for c in manager.courses if any(l.lesson_id == a.lesson_id for l in c.lessons)), None)
            lesson = next((l for l in course.lessons if l.lesson_id == a.lesson_id), None) if course else None
            teacher = manager.find_teacher_by_id(course.teacher_id) if course else None
            student = manager.find_student_by_id(getattr(a, "student_id", None))

            rows.append({
                "Attendance ID": a.id,
                "Student": student.name if student else "N/A",
                "Course": course.name if course else "N/A",
                "Teacher": teacher.name if teacher else "N/A",
                "Date": lesson.day if lesson else "N/A",
                "Time": lesson.start_time if lesson else "N/A",
                "Room": lesson.room if lesson else "N/A",
                "Status": a.status
            })

        st.dataframe(rows)
    else:
        st.info("No attendance records yet.")


def launch():
    """Sets up the main Streamlit application window and navigation."""
    st.set_page_config(layout="wide", page_title="Music School Management System")

    # Instantiate the "brain" of our app ONCE and store it in the session state.
    # This is crucial so the manager object persists as we switch pages.
    if 'manager' not in st.session_state:
        st.session_state.manager = ScheduleManager()

    st.sidebar.title("MSMS Navigation")
    # Create a radio button menu in the sidebar for page navigation.
    page = st.sidebar.radio(
        "Go to", 
        [
            "Student Management", 
            "Teacher Management",
            "Course Management",
            "Attendance Reports", 
            "Payments (stub)"
        ]
    )

    # Use an if/elif block to call the correct function to render the selected page.
    if page == "Student Management":
        show_student_management_page(st.session_state.manager)
    elif page == "Teacher Management":
        show_teacher_management_page(st.session_state.manager)
    elif page == "Course Management":
        show_course_management_page(st.session_state.manager)
    elif page == "Daily Roster":
        show_roster_page(st.session_state.manager)
    elif page == "Attendance Reports":
        show_attendance_reports_page(st.session_state.manager)
    elif page == "Payments (stub)":
        st.header("Payments")
        st.warning("This feature will be implemented in PST5.")