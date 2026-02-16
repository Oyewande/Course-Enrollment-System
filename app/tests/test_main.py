from fastapi.testclient import TestClient
from app.main import app
from app.core import db

client = TestClient(app)

student_data = {"name": "Alice", "email": "alice@example.com", "role": "student"}
admin_data = {"name": "Bob", "email": "bob@example.com", "role": "admin"}
course_data = {"title": "Introduction to Python", "course_code": "CS101"}


def reset_db():
    db.users.clear()
    db.courses.clear()
    db.enrollments.clear()


def seed_student():
    db.users[1] = {"id": 1, "name": "Alice", "role": "student"}


def seed_admin():
    db.users[2] = {"id": 2, "name": "Bob", "role": "admin"}


def seed_course():
    db.courses["MTH101"] = {"title": "Math 101", "course_code": "MTH101"}


def test_app_starts():
    response = client.get("/users")
    assert response.status_code == 200