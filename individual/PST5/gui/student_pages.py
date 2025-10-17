# gui/student_pages.py
import streamlit as st

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    st.subheader("Find a Student")
    search_name = st.text_input("Enter student name")
    if st.button("Search"):
        student = manager.find_student(search_name)
        if student:
            for s in student:
                enrolled_courses = [manager.find_course_by_id(cid) for cid in s.enrolled_course_ids]
                instruments = ", ".join([c.instrument for c in enrolled_courses if c]) or "None"
                st.success(f"ID: {s.id} | Name: {s.name} | Instrument(s): {instruments}")
        else:
            st.warning("Student not found.")

    st.subheader("Manage Students")
    action = st.radio("Choose action:", ["Register Student", "Remove Student"])

    if action == "Register Student":
        with st.form("registration_form"):
            reg_name = st.text_input("New Student Name")

            available_instruments = sorted({c.instrument for c in manager.courses})

            if available_instruments:
                reg_instrument = st.selectbox("Select First Instrument", available_instruments)
                submitted = st.form_submit_button("Register Student")

                if submitted:
                    if reg_name:
                        new_student = manager.register_new_student(reg_name, reg_instrument)
                        if new_student:
                            st.success(f"Successfully registered {reg_name}! (ID: {new_student.id})")
                            st.balloons()
                        else:
                            st.error(f"Could not register student. A teacher for {reg_instrument} might not be available.")
                    else:
                        st.warning("Please enter a name before registering.")
            else:
                st.warning("No courses available yet. Please add courses before registering students.")


    elif action == "Remove Student":
        with st.form("remove_student_form"):
            remove_id = st.number_input("Enter Student ID to Remove", min_value=1, step=1)
            submitted = st.form_submit_button("Remove Student")

            if submitted:
                student = manager.find_student_by_id(remove_id)
                if student:
                    # Remove student from global list
                    manager.students.remove(student)
                    # Also remove from enrolled_course_ids in courses
                    for c in manager.courses:
                        if student.id in c.enrolled_student_ids:
                            c.enrolled_student_ids.remove(student.id)
                    manager._save_data()
                    st.success(f"Removed student: {student.name} (ID: {student.id})")
                else:
                    st.error("No student found with that ID.")
