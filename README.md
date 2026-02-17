### Karatu Exam Capstone Project ###

This is a fastapi application for a course enrollment system

```
uvicorn app.main:app --reload
```

For testing 
```
pytest app/tests/test_main.py
pytest app/tests/test_users.py
pytest app/tests/test_courses.py
pytest app/tests/test_enrollments.py

```

Entities
- Courses - id, title, course code
- Enrollments - id, user_id, course_id
