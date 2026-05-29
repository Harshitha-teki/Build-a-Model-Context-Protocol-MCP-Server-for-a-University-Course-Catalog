from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.db.models import Course, Instructor, Prerequisite
from src.db.session import get_db
from src.utils.graph import create_prerequisite_graph, export_graph_to_json
import networkx as nx

router = APIRouter()

# Minimal MCP-style metadata for discovery by the server
TOOLS = [
    {
        "name": "search_courses",
        "description": "Searches the university course catalog for courses matching a query string. Optional department_code filters results.",
        "input_schema": {"query": "string", "department_code": "string (optional)"},
        "output_schema": [{"course_code": "string", "title": "string", "credits": "integer"}]
    },
    {
        "name": "get_prerequisites",
        "description": "Returns direct prerequisites for a course_code.",
        "input_schema": {"course_code": "string"},
        "output_schema": {"course_code": "string", "prerequisites": [{"course_code": "string", "title": "string"}]}
    },
    {
        "name": "lookup_instructor",
        "description": "Find an instructor's details by name.",
        "input_schema": {"instructor_name": "string"},
        "output_schema": {"name": "string", "email": "string", "department_name": "string"}
    },
    {
        "name": "get_prerequisite_graph",
        "description": "Returns the full prerequisite dependency graph (adjacency list) for a course_code.",
        "input_schema": {"course_code": "string"},
        "output_schema": {"nodes": [{"id": "string"}], "edges": [{"source": "string", "target": "string"}]}
    }
]

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
def search_courses(input: SearchCoursesInput, db: Session = Depends(get_db)):
    query = input.query.lower()
    department_code = input.department_code
    courses = db.query(Course).filter(Course.title.ilike(f"%{query}%"))
    if department_code:
        courses = courses.filter(Course.department_id == department_code)
    return [{"course_code": course.course_code, "title": course.title, "credits": course.credits} for course in courses.all()]

@router.post("/get_prerequisites", response_model=GetPrerequisitesOutput)
def get_prerequisites(input: GetPrerequisitesInput, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_code == input.course_code).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    prerequisites = db.query(Prerequisite).filter(Prerequisite.course_id == course.id).all()
    return {
        "course_code": course.course_code,
        "prerequisites": [{"course_code": p.prerequisite.course_code, "title": p.prerequisite.title} for p in prerequisites]
    }

@router.post("/lookup_instructor", response_model=LookupInstructorOutput)
def lookup_instructor(input: LookupInstructorInput, db: Session = Depends(get_db)):
    instructor = db.query(Instructor).filter(Instructor.name == input.instructor_name).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return {
        "name": instructor.name,
        "email": instructor.email,
        "department_name": instructor.department.name
    }

@router.post("/get_prerequisite_graph", response_model=GetPrerequisiteGraphOutput)
def get_prerequisite_graph(input: GetPrerequisiteGraphInput, db: Session = Depends(get_db)):
    # Build a directed graph of prerequisites and return adjacency list
    # Fetch all courses and prerequisites
    courses = db.query(Course).all()
    prereqs = db.query(Prerequisite).all()

    # Prepare simple dict lists for graph builder
    course_list = [{"course_code": c.course_code, "title": c.title} for c in courses]
    prereq_list = []
    for p in prereqs:
        # Each Prerequisite links course_id -> prerequisite_id
        # resolve course codes
        course = db.query(Course).filter(Course.id == p.course_id).first()
        prereq_course = db.query(Course).filter(Course.id == p.prerequisite_id).first()
        if course and prereq_course:
            prereq_list.append({"course_code": course.course_code, "prerequisite_code": prereq_course.course_code})

    graph = create_prerequisite_graph(course_list, prereq_list)

    # If requested course not in graph, return empty structure with error
    if input.course_code not in graph:
        raise HTTPException(status_code=404, detail="Course not found")

    exported = export_graph_to_json(graph)
    return exported