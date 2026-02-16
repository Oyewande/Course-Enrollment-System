from fastapi import APIRouter
from app.services.courses import CourseService
from app.schemas.courses import CourseCreate, CourseUpdate, CourseDelete

course_router = APIRouter()

@course_router.post("/")
def create_course(course_data: CourseCreate):
    return CourseService.create_course(course_data)

@course_router.get("/")
def get_courses():
    return CourseService.get_courses()

@course_router.get("/{course_id}")
def get_course_by_id(course_id: str):
    course = CourseService.get_course(course_id)
    if course:
        return course
    return {"error": "Course not found."}

@course_router.put("/{course_id}")
def update_course(course_id: str, course_data: CourseUpdate):
    course = CourseService.update_course(course_id, course_data)
    if course:
        return course
    return {"error": "Course not found."}

@course_router.delete("/{course_id}")
def delete_course(course_id: str, course_data: CourseDelete):
    return CourseService.delete_course(course_id, course_data)