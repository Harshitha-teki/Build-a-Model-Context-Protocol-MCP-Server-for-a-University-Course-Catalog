from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .session import Base

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)

    instructors = relationship("Instructor", back_populates="department")
    courses = relationship("Course", back_populates="department")

class Instructor(Base):
    __tablename__ = 'instructors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    office = Column(String)
    department_id = Column(Integer, ForeignKey('departments.id'))

    department = relationship("Department", back_populates="instructors")
    courses = relationship("Course", back_populates="instructor")

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    credits = Column(Integer)
    instructor_id = Column(Integer, ForeignKey('instructors.id'))
    department_id = Column(Integer, ForeignKey('departments.id'))

    instructor = relationship("Instructor", back_populates="courses")
    department = relationship("Department", back_populates="courses")
    prerequisites = relationship("Prerequisite", back_populates="course")

class Prerequisite(Base):
    __tablename__ = 'prerequisites'

    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)
    prerequisite_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)

    course = relationship("Course", back_populates="prerequisites")