from pydantic import BaseModel

class EnrollmentBase(BaseModel):
    user_id: int
    course_id: str
    
class EnrollmentCreate(EnrollmentBase):
    pass    

class Enrollment(EnrollmentBase):
    id: int