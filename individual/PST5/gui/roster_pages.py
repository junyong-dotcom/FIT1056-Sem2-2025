# gui/roster_pages.py
import streamlit as st
import pandas as pd

def show_roster_page(manager):
    """Renders the daily roster and check-in functionality."""
    st.header("Daily Roster")

    # --- View Roster Section (remains the same) ---
    day = st.selectbox("Select a day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    roster = manager.get_roster_for_day(day)

    st.subheader(f"Roster Overview for {day}")
    # ... (code to display the dataframe) ...

    if roster:
        for r in roster:
            r["CheckedIn"] = "Yes" if r.get("CheckedIn") else "No"

        df = pd.DataFrame(roster)
        df = df[["Course", "Instrument", "Time", "Teacher", "Student", "CheckedIn"]]
        st.dataframe(df, use_container_width=True)
    else:
        st.info(f"No lessons or check-ins yet for {day}.")

    st.markdown("---")

    st.subheader("Student Check-in")
    with st.form("check_in_form"):
        # --- Student dropdown ---
        student_list = {s.name: s.id for s in manager.students}
        selected_student_name = st.selectbox("Select Student", list(student_list.keys()))
        
        # --- Course dropdown ---
        course_list = {c.name: c.id for c in manager.courses}
        selected_course_name = st.selectbox("Select Course", list(course_list.keys()))
        
        # --- Only show lessons for the selected course ---
        lesson_list = {}
        selected_course_id = course_list[selected_course_name]
        selected_course = manager.find_course_by_id(selected_course_id)
        
        if selected_course and selected_course.lessons:
            for l in selected_course.lessons:
                lesson_label = f"{l['lesson_id']} - {selected_course.name} ({l['day']} {l['start_time']})"
                lesson_list[lesson_label] = l['lesson_id']

        if lesson_list:
            selected_lesson_label = st.selectbox("Select Lesson", list(lesson_list.keys()))
            selected_lesson_id = lesson_list[selected_lesson_label]
        else:
            st.info("No lessons found for this course.")
            selected_lesson_id = None

        # --- Submit ---
        submitted = st.form_submit_button("Check-in Student")

        if submitted:
            if not selected_lesson_id:
                st.warning("Please select a lesson.")
            else:
                student_id = student_list[selected_student_name]
                success = manager.check_in(student_id, selected_course_id, selected_lesson_id)
                if success:
                    st.success(f"Checked in {selected_student_name} for {selected_course_name} → {selected_lesson_label}!")
                else:
                    st.error("Check-in failed. Is the student enrolled in this course?")
