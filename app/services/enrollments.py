from fastapi import Depends, HTTPException
from pydantic import BaseModel, Field
from app.api.dependency import is_user_student, is_user_admin
from app.core.db import enrollments, courses, users

class EnrollmentCreate(BaseModel):
    user_id: int 
    course_id: str 

class EnrollmentService:
    @staticmethod
    def create_enrollment(enrollment_data: EnrollmentCreate, current_user: int):
        """
        Enroll a student in a course with validation.
        Only students can enroll themselves in courses.
        """
        if enrollment_data.user_id not in users:
            raise HTTPException(status_code=404, detail="Student does not exist.")
        
        if enrollment_data.course_id not in courses:
            raise HTTPException(status_code=404, detail="Course does not exist.")
        
        for enrollment in enrollments.values():
            if enrollment["user_id"] == enrollment_data.user_id and enrollment["course_id"] == enrollment_data.course_id:
                raise HTTPException(status_code=400, detail="Student is already enrolled in this course.")
        
        enrollment_id = len(enrollments) + 1
        enrollment = {
            "id": enrollment_id,
            "user_id": enrollment_data.user_id,
            "course_id": enrollment_data.course_id
        }
        enrollments[enrollment_id] = enrollment
        return {"message": "Student successfully enrolled in the course.", "enrollment": enrollment}

    @staticmethod
    def deregister_student_from_course(user_id: int, course_id: str, current_user: int):
        """
        Deregister a student from a specific course with validation.
        Only students can deregister themselves.
        """
        if user_id not in users:
            raise HTTPException(status_code=404, detail="Student does not exist.")
        
        if course_id not in courses:
            raise HTTPException(status_code=404, detail="Course does not exist.")
        
        for enrollment_id, enrollment in list(enrollments.items()):
            if enrollment["user_id"] == user_id and enrollment["course_id"] == course_id:
                del enrollments[enrollment_id]
                return {"message": "Student successfully deregistered from the course."}
        
        raise HTTPException(status_code=404, detail="Enrollment not found for the specified student and course.")

    @staticmethod
    def get_enrollments_by_student(user_id: int, current_user: int):
        """
        Retrieve all enrollments for a specific student with validation.
        Only students can view their own enrollments.
        """
        if user_id not in users:
            raise HTTPException(status_code=404, detail="Student does not exist.")
        
        student_enrollments = [
            enrollment for enrollment in enrollments.values()
            if enrollment["user_id"] == user_id
        ]
        if not student_enrollments:
            raise HTTPException(status_code=404, detail="No enrollments found for the specified student.")
        return student_enrollments

    @staticmethod
    def get_enrollments(current_user: int):
        """
        Retrieve all enrollments.
        Only admins can access this route.
        """
        return list(enrollments.values())

    @staticmethod
    def get_enrollments_by_course(course_id: str, current_user: int):
        """
        Retrieve all enrollments for a specific course with validation.
        Only admins can access this route.
        """
        if course_id not in courses:
            raise HTTPException(status_code=404, detail="Course does not exist.")
        
        course_enrollments = [
            enrollment for enrollment in enrollments.values()
            if enrollment["course_id"] == course_id
        ]
        if not course_enrollments:
            raise HTTPException(status_code=404, detail="No enrollments found for the specified course.")
        return course_enrollments

    @staticmethod
    def force_deregister_student(user_id: int, course_id: str, current_user: int):
        """
        Force deregister a student from a specific course with validation.
        Only admins can perform this action.
        """
        if user_id not in users:
            raise HTTPException(status_code=404, detail="User does not exist.")
        
        if course_id not in courses:
            raise HTTPException(status_code=404, detail="Course does not exist.")
        
        for enrollment_id, enrollment in list(enrollments.items()):
            if enrollment["user_id"] == user_id and enrollment["course_id"] == course_id:
                del enrollments[enrollment_id]
                return {"message": "Student successfully deregistered from the course by admin."}
        
        raise HTTPException(status_code=404, detail="Enrollment not found for the specified student and course.")