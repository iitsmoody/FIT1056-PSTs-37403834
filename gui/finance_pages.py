import streamlit as st
import pandas as pd


def show_finance_page(manager):
    """Displays the finance page for recording and viewing payments."""

    st.title("Finance & Payments")
    st.write("Manage student payments and view payment history.")

    # Create a dictionary containing student names and IDs.
    student_list = {}

    for student in manager.students:
        student_list[f"{student.id} - {student.name}"] = student.id

    if not student_list:
        st.info("No students are currently registered.")
        return

    # --- Section 1: Record a New Payment ---

    st.subheader("Record New Payment")

    with st.form("payment_form"):

        selected_student = st.selectbox(
            "Select Student",
            list(student_list.keys())
        )

        amount = st.number_input(
            "Payment Amount ($)",
            min_value=0.01,
            value=50.00,
            step=1.00
        )

        method = st.text_input(
            "Payment Method (e.g., Cash, Credit Card)"
        )

        submitted = st.form_submit_button("Record Payment")

        if submitted:
            student_id = student_list[selected_student]

            if not method.strip():
                st.warning("Please enter a payment method.")

            else:
                success = manager.record_payment(
                    student_id,
                    amount,
                    method.strip()
                )

                if success:
                    st.success(
                        f"Payment of ${amount:.2f} for "
                        f"{selected_student} recorded successfully."
                    )
                else:
                    st.error("Could not record the payment.")

    st.divider()

    # --- Section 2: View Student Payment History ---

    st.subheader("Student Payment History")

    with st.form("history_form"):

        history_student = st.selectbox(
            "Select Student to View History",
            list(student_list.keys())
        )

        view_history = st.form_submit_button("View Payment History")

    if view_history:
        student_id = student_list[history_student]

        history = manager.get_payment_history(student_id)

        if history:
            st.success(
                f"Found {len(history)} payment record(s) "
                f"for {history_student}."
            )

            df = pd.DataFrame(history)

            st.dataframe(
                df,
                use_container_width=True
            )

        else:
            st.info("This student has no payment history.")
