from sqlalchemy.orm import Session
import models, schemas

# CRUD operations for each model

def create_user(db: Session, user: schemas.UserCreate):
    try:
        db_user = models.User(**user.dict())
        db_user.set_password(user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creating User: {e}")
        raise

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.user_name == username).first()
    if user and user.verify_password(password):
        return user
    return None


def create_student(db: Session, student: schemas.StudentCreate):
    try:
        db_student = models.Student(**student.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creating student: {e}")
        raise

def create_course(db: Session, course: schemas.CourseCreate):
    try:
        db_course = models.Course(**course.dict())
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creating course: {e}")
        raise

def create_attendance_log(db: Session, log: schemas.AttendanceLogCreate):
    try:
        db_log = models.AttendanceLog(**log.dict())
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creating attendence Log: {e}")
        raise



def create_department(db: Session, department: schemas.DepartmentCreate):
    try:
        db_department = models.Department(**department.dict())
        db.add(db_department)
        db.commit()
        db.refresh(db_department)
        return db_department
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creating department: {e}")
        raise
    




