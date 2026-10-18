import streamlit as st
import pandas as pd

def show_finance_page(manager):
    """Renders the UI for recording payments and viewing payment history."""
    st.header("Finance & Payments")

    # Create a dictionary mapping student names and IDs to their IDs.
    student_list = {
        f"{student.id} - {student.name}": student.id
        for student in manager.students
    }

    # Avoid displaying empty dropdowns when no students are registered.
    if not student_list:
        st.info("No students are currently registered.")
        return

    # --- Section 1: Record a Payment ---
    st.subheader("Record New Payment")

    with st.form("payment_form"):
        selected_student_name = st.selectbox(
            "Select Student",
            student_list.keys()
        )

        amount = st.number_input(
            "Payment Amount",
            min_value=0.01,
            step=1.0
        )

        method = st.text_input(
            "Payment Method (e.g., Credit Card, Cash)"
        )

        submitted = st.form_submit_button("Record Payment")

        if submitted:
            student_id = student_list[selected_student_name]

            if not method.strip():
                st.warning("Please enter a payment method.")
            else:
                success = manager.record_payment(student_id, amount, method.strip())

                if success:
                    st.success(
                        f"Payment of ${amount:.2f} for "
                        f"{selected_student_name} recorded."
                    )
                else:
                    st.error("Could not record the payment.")

    # --- Section 2: View Payment History ---
    st.subheader("View Student Payment History")

    history_student_name = st.selectbox(
        "Select Student to View History",
        student_list.keys()
    )

    if history_student_name:
        history_student_id = student_list[history_student_name]
        history = manager.get_payment_history(history_student_id)

        if history:
            df = pd.DataFrame(history)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("This student has no payment history.")