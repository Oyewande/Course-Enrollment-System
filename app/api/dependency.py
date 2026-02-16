from fastapi import Depends, HTTPException
from app.core.db import users

def get_current_user(user_id: int):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

def is_user_student(current_user: dict = Depends(get_current_user)):
    """
    Dependency to check if the current user is a student.
    """
    if current_user.get("role") != "student":
        raise HTTPException(status_code=403, detail="Not authorized as a student.")
    return current_user

def is_user_admin(current_user: dict = Depends(get_current_user)):
    """
    Dependency to check if the current user is an admin.
    """
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized as an admin.")
    return current_user