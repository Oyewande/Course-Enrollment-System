from app.tests.test_main import client, course_data, reset_db


def setup_function():
    reset_db()


def test_create_course():
    response = client.post("/courses", json=course_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Introduction to Python"
    assert data["course_code"] == "CS101"
    assert "id" in data


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
    resp = client.post("/courses", json=course_data)
    course_id = resp.json()["id"]
    response = client.get(f"/courses/{course_id}")
    assert response.status_code == 200
    assert response.json()["id"] == course_id


def test_get_course_not_found():
    response = client.get("/courses/999")
    assert response.status_code == 404


def test_update_course():
    resp = client.post("/courses", json=course_data)
    course_id = resp.json()["id"]
    response = client.put(f"/courses/{course_id}", json={"title": "Advanced Python", "course_code": "CS102"})
    assert response.status_code == 200
    assert response.json()["title"] == "Advanced Python"


def test_update_course_not_found():
    response = client.put("/courses/999", json={"title": "X", "course_code": "X"})
    assert response.status_code == 404


def test_delete_course():
    resp = client.post("/courses", json=course_data)
    course_id = resp.json()["id"]
    response = client.request("DELETE", f"/courses/{course_id}", json={"id": course_id})
    assert response.status_code == 200
    assert client.get(f"/courses/{course_id}").status_code == 404


def test_delete_course_not_found():
    response = client.request("DELETE", "/courses/999", json={"id": 999})
    assert response.status_code == 404
