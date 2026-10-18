import logging
import shutil
import datetime
import os

def init_logger(log_file="msms.log"):
    """Configures the root logger to write messages to a file."""

    # Configure logging to record INFO messages and above.
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_file,
        filemode='a'
    )

    print(f"Logging configured. Outputting to {log_file}")


def backup_data(data_path="data/msms.json", backup_dir="data/backups"):
    """Creates a timestamped backup of the main data file."""

    # Create the backup directory if it does not already exist.
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Generate a unique filename using the current date and time.
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"msms_backup_{timestamp}.json"
    backup_filepath = os.path.join(backup_dir, backup_filename)

    try:
        # Copy the original data file to the backup location.
        shutil.copy(data_path, backup_filepath)

        # Record the successful backup in the log.
        logging.info(f"Data successfully backed up to {backup_filepath}")
        return True

    except Exception as e:
        # Record the error if the backup fails.
        logging.error(f"Failed to create backup: {e}")
        return False
