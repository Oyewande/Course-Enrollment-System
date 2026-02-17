from pydantic import BaseModel


class CourseBase(BaseModel):
    title: str
    course_code: str
    
class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    
class CourseUpdate(CourseBase):
    pass

class CourseDelete(BaseModel):
    id: int