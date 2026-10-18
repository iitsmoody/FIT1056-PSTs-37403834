# main.py - GUI Launcher
import streamlit as st
from gui.main_dashboard import launch
from app.admin_utils import init_logger, backup_data


if __name__ == "__main__":
    # Initialize logging before starting the application.
    init_logger()

    # Create an automatic backup once per Streamlit session.
    if "startup_backup_done" not in st.session_state:
        if backup_data():
            st.session_state.startup_backup_done = True

    # Launch the application.
    launch()
