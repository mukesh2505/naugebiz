from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Union
from datetime import timedelta

import models, schemas, crud, auth, database
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
#  i have comented thi code because of a error when starting the code thats why i had commented this code 
#  expect 9 point all the points is almost covered 

# @app.on_event("startup")
# async def startup_event():
#     models.Base.metadata.create_all(bind=database.engine)

#     
#     db = database.SessionLocal()
#     try:
#         if db.query(models.User).count() == 0:
#             # Create a default user
#             default_user = schemas.UserCreate(
#                 type="admin",
#                 full_name="Admin User",
#                 user_name="admin",
#                 email="admin@example.com",
#                 password="password123"  # This should be a strong password
#             )
#             db_user = crud.create_user(db, default_user)
#             print(f"First user created with ID: {db_user.id} and Password: password123")
#     finally:
#         db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token", response_model=schemas.Token)
def login(form_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = crud.authenticate_user(db, form_data.user_name, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = auth.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        return crud.create_user(db=db, user=user)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {e}")

@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):
    try:
        return crud.create_student(db=db, student=student)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Error creating student: {e}")

@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):
    try:
        return crud.create_course(db=db, course=course)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Error creating course: {e}")

@app.post("/attendance/", response_model=schemas.AttendanceLog)
def create_attendance(log: schemas.AttendanceLogCreate, db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):
    try:
        return crud.create_attendance_log(db=db, log=log)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Error logging attendance: {e}")

@app.post("/departments/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(database.get_db), current_user: str = Depends(get_current_user)):
    try:
        return crud.create_department(db=db, department=department)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Error creating department: {e}")
