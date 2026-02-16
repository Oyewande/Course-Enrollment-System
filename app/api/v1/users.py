from fastapi import APIRouter
from app.services.users import UserService
from app.schemas.users import UserCreate   

user_router = APIRouter()

@user_router.post("/")
def create_user(user_data: UserCreate):
    return UserService.create_user(user_data)

@user_router.get("/")
def get_users():
    return UserService.get_users()
    

@user_router.get("/{user_id}")
def get_user_by_id(user_id: int):
    user = UserService.get_user(user_id)
    if user:
        return user
    return {"error": "User not found."} 
