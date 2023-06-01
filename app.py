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


@app.get('/')
def index():
    return {'Data': 'Welcome to API!'}


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
        return {'error': 'Not found...'}


@app.get('/get-by-name')
def get_student(*, name: Optional[str] = None):
    # Optional[X] == X | None
    # api/get-by-name?name=kaua
    # * => All parameters must be passed by key and value (?param=value)
    for student_id in students:
        if students[student_id]['name'] == name:
            return students[student_id]

    return {'error': 'Not found...'}


@app.get('/get-by-number/{name}')
def get_student(*, name: Optional[str], student_number: int):
    # api/get-by-number/kaua?student_number=22
    for student_id in students:
        if students[student_id]['name'] == name and students[student_id]['number'] == student_number:
            return students[student_id]


@app.post('/create-student/{student_id}')
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {'error': 'Student exists...'}

    students[student_id] = student.dict()
    return students[student_id]


if __name__ == '__main__':
    uvicorn.run('app:app', host=HOST, port=PORT, reload=True)
