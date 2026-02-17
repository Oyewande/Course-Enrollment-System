from fastapi import APIRouter, Depends
from app.services.enrollments import EnrollmentService, EnrollmentCreate
from app.api.dependency import is_user_student, is_user_admin
from fastapi.exceptions import HTTPException

enrollment_router = APIRouter()

@enrollment_router.post("/")
def create_enrollment(
    enrollment_data: EnrollmentCreate, 
    current_user: dict = Depends(is_user_student) 
):
    return EnrollmentService.create_enrollment(enrollment_data, current_user["id"])

@enrollment_router.get("/student/{student_id}")
def get_enrollments_by_student(
    student_id: int, 
    current_user: dict = Depends(is_user_student) 
):
    if current_user["id"] != student_id:
        raise HTTPException(status_code=403, detail="You can only view your own enrollments.")
    return EnrollmentService.get_enrollments_by_student(student_id, current_user["id"])

@enrollment_router.get("/")
def get_all_enrollments(current_user: dict = Depends(is_user_admin)): 
    return EnrollmentService.get_enrollments(current_user["id"])

@enrollment_router.get("/course/{course_id}")
def get_enrollments_by_course(
    course_id: int, 
    current_user: dict = Depends(is_user_admin) 
):
    return EnrollmentService.get_enrollments_by_course(course_id, current_user["id"])

@enrollment_router.delete("/deregister/{student_id}/{course_id}")
def deregister_student(
    student_id: int, 
    course_id: int, 
    current_user: dict = Depends(is_user_student) 
):
    if current_user["id"] != student_id:
        raise HTTPException(status_code=403, detail="You can only deregister yourself.")
    return EnrollmentService.deregister_student_from_course(student_id, course_id, current_user["id"])

@enrollment_router.delete("/force-deregister/{student_id}/{course_id}")
def force_deregister_student(
    student_id: int, 
    course_id: int, 
    current_user: dict = Depends(is_user_admin)  
):
    return EnrollmentService.force_deregister_student(student_id, course_id, current_user["id"])