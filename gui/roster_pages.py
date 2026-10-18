# gui/roster_pages.py

import streamlit as st
import pandas as pd


def show_roster_page(manager):
    """Displays the daily roster, lesson management and student check-in."""

    st.header("Daily Roster")

    # --- Section 1: View Daily Roster ---

    day = st.selectbox(
        "Select a day",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    )

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

    # --- Section 2: Schedule New Lesson ---

    st.divider()
    show_add_lesson_section(manager)

    # --- Section 3: Update Scheduled Lesson ---

    st.divider()
    show_update_lesson_section(manager)

    # --- Section 4: Cancel Scheduled Lesson ---

    st.divider()
    show_cancel_lesson_section(manager)

    # --- Section 5: Student Check-in ---

    st.divider()
    st.subheader("Student Check-in")

    # Map displayed student details to their IDs.
    student_list = {}

    for student in manager.students:
        student_list[f"{student.id} - {student.name}"] = student.id

    if not student_list:
        st.info("No students are currently registered.")
        return

    # Keep this selector outside the form so available courses update.
    selected_student_name = st.selectbox(
        "Select Student",
        list(student_list.keys())
    )

    student_id = student_list[selected_student_name]
    selected_student = manager.find_student_by_id(student_id)

    # Find courses the selected student is enrolled in.
    enrolled_courses = []

    for course in manager.courses:
        if course.id in selected_student.enrolled_course_ids:
            enrolled_courses.append(course)

    course_list = {}

    for course in enrolled_courses:
        course_list[f"{course.id} - {course.name}"] = course.id

    if not course_list:
        st.warning(
            f"{selected_student.name} is not currently enrolled in any courses."
        )
        return

    with st.form("check_in_form"):

        selected_course_name = st.selectbox(
            "Select Course",
            list(course_list.keys())
        )

        submitted = st.form_submit_button("Check-in Student")

        if submitted:
            course_id = course_list[selected_course_name]

            success = manager.check_in(student_id, course_id)

            if success:
                st.success(
                    f"Checked in {selected_student.name} "
                    f"for {selected_course_name}!"
                )
            else:
                st.error(
                    "Check-in failed. Is the student enrolled "
                    "in the selected course?"
                )


def show_add_lesson_section(manager):
    """Allows an administrator to schedule a new lesson."""

    st.subheader("Schedule New Lesson")

    if not manager.courses:
        st.info("No courses are available. Create a course first.")
        return

    # Map course labels to their IDs.
    course_options = {}

    for course in manager.courses:
        course_options[f"{course.id} - {course.name}"] = course.id

    with st.form("add_lesson_form"):

        selected_course = st.selectbox(
            "Select Course",
            list(course_options.keys())
        )

        day = st.selectbox(
            "Lesson Day",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        )

        start_time = st.text_input(
            "Start Time (e.g., 10:00)"
        )

        room = st.text_input(
            "Room (e.g., Room 1)"
        )

        submitted = st.form_submit_button("Schedule Lesson")

        if submitted:
            course_id = course_options[selected_course]

            success = manager.add_lesson(
                course_id,
                day,
                start_time,
                room
            )

            if success:
                st.success("Lesson scheduled successfully.")
                st.rerun()
            else:
                st.error("Please enter valid lesson details.")


def show_update_lesson_section(manager):
    """Allows an administrator to update an existing lesson."""

    st.subheader("Update Scheduled Lesson")

    # Only include courses with scheduled lessons.
    available_courses = []

    for course in manager.courses:
        if course.lessons:
            available_courses.append(course)

    if not available_courses:
        st.info("There are no scheduled lessons to update.")
        return

    course_options = {}

    for course in available_courses:
        course_options[f"{course.id} - {course.name}"] = course

    # Keep selectors outside the form so lesson details update.
    selected_course = st.selectbox(
        "Select Course to Update",
        list(course_options.keys())
    )

    course = course_options[selected_course]

    lesson_options = {}

    for index in range(len(course.lessons)):
        lesson = course.lessons[index]

        label = (
            f"Lesson {index + 1}: "
            f"{lesson['day']} at {lesson['start_time']} "
            f"- {lesson['room']}"
        )

        lesson_options[label] = index

    selected_lesson = st.selectbox(
        "Select Lesson to Update",
        list(lesson_options.keys())
    )

    lesson_index = lesson_options[selected_lesson]
    lesson = course.lessons[lesson_index]

    with st.form("update_lesson_form"):

        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ]

        day_index = 0

        if lesson["day"] in days:
            day_index = days.index(lesson["day"])

        day = st.selectbox(
            "New Lesson Day",
            days,
            index=day_index
        )

        start_time = st.text_input(
            "New Start Time",
            value=lesson["start_time"],
            key=f"update_time_{course.id}_{lesson_index}"
        )

        room = st.text_input(
            "New Room",
            value=lesson["room"],
            key=f"update_room_{course.id}_{lesson_index}"
        )

        submitted = st.form_submit_button("Update Lesson")

        if submitted:
            success = manager.update_lesson(
                course.id,
                lesson_index,
                day,
                start_time,
                room
            )

            if success:
                st.success("Lesson updated successfully.")
                st.rerun()
            else:
                st.error("Could not update the lesson.")


def show_cancel_lesson_section(manager):
    """Allows an administrator to cancel a scheduled lesson."""

    st.subheader("Cancel Scheduled Lesson")

    # Only include courses that have scheduled lessons.
    available_courses = []

    for course in manager.courses:
        if course.lessons:
            available_courses.append(course)

    if not available_courses:
        st.info("There are no scheduled lessons to cancel.")
        return

    course_options = {}

    for course in available_courses:
        course_options[f"{course.id} - {course.name}"] = course

    # Keep course selector outside the form so lessons update.
    selected_course = st.selectbox(
        "Select Course to Cancel a Lesson From",
        list(course_options.keys())
    )

    course = course_options[selected_course]

    lesson_options = {}

    for index in range(len(course.lessons)):
        lesson = course.lessons[index]

        label = (
            f"Lesson {index + 1}: "
            f"{lesson['day']} at {lesson['start_time']} "
            f"- {lesson['room']}"
        )

        lesson_options[label] = index

    with st.form("cancel_lesson_form"):

        selected_lesson = st.selectbox(
            "Select Lesson to Cancel",
            list(lesson_options.keys())
        )

        reason = st.text_input(
            "Reason for Cancellation"
        )

        confirmed = st.checkbox(
            "I confirm that I want to cancel this lesson."
        )

        submitted = st.form_submit_button("Cancel Lesson")

        if submitted:

            if not reason.strip():
                st.warning("Please enter a cancellation reason.")

            elif not confirmed:
                st.warning("Please confirm the cancellation.")

            else:
                lesson_index = lesson_options[selected_lesson]

                success = manager.cancel_lesson(
                    course.id,
                    lesson_index,
                    reason
                )

                if success:
                    st.success("Lesson cancelled successfully.")
                    st.rerun()
                else:
                    st.error("Could not cancel the lesson.")