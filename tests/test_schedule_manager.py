import pytest
import csv
from app.schedule import ScheduleManager

@pytest.fixture
def fresh_manager(tmp_path):
    """Creates a fresh ScheduleManager using a temporary JSON file."""

    test_file = tmp_path / "test_data.json"

    return ScheduleManager(data_path=str(test_file))


def test_record_payment_and_history(fresh_manager):
    # ARRANGE: Create a student for the payment test.
    fresh_manager.register_student("Test Student")
    student_id_to_test = fresh_manager.students[0].id

    # ACT: Record a payment and retrieve the student's history.
    result = fresh_manager.record_payment(
        student_id_to_test, 100.00, "Credit Card"
    )
    history = fresh_manager.get_payment_history(student_id_to_test)

    # ASSERT: Verify that the payment was recorded correctly.
    assert result is True
    assert len(history) == 1
    assert history[0]["student_id"] == student_id_to_test
    assert history[0]["amount"] == 100.00
    assert history[0]["method"] == "Credit Card"


def test_get_payment_history_no_results(fresh_manager):
    # ARRANGE: Register a student without recording any payments.
    fresh_manager.register_student("Test Student")
    student_id = fresh_manager.students[0].id

    # ACT: Retrieve the student's payment history.
    history = fresh_manager.get_payment_history(student_id)

    # ASSERT: The student should have no payment records.
    assert history == []


def test_record_payment_invalid_student(fresh_manager):
    # ARRANGE: Use a student ID that does not exist.
    invalid_student_id = 999

    # ACT: Attempt to record a payment.
    result = fresh_manager.record_payment(
        invalid_student_id, 100.00, "Cash"
    )

    # ASSERT: The payment should be rejected.
    assert result is False
    assert len(fresh_manager.finance_log) == 0


def test_payment_persistence(fresh_manager):
    # ARRANGE: Register a student and record a payment.
    fresh_manager.register_student("Test Student")
    student_id = fresh_manager.students[0].id

    fresh_manager.record_payment(student_id, 150.00, "Cash")

    # ACT: Create a new manager that loads the same JSON file.
    reloaded_manager = ScheduleManager(
        data_path=fresh_manager.data_path
    )

    # ASSERT: Check that the payment was saved and loaded correctly.
    history = reloaded_manager.get_payment_history(student_id)

    assert len(history) == 1
    assert history[0]["student_id"] == student_id
    assert history[0]["amount"] == 150.00
    assert history[0]["method"] == "Cash"


def test_export_finance_report(fresh_manager, tmp_path):
    # ARRANGE: Register a student and record a payment.
    fresh_manager.register_student("Test Student")
    student_id = fresh_manager.students[0].id

    fresh_manager.record_payment(student_id, 200.00, "Cash")

    # Create a temporary path for the CSV report.
    report_path = tmp_path / "finance_report.csv"

    # ACT: Export the finance report.
    fresh_manager.export_report("finance", str(report_path))

    # ASSERT: Check that the CSV file was created.
    assert report_path.exists()

    # Read the exported CSV file.
    with open(report_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # ASSERT: Verify the exported payment details.
    assert len(rows) == 1
    assert rows[0]["student_id"] == str(student_id)
    assert float(rows[0]["amount"]) == 200.00
    assert rows[0]["method"] == "Cash"
    assert "timestamp" in rows[0]


def test_export_attendance_report(fresh_manager, tmp_path):
    # ARRANGE: Add an attendance record to the test manager.
    attendance_record = {
        "student_id": 1,
        "course_id": 101,
        "timestamp": "2026-10-18T10:00:00"
    }

    fresh_manager.attendance_log.append(attendance_record)

    # Create a temporary path for the CSV report.
    report_path = tmp_path / "attendance_report.csv"

    # ACT: Export the attendance report.
    fresh_manager.export_report("attendance", str(report_path))

    # ASSERT: Check that the CSV file was created.
    assert report_path.exists()

    # Read the CSV file.
    with open(report_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # ASSERT: Verify the exported attendance details.
    assert len(rows) == 1
    assert rows[0]["student_id"] == "1"
    assert rows[0]["course_id"] == "101"
    assert rows[0]["timestamp"] == "2026-10-18T10:00:00"


def test_register_new_student(fresh_manager):
    # ARRANGE: Create a course for the student to enrol in.
    from app.teacher import Course

    course = Course(101, "Beginner Piano", "Piano", 1)
    fresh_manager.courses.append(course)

    # ACT: Register a student and enrol them in the course.
    student = fresh_manager.register_new_student(
        "Test Student", "Piano", 101
    )

    # ASSERT: Verify the student was registered correctly.
    assert student is not False
    assert student.name == "Test Student"
    assert len(fresh_manager.students) == 1

    # ASSERT: Verify the enrolment was recorded on both sides.
    assert 101 in student.enrolled_course_ids
    assert student.id in course.enrolled_student_ids



