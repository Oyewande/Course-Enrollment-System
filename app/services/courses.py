from fastapi import Depends, HTTPException
from typing import List, Dict
from app.schemas.courses import CourseCreate, CourseUpdate
from app.core.db import courses 
from app.api.dependency import is_user_admin


class CourseService:
    @staticmethod
    def create_course(course_create: CourseCreate, current_user: int = Depends(is_user_admin)):
        """
        Create a new course with validation.
        """
        if not course_create.title or not course_create.course_code:
            raise HTTPException(status_code=400, detail="Course title and course code are required.")
        
        course_id = len(courses) + 1
        course = {
            "id": course_id,
            "title": course_create.title,
            "course_code": course_create.course_code
        }
            
        courses[course_id] = course
        return course

    @staticmethod
    def get_courses():
        return list(courses.values())

    @staticmethod
    def get_course(course_id: int):
        """
        Retrieve a specific course by ID with validation.
        """
        if course_id not in courses:
            raise HTTPException(status_code=404, detail="Course not found.")
        return courses.get(course_id)
    
    @staticmethod
    def update_course(course_id: int, course_update: CourseUpdate, current_user: int = Depends(is_user_admin)):
        """
        Update a course with validation.
        """
        if course_id not in courses:
            raise HTTPException(status_code=404, detail="Course not found.")
        
        if not course_update.title or not course_update.course_code:
            raise HTTPException(status_code=400, detail="Course title and course code are required.")
        
        courses[course_id] = {
            "id": course_id,
            "title": course_update.title,
            "course_code": course_update.course_code
        }
        return courses[course_id]

    @staticmethod
    def delete_course(course_id: int, current_user: int = Depends(is_user_admin)):
        """
        Delete a course with validation.
        """
        if course_id not in courses:
            raise HTTPException(status_code=404, detail="Course does not exist.")
        
        del courses[course_id]
        return {"message": "Course deleted successfully"}
