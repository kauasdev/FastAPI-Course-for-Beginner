from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
import uvicorn


HOST = '0.0.0.0'
PORT = 2929

app = FastAPI()
# API/docs -> API Documentation

students = {
    1: {
        'name': 'kaua',
        'age': 16,
        'number': 22,
        'year': 'Year 12'
    }
}


class Student(BaseModel):
    name: str
    age: int
    number: int
    year: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None
    number: Optional[int] = None


@app.get('/')
def index():
    return {'Data': 'Welcome to API!'}


@app.get('/student-list')
def student_list():
    return students


@app.get('/get-student/{student_id}')
def get_student(
        student_id: int = Path(description='The ID of the student you want to view', gt=0, lt=3)
        # gt => greater than
        # lt => less than
):
    # api/get-student/1
    try:
        return students[student_id]
    except KeyError:
        return {'Error': 'Not found...'}


@app.get('/get-by-name')
def get_student(*, name: Optional[str] = None):
    # Optional[X] == X | None
    # api/get-by-name?name=kaua
    # * => All parameters must be passed by key and value (?param=value)
    for student_id in students:
        if students[student_id]['name'] == name:
            return students[student_id]

    return {'Error': 'Not found...'}


@app.get('/get-by-number/{name}')
def get_student(*, name: Optional[str], student_number: int):
    # api/get-by-number/kaua?student_number=22
    for student_id in students:
        if students[student_id]['name'] == name and students[student_id]['number'] == student_number:
            return students[student_id]


@app.post('/create-student/{student_id}')
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {'Error': 'Student exists...'}

    students[student_id] = student.dict()
    return students[student_id]


@app.put('/update-student/{student_id}')
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {'Error': 'Student does not exist...'}
    students[student_id] = student.dict()

    for key, value in student:
        if student.dict()[key] is not None:
            students[student_id][key] = value

    return students[student_id]


@app.patch('/update-student/{student_id}')
def update_user(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {'Error': 'Student does not exist...'}

    old_student_data = students[student_id].copy()
    update_student_data = student.dict(exclude_unset=True)
    old_student_data.update(update_student_data)

    student = old_student_data.copy()

    students[student_id] = student

    return students[student_id]


@app.delete('/delete-student/{student_id}')
def delete_student(student_id: int):
    if student_id not in students:
        return {'Error': 'Student does not exist'}

    del students[student_id]
    return {'Message': 'Student deleted successfully'}


if __name__ == '__main__':
    uvicorn.run('app:app', host=HOST, port=PORT, reload=True)
