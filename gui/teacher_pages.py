# gui/teacher_pages.py
import streamlit as st

def show_teacher_management_page(manager):
    """Renders the teacher management functionality."""
    st.header("Teacher Management")

    # --- Search Teacher Section ---
    st.subheader("Find a Teacher")
    search_term = st.text_input("Search by teacher name or speciality")

    if search_term:
        results = manager.find_teachers(search_term)

        if results:
            for teacher in results:
                st.write(f"**ID:** {teacher.id}")
                st.write(f"**Name:** {teacher.name}")
                st.write(f"**Speciality:** {teacher.speciality}")
                st.divider()
        else:
            st.info("No teachers found.")

    # --- List All Teachers Section ---
    st.subheader("All Teachers")

    if manager.teachers:
        for teacher in manager.teachers:
            st.write(
                f"**ID:** {teacher.id} | "
                f"**Name:** {teacher.name} | "
                f"**Speciality:** {teacher.speciality}"
            )
    else:
        st.info("No teachers are currently registered.")

    st.divider()

    # --- Register Teacher Section ---
    st.subheader("Register New Teacher")

    with st.form("teacher_registration_form"):
        teacher_name = st.text_input("Teacher Name")
        speciality = st.text_input("Speciality")
        submitted = st.form_submit_button("Register Teacher")

        if submitted:
            if teacher_name and speciality:
                success = manager.register_teacher(teacher_name, speciality)

                if success:
                    st.success(f"Successfully registered {teacher_name}.")
                else:
                    st.error("Could not register teacher.")
            else:
                st.warning("Please enter a teacher name and speciality.")

    st.divider()

    # --- Update Teacher Section ---
    st.subheader("Update Teacher")

    if manager.teachers:
        teacher_list = {
            f"{teacher.id} - {teacher.name}": teacher.id
            for teacher in manager.teachers
        }

        selected_teacher_name = st.selectbox(
            "Select Teacher",
            teacher_list.keys(),
            key="update_teacher"
        )

        teacher_id = teacher_list[selected_teacher_name]
        teacher = next(
            (teacher for teacher in manager.teachers if teacher.id == teacher_id),
            None
        )

        with st.form("update_teacher_form"):
            new_name = st.text_input("Teacher Name", value=teacher.name)
            new_speciality = st.text_input("Speciality", value=teacher.speciality)
            submitted = st.form_submit_button("Update Teacher")

            if submitted:
                if manager.update_teacher(teacher_id, new_name, new_speciality):
                    st.success("Teacher updated successfully.")
                else:
                    st.error("Could not update teacher.")
    else:
        st.info("No teachers are currently registered.")

    st.divider()

    # --- Remove Teacher Section ---
    st.subheader("Remove Teacher")

    if manager.teachers:
        teacher_list = {
            f"{teacher.id} - {teacher.name}": teacher.id
            for teacher in manager.teachers
        }

        selected_teacher_name = st.selectbox(
            "Select Teacher to Remove",
            teacher_list.keys(),
            key="remove_teacher"
        )

        teacher_id = teacher_list[selected_teacher_name]
        teacher = next(
            (teacher for teacher in manager.teachers if teacher.id == teacher_id),
            None
        )

        st.warning(f"This will remove {teacher.name} from the system.")

        if st.button("Remove Teacher"):
            if manager.remove_teacher(teacher_id):
                st.success(f"{teacher.name} was removed successfully.")
                st.rerun()
            else:
                st.error("Could not remove teacher.")
    else:
        st.info("No teachers are currently registered.")