from pydantic import BaseModel
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"
    
class UserBase(BaseModel):
    name: str
    email: str
    role: UserRole
    
class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    
