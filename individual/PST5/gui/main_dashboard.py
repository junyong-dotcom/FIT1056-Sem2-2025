# gui/main_dashboard.py
import streamlit as st
from app.schedule import ScheduleManager
from app.student import Attendance
from app.teacher import Course, Lesson
from app.admin_utils import init_logger, backup_data 
from app.admin_utils import backup_data
from gui.student_pages import show_student_management_page
from gui.roster_pages import show_roster_page
from gui.finance_pages import show_finance_page

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
            st.subheader("Register New Teacher")

            reg_name = st.text_input("Teacher Name")

            available_specialties = sorted({c.instrument for c in manager.courses})

            reg_speciality = st.selectbox(
                "Select Speciality (Instrument)",
                ["-- Select a speciality --"] + available_specialties,
                index=0
            )

            submitted = st.form_submit_button("Register Teacher")

            if submitted:
                if not reg_name:
                    st.warning("Please enter the teacher’s name.")
                elif reg_speciality == "-- Select a speciality --":
                    st.warning("Please select a speciality (instrument).")
                else:
                    new_id = max(
                        (a["id"] if isinstance(a, dict) else a.id for a in manager.attendance),
                        default=0
                    ) + 1
                    from app.teacher import TeacherUser

                    new_teacher = TeacherUser(new_id, reg_name.strip(), reg_speciality.strip())
                    manager.teachers.append(new_teacher)
                    manager._save_data()

                    st.success(f"Successfully registered {reg_name} ({reg_speciality})!")
                    st.balloons()

    elif action == "Remove Teacher":
        with st.form("teacher_removal_form"):
            st.subheader("Remove Existing Teacher")

            if manager.teachers:
                teacher_options = ["-- Select a teacher --"] + [
                    f"{t.name} (ID: {t.id}, {t.speciality})" for t in manager.teachers
                ]

                selected_teacher = st.selectbox("Select Teacher to Remove", teacher_options)

                submitted = st.form_submit_button("Remove Teacher")

                if submitted:
                    if selected_teacher == "-- Select a teacher --":
                        st.warning("Please select a teacher to remove.")
                    else:
                        # Find teacher object by name and ID
                        name_part = selected_teacher.split(" (ID:")[0].strip()
                        teacher = next((t for t in manager.teachers if t.name == name_part), None)

                        if teacher:
                            manager.teachers.remove(teacher)
                            manager._save_data()
                            st.success(f"Removed teacher: {teacher.name} ({teacher.speciality})")
                        else:
                            st.error("Teacher not found.")
            else:
                st.info("No teachers available to remove.")


    # --- List All Teachers Section ---
    st.subheader("All Teachers")
    if manager.teachers:
        for t in manager.teachers:
            st.write(f"**{t.name}** — {t.speciality}")
    else:
        st.info("No teachers registered yet.")


def show_course_management_page(manager):
    st.header("Course Management")
    action = st.radio("Choose action:", ["Create Course", "Update Lesson", "Enroll Student in Course", "Assign Teacher to Course", "Remove Course"])

    if action == "Create Course":
        with st.form("create_course_form"):
            course_name = st.text_input("Course Name")
            instrument = st.text_input("Instrument")
            
            teacher_list = {f"{t.name} ({t.speciality})": t.id for t in manager.teachers}
            teacher_labels = ["None"] + list(teacher_list.keys())
            teacher_name = st.selectbox("Assign Teacher", teacher_labels)
            
            submitted = st.form_submit_button("Create Course")

        if submitted:
            if not course_name or not instrument:
                st.warning("Please fill in both course name and instrument.")
            else:
                new_id = max((c.id for c in manager.courses), default=0) + 1
                teacher_id = None if teacher_name == "None" else teacher_list[teacher_name]

            # Create course with empty lessons list
            new_course = Course(
                new_id, course_name.strip(), instrument.strip(), teacher_id,
                enrolled_student_ids=[], lessons=[]
            )
            manager.courses.append(new_course)
            manager._save_data()
            st.success(f"Successfully created course: {course_name} ({instrument})")
            
            # After creating new_course
            st.session_state['new_course_temp'] = new_course
    # --- Add Lesson Form (Separate) ---
    new_course = st.session_state.get('new_course_temp')
    if new_course:
        st.subheader(f"Add Lesson for {new_course.name}")
        with st.form(f"add_lesson_form_{new_course.id}"):
            day = st.selectbox("Lesson Day", ["Monday","Tuesday","Wednesday","Thursday","Friday"])
            start_time = st.time_input("Start Time")
            room = st.text_input("Room (optional)")
            submitted_lesson = st.form_submit_button("Add Lesson")

            if submitted_lesson:
                lesson_id = manager.next_lesson_id
                manager.next_lesson_id += 1
                new_course.lessons.append({
                    "lesson_id": lesson_id,
                    "course_name": new_course.name,
                    "day": day,
                    "start_time": start_time.strftime("%H:%M"),
                    "room": room
                })
                manager._save_data()
                st.success(f"Lesson successfully added to {new_course.name} on {day} at {start_time.strftime('%H:%M')}")
                # Clear session state to hide form if you want
                del st.session_state['new_course_temp']

    # --- Update Lesson Section ---
    elif action == "Update Lesson":
        st.subheader("Update or Add Lesson")

        if not manager.courses:
            st.info("No courses found.")
        else:
            # Select course
            course_options = {f"{c.name} ({c.instrument})": c for c in manager.courses}
            selected_course_name = st.selectbox("Select Course", list(course_options.keys()))
            selected_course = course_options[selected_course_name]

            # If course has no lesson yet
            if not selected_course.lessons:
                st.info("No lessons assigned yet for this course. You can add one below.")
                with st.form(f"add_lesson_for_{selected_course.id}"):
                    day = st.selectbox("Lesson Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
                    start_time = st.time_input("Start Time")
                    room = st.text_input("Room")
                    add_submitted = st.form_submit_button("Add Lesson")

                    if add_submitted:
                        lesson_id = manager.next_lesson_id
                        manager.next_lesson_id += 1
                        selected_course.lessons.append({
                            "lesson_id": lesson_id,
                            "course_name": selected_course.name,
                            "day": day,
                            "start_time": start_time.strftime("%H:%M"),
                            "room": room
                        })
                        manager._save_data()
                        st.success(f"Lesson added for {selected_course.name} on {day} at {start_time.strftime('%H:%M')} in {room}")
            else:
                # If lesson exists, show it and allow update
                lesson = selected_course.lessons[0]  # assuming one lesson per course
                st.write(f"**Current Lesson Info:**")
                st.write(f"- Day: {lesson['day']}")
                st.write(f"- Time: {lesson['start_time']}")
                st.write(f"- Room: {lesson['room'] if lesson['room'] else 'Not assigned'}")

                with st.form(f"update_lesson_for_{selected_course.id}"):
                    new_day = st.selectbox("New Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], index=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].index(lesson['day']))
                    new_time = st.time_input("New Start Time")
                    new_room = st.text_input("New Room", value=lesson['room'])
                    update_submitted = st.form_submit_button("Update Lesson")

                    if update_submitted:
                        lesson['day'] = new_day
                        lesson['start_time'] = new_time.strftime("%H:%M")
                        lesson['room'] = new_room
                        manager._save_data()
                        st.success(f"Lesson updated for {selected_course.name}: {new_day} at {new_time.strftime('%H:%M')} in {new_room}")


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

    elif action == "Assign Teacher to Course":
        with st.form("assign_teacher_form"):
            st.subheader("Assign Teacher to Course")

            if not manager.courses:
                st.info("No courses available.")
            elif not manager.teachers:
                st.info("No teachers available.")
            else:
                course_labels = [
                    f"{c.name} (ID: {c.id}, {c.instrument})" for c in manager.courses
                ]
                selected_course_label = st.selectbox("Select Course", ["-- Select a course --"] + course_labels)

                selected_course = None
                available_teachers = []
                if selected_course_label != "-- Select a course --":
                    selected_course_name = selected_course_label.split(" (ID:")[0].strip()
                    selected_course = next((c for c in manager.courses if c.name == selected_course_name), None)

                    if selected_course:
                        available_teachers = [
                            t for t in manager.teachers
                            if t.speciality.lower() == selected_course.instrument.lower()
                        ]

                if available_teachers:
                    teacher_labels = [
                        f"{t.name} (ID: {t.id}, {t.speciality})" for t in available_teachers
                    ]
                    selected_teacher_label = st.selectbox("Select Teacher", ["-- Select a teacher --"] + teacher_labels)
                elif selected_course:
                    st.warning(f"No teachers available for {selected_course.instrument}.")
                    selected_teacher_label = "-- Select a teacher --"
                else:
                    selected_teacher_label = "-- Select a teacher --"

                submitted = st.form_submit_button("Assign Teacher")

                if submitted:
                    if selected_course_label == "-- Select a course --":
                        st.warning("Please select a course first.")
                    elif selected_teacher_label == "-- Select a teacher --":
                        st.warning("Please select a teacher.")
                    else:
                        selected_teacher_name = selected_teacher_label.split(" (ID:")[0].strip()
                        teacher = next((t for t in manager.teachers if t.name == selected_teacher_name), None)

                        if selected_course and teacher:
                            selected_course.teacher_id = teacher.id = teacher.id
                            manager._save_data()
                            st.success(f"Assigned {teacher.name} to {selected_course.name} ({selected_course.instrument}).")
                        else:
                            st.error("Could not assign teacher. Please check your selection.")

    elif action == "Remove Course":
        with st.form("remove_course_form"):
            st.subheader("Remove Existing Course")

            if manager.courses:
                course_options = ["-- Select a course --"] + [
                    f"{c.name} (ID: {c.id}, {c.instrument})" for c in manager.courses
                ]

                selected_course = st.selectbox("Select Course to Remove", course_options)

                submitted = st.form_submit_button("Remove Course")

                if submitted:
                    if selected_course == "-- Select a course --":
                        st.warning("Please select a course to remove.")
                    else:
                        name_part = selected_course.split(" (ID:")[0].strip()
                        course = next((c for c in manager.courses if c.name == name_part), None)

                        if course:
                            manager.courses.remove(course)
                            manager._save_data()
                            st.success(f"Removed course: {course.name} ({course.instrument})")
                        else:
                            st.error("Course not found.")
            else:
                st.info("No courses available to remove.")

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
                        f"Lesson {l['lesson_id']} - {course.name} "
                        f"with {teacher.name if teacher else 'Unknown'} "
                        f"({l['day']} {l['start_time']}, {l['room']})"
                    )
                    lesson_list[lesson_label] = (course.id, l["lesson_id"])

        selected_lesson = st.selectbox(
            "Select Lesson", list(lesson_list.keys())
        ) if lesson_list else None

        # --- Attendance Status ---
        status = st.radio("Attendance Status", ["Present", "Absent", "Late"], key="attendance_status")

        submitted = st.form_submit_button("Save Attendance")

        if submitted:
            if selected_student_id and selected_lesson:
                course_id, lesson_id = lesson_list[selected_lesson]
                
                existing_att = next(
                    (a for a in manager.attendance 
                    if getattr(a, "student_id", None) == selected_student_id 
                    and getattr(a, "lesson_id", None) == lesson_id),
                    None
                )

                if existing_att:
                    # Just update the status
                    existing_att.status = status
                    st.info(f"Updated attendance: {selected_student_name} → {selected_lesson} → {status}")
                else:
                    # Create a new record only if not checked in before
                    new_id = max(
                        (a["id"] if isinstance(a, dict) else getattr(a, "id", 0))
                        for a in manager.attendance
                    ) + 1 if manager.attendance else 1
                    new_att = Attendance(new_id, lesson_id, status)
                    new_att.student_id = selected_student_id  
                    manager.attendance.append(new_att)
                    st.success(f"New attendance recorded: {selected_student_name} → {selected_lesson} → {status}")

                manager._save_data()
                
            else:
                st.warning("Please select a student and a lesson.")

    # --- Show Attendance Records ---
    st.subheader("Attendance Records")
    if manager.attendance:
        rows = []
        for a in manager.attendance:
            course = next(
                (c for c in manager.courses 
                    if any(
                        l["lesson_id"] == (a["lesson_id"] if isinstance(a, dict) else a.lesson_id)
                        for l in c.lessons)), None)
            lesson = next(
                (l for l in course.lessons if l["lesson_id"] == (a["lesson_id"] if isinstance(a, dict) else a.lesson_id)),
                None
            ) if course else None
            teacher = manager.find_teacher_by_id(course.teacher_id) if course else None
            student_id = a.get("student_id") if isinstance(a, dict) else getattr(a, "student_id", None)
            student = manager.find_student_by_id(student_id)

            rows.append({
                "Attendance ID": a.get("id") if isinstance(a, dict) else a.id,
                "Student": student.name if student else "N/A",
                "Course": course.name if course else "N/A",
                "Teacher": teacher.name if teacher else "N/A",
                "Date": lesson["day"] if lesson else "N/A",
                "Time": lesson["start_time"] if lesson else "N/A",
                "Room": lesson["room"] if lesson and lesson.get("room") else "N/A",
                "Status": a.get("status") if isinstance(a, dict) else a.status
            })

        st.dataframe(rows)
    else:
        st.info("No attendance records yet.")

def launch():
    """Sets up the main Streamlit application window and navigation."""
    st.set_page_config(layout="wide", page_title="Music School Management System")

    init_logger()

    backup_data()

    # Instantiate the "brain" of our app ONCE and store it in the session state.
    # This is crucial so the manager object persists as we switch pages.
    if 'manager' not in st.session_state:
        st.session_state.manager = ScheduleManager()

    st.sidebar.title("MSMS Navigation")
    # Create a radio button menu in the sidebar for page navigation.
    page = st.sidebar.radio("Go to", [
            "Student Management",           
            "Course Management",
            "Teacher Management",
            "Daily Roster", 
            "Payments",
            "Attendance Reports", ])

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
    elif page == "Payments":
        show_finance_page(st.session_state.manager)

    if st.sidebar.button("Backup Now"):
        if backup_data():
            st.success("Backup completed successfully.")
        else:
            st.error("Backup failed. Check logs for details.")