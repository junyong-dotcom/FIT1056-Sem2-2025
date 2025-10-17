# tests/test_schedule_manager.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
import pytest
import datetime

from app.schedule import ScheduleManager
from app.teacher import Course
from app.student import StudentUser

@pytest.fixture
def fresh_manager(tmp_path):
    """
    Creates a fresh ScheduleManager instance using a temporary test data file
    so tests won't touch your real msms.json.
    """
    test_file = str(tmp_path / "test_data.json")
    # Ensure no old test file exists.
    if os.path.exists(test_file):
        os.remove(test_file)
    return ScheduleManager(data_path=test_file)

def test_create_course_by_appending(fresh_manager):
    # ARRANGE
    manager = fresh_manager
    assert len(manager.courses) == 0

    # ACT
    new_course = Course(course_id=201, name="Beginner Piano", instrument="Piano", teacher_id=None)
    manager.courses.append(new_course)
    manager._save_data()

    # ASSERT
    assert len(manager.courses) == 1
    assert manager.courses[0].name == "Beginner Piano"
    assert manager.courses[0].instrument == "Piano"

def test_record_payment_and_history(fresh_manager):
    # ARRANGE
    manager = fresh_manager
    # Add a student so record_payment will succeed
    student = StudentUser(user_id=1, name="Test Student", enrolled_course_ids=[])
    manager.students.append(student)

    # ACT
    manager.record_payment(student_id=1, amount=100.00, method="Credit Card")
    history = manager.get_payment_history(1)

    # ASSERT
    assert isinstance(history, list)
    assert len(history) == 1
    assert history[0]["amount"] == 100.00
    assert history[0]["method"] == "Credit Card"
    # timestamp should be present and parseable
    assert "timestamp" in history[0]
    # basic ISO-format check
    try:
        datetime.datetime.fromisoformat(history[0]["timestamp"])
    except Exception:
        pytest.fail("Timestamp is not in ISO format")

def test_get_payment_history_no_results(fresh_manager):
    # ARRANGE
    manager = fresh_manager
    # Ensure no payments exist for student ID 999
    # (Also ensure student exists or not — method just filters finance_log.)
    manager.finance_log = []

    # ACT
    history = manager.get_payment_history(999)

    # ASSERT
    assert isinstance(history, list)
    assert history == []

def test_add_lesson_to_course(fresh_manager):
    # ARRANGE
    manager = fresh_manager
    new_course = Course(course_id=300, name="Test Course", instrument="Guitar", teacher_id=None)
    manager.courses.append(new_course)
    manager._save_data()

    # ACT
    lesson_id = manager.add_lesson_to_course(course_id=300, day="Friday", start_time="09:00", room="R1")

    # ASSERT
    assert lesson_id is not None
    course = manager.find_course_by_id(300)
    assert course is not None
    assert any(l["lesson_id"] == lesson_id for l in course.lessons)

def test_cancel_lesson_removes_from_course(fresh_manager):
    # ARRANGE
    manager = fresh_manager
    course = Course(course_id=400, name="Cancel Test", instrument="Violin", teacher_id=None,
                    lessons=[{"lesson_id": 9001, "course_name": "Cancel Test", "day": "Monday", "start_time": "08:00", "room": "R2"}])
    manager.courses.append(course)
    manager._save_data()
    # ensure lesson present
    assert any(l["lesson_id"] == 9001 for l in course.lessons)

    # ACT
    manager.cancel_lesson(lesson_id=9001, reason="Testing cancel")

    # ASSERT
    # Lesson should no longer exist in the course
    course_after = manager.find_course_by_id(400)
    assert course_after is not None
    assert not any(l["lesson_id"] == 9001 for l in course_after.lessons)

def test_check_in_success_and_failure(fresh_manager):
    # ARRANGE
    manager = fresh_manager
    # create student and course, enroll student and add lesson
    student = StudentUser(user_id=5, name="Checkin Student", enrolled_course_ids=[])
    manager.students.append(student)
    course = Course(course_id=500, name="Checkin Course", instrument="Piano", teacher_id=None,
                    enrolled_student_ids=[5],
                    lessons=[{"lesson_id": 777, "course_name": "Checkin Course", "day": "Tuesday", "start_time": "10:00", "room": "R3"}])
    manager.courses.append(course)
    manager._save_data()

    # ACT 1: successful check-in
    ok = manager.check_in(student_id=5, course_id=500, lesson_id=777)

    # ASSERT 1
    assert ok is True
    assert any((getattr(a, "student_id", None) == 5 and getattr(a, "lesson_id", None) == 777) for a in manager.attendance)

    # ACT 2: attempt to check-in a non-enrolled student
    bad = manager.check_in(student_id=9999, course_id=500, lesson_id=777)

    # ASSERT 2
    assert bad is False
