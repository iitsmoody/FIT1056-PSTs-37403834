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

    # --- List All Students Section ---
    st.subheader("All Students")

    if manager.students:
        for student in manager.students:
            # Find the names of all courses this student is enrolled in.
            course_names = []

            for course_id in student.enrolled_course_ids:
                course = manager.find_course_by_id(course_id)

                if course:
                    course_names.append(course.name)

            if course_names:
                st.write(
                    f"**ID:** {student.id} | "
                    f"**Name:** {student.name} | "
                    f"**Courses:** {', '.join(course_names)}"
                )
            else:
                st.write(
                    f"**ID:** {student.id} | "
                    f"**Name:** {student.name} | "
                    f"**Courses:** No current enrolments"
                )
    else:
        st.info("No students are currently registered.")

    # --- Enrolment Section ---
    st.subheader("Enrol Student in Course")

    if manager.students and manager.courses:
        # Map the displayed student details to the student's actual ID.
        student_list = {
            f"{student.id} - {student.name}": student.id
            for student in manager.students
        }

        selected_student_name = st.selectbox(
            "Select Student",
            student_list.keys(),
            key="enrol_student"
        )

        student_id = student_list[selected_student_name]
        student = manager.find_student_by_id(student_id)

        # Only show courses the selected student is not already enrolled in.
        available_courses = [
            course for course in manager.courses
            if course.id not in student.enrolled_course_ids
        ]

        if available_courses:
            course_list = {
                f"{course.id} - {course.name}": course.id
                for course in available_courses
            }

            with st.form("enrol_student_form"):
                selected_course_name = st.selectbox(
                    "Select Course",
                    course_list.keys()
                )

                submitted = st.form_submit_button("Enrol Student")

                if submitted:
                    course_id = course_list[selected_course_name]
                    success = manager.enrol_student(student_id, course_id)

                    if success:
                        st.success(
                            f"Successfully enrolled {student.name} "
                            f"in {selected_course_name}!"
                        )
                    else:
                        st.error("Could not enrol student.")
        else:
            st.info(
                f"{student.name} is already enrolled "
                f"in all available courses."
            )
    else:
        st.info("Students and courses are required for enrolment.")

    # --- Switch Course Section ---
    st.subheader("Switch Student Course")

    if manager.students and manager.courses:
        student_list = {
            f"{student.id} - {student.name}": student.id
            for student in manager.students
        }

        selected_student_name = st.selectbox(
            "Select Student",
            student_list.keys(),
            key="switch_student"
        )

        student_id = student_list[selected_student_name]
        student = manager.find_student_by_id(student_id)

        # Only show courses the selected student is currently enrolled in.
        current_courses = [
            course for course in manager.courses
            if course.id in student.enrolled_course_ids
        ]

        if current_courses:
            current_course_list = {
                f"{course.id} - {course.name}": course.id
                for course in current_courses
            }

            selected_current_course = st.selectbox(
                "Current Course",
                current_course_list.keys(),
                key="current_course"
            )

            from_course_id = current_course_list[selected_current_course]

            # A student can only switch to a course they are not already taking.
            available_courses = [
                course for course in manager.courses
                if course.id not in student.enrolled_course_ids
            ]

            if available_courses:
                new_course_list = {
                    f"{course.id} - {course.name}": course.id
                    for course in available_courses
                }

                with st.form("switch_course_form"):
                    selected_new_course = st.selectbox(
                        "New Course",
                        new_course_list.keys()
                    )

                    submitted = st.form_submit_button("Switch Course")

                    if submitted:
                        to_course_id = new_course_list[selected_new_course]

                        success = manager.switch_student_course(
                            student_id,
                            from_course_id,
                            to_course_id
                        )

                        if success:
                            st.success(
                                f"Successfully switched {student.name} "
                                f"to {selected_new_course}!"
                            )
                        else:
                            st.error("Could not switch student course.")
            else:
                st.info(
                    f"{student.name} has no other available "
                    f"courses to switch to."
                )
        else:
            st.info(
                f"{student.name} is not currently enrolled "
                f"in any courses."
            )

    # --- Update Student Section ---
    st.subheader("Update Student")

    if manager.students:
        student_list = {
            f"{student.id} - {student.name}": student.id
            for student in manager.students
        }

        selected_student_name = st.selectbox(
            "Select Student",
            student_list.keys(),
            key="update_student"
        )

        student_id = student_list[selected_student_name]
        student = manager.find_student_by_id(student_id)

        with st.form("update_student_form"):
            new_name = st.text_input(
                "Student Name",
                value=student.name
            )

            submitted = st.form_submit_button("Update Student")

            if submitted:
                success = manager.update_student(student_id, new_name)

                if success:
                    st.success("Student updated successfully.")
                else:
                    st.error("Could not update student.")
    else:
        st.info("No students are currently registered.")

    # --- Remove Student Section ---
    st.subheader("Remove Student")

    if manager.students:
        student_list = {
            f"{student.id} - {student.name}": student.id
            for student in manager.students
        }

        selected_student_name = st.selectbox(
            "Select Student to Remove",
            student_list.keys(),
            key="remove_student"
        )

        student_id = student_list[selected_student_name]
        student = manager.find_student_by_id(student_id)

        st.warning(
            f"This will remove {student.name} "
            f"and their course enrolments."
        )

        if st.button("Remove Student"):
            success = manager.remove_student(student_id)

            if success:
                st.success(
                    f"{student.name} was removed successfully."
                )
                st.rerun()
            else:
                st.error("Could not remove student.")
    else:
        st.info("No students are currently registered.")

    # --- Student Card Section ---
    st.subheader("Print Student Card")

    if manager.students:
        student_list = {
            f"{student.id} - {student.name}": student.id
            for student in manager.students
        }

        selected_student_name = st.selectbox(
            "Select Student",
            student_list.keys(),
            key="student_card"
        )

        student_id = student_list[selected_student_name]
        student = manager.find_student_by_id(student_id)

        if st.button("Print Student Card"):
            success = manager.print_student_card(student_id)

            if success:
                st.success(
                    f"Student card created for {student.name}."
                )
            else:
                st.error("Could not create student card.")
    else:
        st.info("No students are currently registered.")