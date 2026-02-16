from app.tests.test_main import client, student_data, admin_data, reset_db


def setup_function():
    reset_db()


def test_create_student():
    response = client.post("/users", json=student_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["role"] == "student"
    assert "id" in data


def test_create_admin():
    response = client.post("/users", json=admin_data)
    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_missing_fields():
    response = client.post("/users", json={"name": "Incomplete"})
    assert response.status_code == 422


def test_invalid_role():
    response = client.post("/users", json={"name": "Bad", "email": "x@x.com", "role": "superuser"})
    assert response.status_code == 422


def test_get_users_empty():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_get_users():
    client.post("/users", json=student_data)
    client.post("/users", json=admin_data)
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_user_by_id():
    resp = client.post("/users", json=student_data)
    user_id = resp.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
