from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    user_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    submitted_by = Column(String, nullable=False)
    updated_by = Column(String, nullable=False)

    
    def set_password(self, plain_password: str):
        self.hashed_password = pwd_context.hash(plain_password)

    
    def verify_password(self, plain_password: str):
        return pwd_context.verify(plain_password, self.hashed_password)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    student_class = Column(String, nullable=False)
    submitted_by = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    department = relationship("Department", back_populates="students")
    attendance_logs = relationship("AttendanceLog", back_populates="student")

class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    present = Column(Boolean, nullable=False)
    submitted_by = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("Student", back_populates="attendance_logs")
    course = relationship("Course", back_populates="attendance_logs")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    semester = Column(Integer, nullable=False)
    course_class = Column(String, nullable=False)
    lecture_hours = Column(Integer, nullable=False)
    submitted_by = Column(String, nullable=False)
    updated_by = Column(String, nullable=False)

    department = relationship("Department", back_populates="courses")
    attendance_logs = relationship("AttendanceLog", back_populates="course")


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String, nullable=False)
    submitted_by = Column(String, nullable=False)
    updated_by = Column(String, nullable=False)

    students = relationship("Student", back_populates="department")
    courses = relationship("Course", back_populates="department")
