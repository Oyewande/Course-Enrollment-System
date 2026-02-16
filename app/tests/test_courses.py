from app.tests.test_main import client, course_data, reset_db


def setup_function():
    reset_db()


def test_create_course():
    response = client.post("/courses", json=course_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Introduction to Python"
    assert data["course_code"] == "CS101"


def test_create_course_missing_title():
    response = client.post("/courses", json={"course_code": "CS101"})
    assert response.status_code == 422


def test_get_courses_empty():
    response = client.get("/courses")
    assert response.status_code == 200
    assert response.json() == []


def test_get_courses():
    client.post("/courses", json=course_data)
    client.post("/courses", json={"title": "Advanced Python", "course_code": "CS201"})
    response = client.get("/courses")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_course_by_id():
    client.post("/courses", json=course_data)
    response = client.get("/courses/CS101")
    assert response.status_code == 200
    assert response.json()["course_code"] == "CS101"


def test_get_course_not_found():
    response = client.get("/courses/NONEXIST")
    assert response.status_code == 404


def test_update_course():
    client.post("/courses", json=course_data)
    response = client.put("/courses/CS101", json={"title": "Advanced Python", "course_code": "CS101"})
    assert response.status_code == 200
    assert response.json()["title"] == "Advanced Python"


def test_update_course_not_found():
    response = client.put("/courses/NONEXIST", json={"title": "X", "course_code": "X"})
    assert response.status_code == 404


def test_delete_course():
    client.post("/courses", json=course_data)
    response = client.request("DELETE", "/courses/CS101", json={"course_code": "CS101"})
    assert response.status_code == 200
    assert client.get("/courses/CS101").status_code == 404


def test_delete_course_not_found():
    response = client.request("DELETE", "/courses/NONEXIST", json={"course_code": "NONEXIST"})
    assert response.status_code == 404
