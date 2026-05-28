from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.db.models import Course, Instructor, Prerequisite
from src.db.session import get_db

router = APIRouter()

class SearchCoursesInput(BaseModel):
    query: str
    department_code: str = None

class SearchCoursesOutput(BaseModel):
    course_code: str
    title: str
    credits: int

class GetPrerequisitesInput(BaseModel):
    course_code: str

class GetPrerequisitesOutput(BaseModel):
    course_code: str
    prerequisites: list

class LookupInstructorInput(BaseModel):
    instructor_name: str

class LookupInstructorOutput(BaseModel):
    name: str
    email: str
    department_name: str

class GetPrerequisiteGraphInput(BaseModel):
    course_code: str

class GetPrerequisiteGraphOutput(BaseModel):
    nodes: list
    edges: list

@router.post("/search_courses", response_model=list[SearchCoursesOutput])
def search_courses(input: SearchCoursesInput, db: Session = next(get_db())):
    query = input.query.lower()
    department_code = input.department_code
    courses = db.query(Course).filter(Course.title.ilike(f"%{query}%"))
    if department_code:
        courses = courses.filter(Course.department_id == department_code)
    return [{"course_code": course.course_code, "title": course.title, "credits": course.credits} for course in courses.all()]

@router.post("/get_prerequisites", response_model=GetPrerequisitesOutput)
def get_prerequisites(input: GetPrerequisitesInput, db: Session = next(get_db())):
    course = db.query(Course).filter(Course.course_code == input.course_code).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    prerequisites = db.query(Prerequisite).filter(Prerequisite.course_id == course.id).all()
    return {
        "course_code": course.course_code,
        "prerequisites": [{"course_code": p.prerequisite.course_code, "title": p.prerequisite.title} for p in prerequisites]
    }

@router.post("/lookup_instructor", response_model=LookupInstructorOutput)
def lookup_instructor(input: LookupInstructorInput, db: Session = next(get_db())):
    instructor = db.query(Instructor).filter(Instructor.name == input.instructor_name).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return {
        "name": instructor.name,
        "email": instructor.email,
        "department_name": instructor.department.name
    }

@router.post("/get_prerequisite_graph", response_model=GetPrerequisiteGraphOutput)
def get_prerequisite_graph(input: GetPrerequisiteGraphInput, db: Session = next(get_db())):
    # Logic to construct the prerequisite graph using NetworkX would go here
    pass