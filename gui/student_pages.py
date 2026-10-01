# gui/student_pages.py
import streamlit as st

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    # --- Search Section ---
    st.subheader("Find a Student")

    search_term = st.text_input("Search by student name")

    if search_term:
        results = manager.find_students(search_term)
        
        if results:
            for student in results:
                # Find all courses the student is enrolled in.
                enrolled_courses = [
                    course for course in manager.courses
                    if course.id in student.enrolled_course_ids
                ]

                st.write(f"**ID:** {student.id}")
                st.write(f"**Name:** {student.name}")

                if enrolled_courses:
                    for course in enrolled_courses:
                        st.write(
                            f"**Course:** {course.name} | "
                            f"**Instrument:** {course.instrument}"
                        )
                else:
                    st.write("**Courses:** No current enrolments")

                st.divider()

        else:
            st.info("No students found.")

    # --- Registration Section ---
    st.subheader("Register New Student")

    # Get the available instruments from the existing courses.
    instrument_list = sorted(set(course.instrument for course in manager.courses))

    # This is outside the form so changing the instrument reruns the page.
    reg_instrument = st.selectbox(
        "First Instrument",
        instrument_list,
        key="registration_instrument"
    )

    # Find only the courses that match the selected instrument.
    matching_courses = [
        course for course in manager.courses
        if course.instrument == reg_instrument
    ]

    course_list = {
        course.name: course.id
        for course in matching_courses
    }

    with st.form("registration_form"):
        reg_name = st.text_input("New Student Name")

        selected_course_name = st.selectbox(
            "Select Course",
            list(course_list.keys())
        )

        submitted = st.form_submit_button("Register Student")

        if submitted:
            if reg_name and reg_instrument:
                # Convert the selected course name into its course ID.
                selected_course_id = course_list[selected_course_name]
                
                # Register the student with their chosen instrument and course.
                new_student = manager.register_new_student(
                    reg_name,
                    reg_instrument,
                    selected_course_id
                )

                if new_student:
                    st.success(
                        f"Successfully registered {reg_name} "
                        f"for {selected_course_name}!"
                    )

                else:
                    st.error(
                        f"Could not register student for {reg_instrument}."
                    )
            else:
                st.warning("Please enter a student name.")