# gui/main_dashboard.py
import streamlit as st
from app.schedule import ScheduleManager
from app.admin_utils import backup_data
from gui.student_pages import show_student_management_page
from gui.teacher_pages import show_teacher_management_page
from gui.roster_pages import show_roster_page
from gui.finance_pages import show_finance_page
from gui.course_pages import show_course_management_page

def show_home_page(manager):
    """Displays an overview of the music school."""
    st.title("Music School Management System")
    st.caption("School administration overview")

    total_students = len(manager.students)
    total_teachers = len(manager.teachers)
    total_courses = len(manager.courses)
    total_payments = sum(
        float(payment["amount"])
        for payment in manager.finance_log
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Students", total_students)
    col2.metric("Teachers", total_teachers)
    col3.metric("Courses", total_courses)
    col4.metric("Payments Recorded", f"${total_payments:,.2f}")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("School Overview")

        st.write(
            "Use the navigation menu to manage students, "
            "teachers, courses, attendance and payments."
        )

        st.write(
            f"**Attendance Records:** {len(manager.attendance_log)}"
        )

        st.write(
            f"**Payment Records:** {len(manager.finance_log)}"
        )

    with right:
        st.subheader("Available Features")

        st.write("Student registration and enrolment")
        st.write("Teacher management")
        st.write("Course management")
        st.write("Daily lesson roster and attendance")
        st.write("Payment recording and reports")
        st.write("Data backups and activity logging")

    st.divider()

    st.subheader("Course Overview")

    if manager.courses:
        for course in manager.courses:
            with st.expander(
                f"{course.name} ({course.instrument})"
            ):
                st.write(f"**Course ID:** {course.id}")
                st.write(
                    f"**Enrolled Students:** "
                    f"{len(course.enrolled_student_ids)}"
                )
                st.write(
                    f"**Scheduled Lessons:** {len(course.lessons)}"
                )
    else:
        st.info("No courses are currently available.")


def launch():
    """Sets up the Streamlit application and navigation."""
    st.set_page_config(
        layout="wide",
        page_title="Music School Management System",
        page_icon="🎵"
    )

    if "manager" not in st.session_state:
        st.session_state.manager = ScheduleManager()

    manager = st.session_state.manager

    st.sidebar.title("🎵 MSMS")
    st.sidebar.caption("Music School Management System")
    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Student Management",
            "Teacher Management",
            "Course Management",
            "Daily Roster",
            "Payments"
        ]
    )

    st.sidebar.divider()
    st.sidebar.subheader("Administration")

    if st.sidebar.button(
        "Backup Data Now",
        use_container_width=True
    ):
        if backup_data():
            st.sidebar.success("Data backed up successfully!")
        else:
            st.sidebar.error("Backup failed.")

    st.sidebar.divider()
    st.sidebar.caption("FIT1056 | PST5")

    if page == "Dashboard":
        show_home_page(manager)

    elif page == "Student Management":
        show_student_management_page(manager)

    elif page == "Teacher Management":
        show_teacher_management_page(manager)

    elif page == "Course Management":
        show_course_management_page(manager)

    elif page == "Daily Roster":
        show_roster_page(manager)

    elif page == "Payments":
        show_finance_page(manager)
