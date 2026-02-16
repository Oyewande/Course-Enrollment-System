from fastapi import HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict
from app.core.db import users
from app.schemas.users import UserRole 

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    role: UserRole

# class UserUpdate(BaseModel):
#     name: str = Field(None, min_length=1, max_length=100)
#     email: EmailStr = None
#     age: int = Field(None, gt=0, description="Age must be a positive integer.")

class UserService:
    @staticmethod
    def create_user(user_data: UserCreate):
        """
        Create a new user with validation.
        """
        user_id = len(users) + 1
        user = {
            "id": user_id,
            "name": user_data.name,
            "email": user_data.email,
            "role": user_data.role
        }
        users[user_id] = user
        return user

    @staticmethod
    def get_users():
        """
        Retrieve all users.
        """
        return list(users.values())

    @staticmethod
    def get_user(user_id: int):
        """
        Retrieve a specific user by ID with validation.
        """
        if user_id not in users:
            raise HTTPException(status_code=404, detail="User not found.")
        return users[user_id]
    