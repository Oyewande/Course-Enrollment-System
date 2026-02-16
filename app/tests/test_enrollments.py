from app.tests.test_main import client, reset_db, seed_student, seed_admin, seed_course


def setup_function():
    reset_db()


def test_student_can_enroll():
    seed_student()
    seed_course()
    response = client.post("/enrollments?user_id=1", json={"user_id": 1, "course_id": "MTH101"})
    assert response.status_code == 200
    assert response.json()["enrollment"]["course_id"] == "MTH101"


def test_admin_cannot_enroll():
    seed_admin()
    seed_course()
    response = client.post("/enrollments?user_id=2", json={"user_id": 2, "course_id": "MTH101"})
    assert response.status_code == 403


def test_duplicate_enrollment():
    seed_student()
    seed_course()
    client.post("/enrollments?user_id=1", json={"user_id": 1, "course_id": "MTH101"})
    response = client.post("/enrollments?user_id=1", json={"user_id": 1, "course_id": "MTH101"})
    assert response.status_code == 400


def test_admin_views_all_enrollments():
    seed_student()
    seed_admin()
    seed_course()
    client.post("/enrollments?user_id=1", json={"user_id": 1, "course_id": "MTH101"})
    response = client.get("/enrollments?user_id=2")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_student_cannot_view_all_enrollments():
    seed_student()
    response = client.get("/enrollments?user_id=1")
    assert response.status_code == 403


def test_student_views_own_enrollments():
    seed_student()
    seed_course()
    client.post("/enrollments?user_id=1", json={"user_id": 1, "course_id": "MTH101"})
    response = client.get("/enrollments/student/1?user_id=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_student_cannot_view_other_enrollments():
    seed_student()
    response = client.get("/enrollments/student/999?user_id=1")
    assert response.status_code == 403


def test_admin_views_course_enrollments():
    seed_student()
    seed_admin()
    seed_course()
    client.post("/enrollments?user_id=1", json={"user_id": 1, "course_id": "MTH101"})
    response = client.get("/enrollments/course/MTH101?user_id=2")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_student_cannot_view_course_enrollments():
    seed_student()
    seed_course()
    response = client.get("/enrollments/course/MTH101?user_id=1")
    assert response.status_code == 403


def test_student_deregisters():
    seed_student()
    seed_course()
    client.post("/enrollments?user_id=1", json={"user_id": 1, "course_id": "MTH101"})
    response = client.delete("/enrollments/deregister/1/MTH101?user_id=1")
    assert response.status_code == 200


def test_student_cannot_deregister_other():
    seed_student()
    seed_course()
    response = client.delete("/enrollments/deregister/999/MTH101?user_id=1")
    assert response.status_code == 403


def test_admin_force_deregisters():
    seed_student()
    seed_admin()
    seed_course()
    client.post("/enrollments?user_id=1", json={"user_id": 1, "course_id": "MTH101"})
    response = client.delete("/enrollments/force-deregister/1/MTH101?user_id=2")
    assert response.status_code == 200


def test_student_cannot_force_deregister():
    seed_student()
    seed_course()
    response = client.delete("/enrollments/force-deregister/1/MTH101?user_id=1")
    assert response.status_code == 403
