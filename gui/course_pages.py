import streamlit as st
import pandas as pd


def show_course_management_page(manager):
    """Displays course information and course management forms."""
    st.title("Course Management")
    st.caption("Create, view, update and remove music courses.")

    if not manager.teachers:
        st.warning(
            "No teachers are registered. Please register a teacher "
            "before creating or editing courses."
        )

    # Overview statistics
    total_courses = len(manager.courses)
    total_enrolments = sum(
        len(course.enrolled_student_ids)
        for course in manager.courses
    )
    total_lessons = sum(
        len(course.lessons)
        for course in manager.courses
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Courses", total_courses)
    col2.metric("Course Enrolments", total_enrolments)
    col3.metric("Scheduled Lessons", total_lessons)

    st.divider()

    # Display all courses
    st.subheader("Available Courses")

    teacher_names = {
        teacher.id: teacher.name
        for teacher in manager.teachers
    }

    if manager.courses:
        course_rows = []

        for course in manager.courses:
            course_rows.append({
                "Course ID": course.id,
                "Course Name": course.name,
                "Instrument": course.instrument,
                "Teacher": teacher_names.get(
                    course.teacher_id,
                    "Unassigned / Missing Teacher"
                ),
                "Students": len(course.enrolled_student_ids),
                "Lessons": len(course.lessons)
            })

        st.dataframe(
            pd.DataFrame(course_rows),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No courses are currently available.")

    st.divider()

    create_tab, edit_tab, remove_tab = st.tabs([
        "Create Course",
        "Edit Course",
        "Remove Course"
    ])

    # CREATE COURSE
    with create_tab:
        st.subheader("Create a New Course")

        if not manager.teachers:
            st.info("Register a teacher first.")
        else:
            with st.form("create_course_form"):
                name = st.text_input("Course Name")
                instrument = st.text_input("Instrument")

                teacher_id = st.selectbox(
                    "Assign Teacher",
                    options=[t.id for t in manager.teachers],
                    format_func=lambda tid: (
                        f"{tid} - {teacher_names[tid]}"
                    )
                )

                submitted = st.form_submit_button(
                    "Create Course",
                    type="primary"
                )

                if submitted:
                    if manager.create_course(
                        name, instrument, teacher_id
                    ):
                        st.success("Course created successfully!")
                        st.rerun()
                    else:
                        st.error(
                            "Could not create the course. Check that "
                            "the fields are not empty, the teacher "
                            "exists, and the course name is unique."
                        )

    # EDIT COURSE
    with edit_tab:
        st.subheader("Edit an Existing Course")

        if not manager.courses:
            st.info("There are no courses to edit.")
        elif not manager.teachers:
            st.info("Register a teacher before editing courses.")
        else:
            selected_id = st.selectbox(
                "Choose Course",
                options=[c.id for c in manager.courses],
                format_func=lambda cid: (
                    f"{cid} - "
                    f"{manager.find_course_by_id(cid).name}"
                ),
                key="edit_course_select"
            )

            selected_course = manager.find_course_by_id(selected_id)

            with st.form(f"edit_course_form_{selected_id}"):
                updated_name = st.text_input(
                    "Course Name",
                    value=selected_course.name
                )

                updated_instrument = st.text_input(
                    "Instrument",
                    value=selected_course.instrument
                )

                teacher_ids = [t.id for t in manager.teachers]

                teacher_index = (
                    teacher_ids.index(selected_course.teacher_id)
                    if selected_course.teacher_id in teacher_ids
                    else 0
                )

                updated_teacher = st.selectbox(
                    "Assigned Teacher",
                    options=teacher_ids,
                    index=teacher_index,
                    format_func=lambda tid: (
                        f"{tid} - {teacher_names[tid]}"
                    )
                )

                submitted = st.form_submit_button(
                    "Save Changes",
                    type="primary"
                )

                if submitted:
                    if manager.update_course(
                        selected_id,
                        updated_name,
                        updated_instrument,
                        updated_teacher
                    ):
                        st.success("Course updated successfully!")
                        st.rerun()
                    else:
                        st.error(
                            "Could not update the course. "
                            "Check the information and try again."
                        )

    # REMOVE COURSE
    with remove_tab:
        st.subheader("Remove a Course")

        if not manager.courses:
            st.info("There are no courses to remove.")
        else:
            remove_id = st.selectbox(
                "Choose Course to Remove",
                options=[c.id for c in manager.courses],
                format_func=lambda cid: (
                    f"{cid} - "
                    f"{manager.find_course_by_id(cid).name}"
                ),
                key="remove_course_select"
            )

            course = manager.find_course_by_id(remove_id)

            if course.enrolled_student_ids or course.lessons:
                st.warning(
                    "This course has enrolled students or "
                    "scheduled lessons and cannot be removed."
                )
            else:
                st.info(
                    "This course has no enrolled students "
                    "or scheduled lessons."
                )

            confirm = st.checkbox(
                "I confirm that I want to remove this course."
            )

            if st.button(
                "Remove Course",
                disabled=not confirm,
                type="primary"
            ):
                if manager.remove_course(remove_id):
                    st.success("Course removed successfully!")
                    st.rerun()
                else:
                    st.error(
                        "Cannot remove this course. It may have "
                        "enrolments or scheduled lessons."
                    )
