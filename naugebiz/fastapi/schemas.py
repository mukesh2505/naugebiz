from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class UserBase(BaseModel):
    type: str
    full_name: str
    user_name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    submitted_by: str
    updated_by: str

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    full_name: str
    department_id: int
    student_class: str

class StudentCreate(StudentBase):
    submitted_by: str

class Student(StudentBase):
    id: int
    updated_at: datetime

    class Config:
        orm_mode = True

class AttendanceLogBase(BaseModel):
    student_id: int
    course_id: int
    present: bool

class AttendanceLogCreate(AttendanceLogBase):
    submitted_by: str

class AttendanceLog(AttendanceLogBase):
    id: int
    updated_at: datetime

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    course_name: str
    department_id: int
    semester: int
    course_class: str
    lecture_hours: int

class CourseCreate(CourseBase):
    submitted_by: str

class Course(CourseBase):
    id: int
    updated_by: str

    class Config:
        orm_mode = True

class DepartmentBase(BaseModel):
    department_name: str

class DepartmentCreate(DepartmentBase):
    submitted_by: str

class Department(DepartmentBase):
    id: int
    updated_by: str

    class Config:
        orm_mode = True
