# gui/roster_pages.py
import streamlit as st
import pandas as pd

def show_roster_page(manager):
    """Renders the daily roster and check-in functionality."""
    st.header("Daily Roster")

    # --- View Roster Section (remains the same) ---
    day = st.selectbox("Select a day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    lessons = manager.get_lessons_for_day(day)

    if lessons:
        df = pd.DataFrame(lessons)

        # Use user-friendly column names in the GUI.
        df = df.rename(columns={
            "course_name": "Course",
            "instrument": "Instrument",
            "start_time": "Start Time",
            "room": "Room"
        })

        st.dataframe(df, use_container_width=True)

    else:
        st.info(f"No lessons scheduled for {day}.")

    # --- Student Check-in Section (now works correctly) ---
    st.subheader("Student Check-in")

    # To make this user-friendly, we should populate the dropdowns dynamically.
    # Get lists of students and courses from the manager.

    # Map the displayed student details to their IDs.
    student_list = {
        f"{student.id} - {student.name}": student.id
        for student in manager.students
    }

    # Stop gracefully if there are no registered students.
    if not student_list:
        st.info("No students are currently registered.")
        return

    # Keep this outside the form so changing the student immediately updates the available courses.
    selected_student_name = st.selectbox(
        "Select Student",
        student_list.keys()
    )

    student_id = student_list[selected_student_name]
    selected_student = manager.find_student_by_id(student_id)

    # Only include courses the selected student is enrolled in.
    enrolled_courses = [
        course for course in manager.courses
        if course.id in selected_student.enrolled_course_ids
    ]

    course_list = {
        course.name: course.id
        for course in enrolled_courses
    }

    # Stop gracefully if the selected student has no enrolled courses.
    if not course_list:
        st.warning(
            f"{selected_student.name} is not currently enrolled in any courses."
        )
        return

    with st.form("check_in_form"):
        selected_course_name = st.selectbox(
            "Select Course",
            course_list.keys()
        )

        submitted = st.form_submit_button("Check-in Student")

        if submitted:
            # Convert the selected course name back to its ID.
            course_id = course_list[selected_course_name]

            # Record the attendance using the ScheduleManager.
            success = manager.check_in(student_id, course_id)

            if success:
                st.success(
                    f"Checked in {selected_student.name} "
                    f"for {selected_course_name}!"
                )
            else:
                # The manager's print statements will go to the console,
                # but we can add a GUI error too.
                st.error(
                    "Check-in failed. See console for details. "
                    "(Is the student enrolled in that course?)"
                )