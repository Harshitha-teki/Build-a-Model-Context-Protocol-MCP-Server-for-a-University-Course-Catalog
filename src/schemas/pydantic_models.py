from pydantic import BaseModel
from typing import List, Optional

class CourseSearchRequest(BaseModel):
    query: str
    department_code: Optional[str] = None

class CourseSearchResponse(BaseModel):
    course_code: str
    title: str
    credits: int

class GetPrerequisitesRequest(BaseModel):
    course_code: str

class GetPrerequisitesResponse(BaseModel):
    course_code: str
    prerequisites: List[CourseSearchResponse]

class LookupInstructorRequest(BaseModel):
    instructor_name: str

class LookupInstructorResponse(BaseModel):
    name: str
    email: str
    department_name: str

class GetPrerequisiteGraphRequest(BaseModel):
    course_code: str

class PrerequisiteGraphResponse(BaseModel):
    nodes: List[dict]
    edges: List[dict]