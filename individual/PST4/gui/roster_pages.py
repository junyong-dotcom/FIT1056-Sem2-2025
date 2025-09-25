# gui/roster_pages.py
import streamlit as st
import pandas as pd

def show_roster_page(manager):
    """Renders the daily roster and check-in functionality."""
    st.header("Daily Roster")

    # --- View Roster Section (remains the same) ---
    day = st.selectbox("Select a day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    roster = manager.get_roster_for_day(day)

    # ... (code to display the dataframe) ...

    if roster:
        df = pd.DataFrame(roster)
        st.subheader(f"Roster for {day}")
        st.dataframe(df)
    else:
        st.info(f"No students checked in yet for {day}.")

    st.subheader("Student Check-in")
    with st.form("check_in_form"):
        student_list = {s.name: s.id for s in manager.students}
        course_list = {c.name: c.id for c in manager.courses}
        
        selected_student_name = st.selectbox("Select Student", list(student_list.keys()))
        selected_course_name = st.selectbox("Select Course", list(course_list.keys()))
        
        submitted = st.form_submit_button("Check-in Student")

        if submitted:
            student_id = student_list[selected_student_name]
            course_id = course_list[selected_course_name]

            # This call now works because we implemented the method in PST3.
            success = manager.check_in(student_id, course_id)

            if success:
                st.success(f"Checked in {selected_student_name} for {selected_course_name}!")
            else:
                # The manager's print statements will go to the console, but we can add a GUI error too.
                st.error("Check-in failed. See console for details. (Is the student enrolled in that course?)")