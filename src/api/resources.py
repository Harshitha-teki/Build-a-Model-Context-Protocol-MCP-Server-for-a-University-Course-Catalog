from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.db.models import Course, Department

router = APIRouter()

@router.get("/resources/course_descriptions")
def get_course_descriptions(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    descriptions = "\n".join([f"[{course.course_code}] {course.title}: {course.description}" for course in courses])
    return descriptions


@router.get("/resources/department_directory")
def get_department_directory(db: Session = Depends(get_db)):
    departments = db.query(Department).all()
    directory = "\n".join([f"{dept.name} ({dept.code})" for dept in departments])
    return directory