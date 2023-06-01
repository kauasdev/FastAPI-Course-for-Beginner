from fastapi import FastAPI, Path
import uvicorn


HOST = '0.0.0.0'
PORT = 2929

app = FastAPI()
# API/docs -> API Documentation

students = {
    1: {
        'name': 'kaua',
        'age': 16,
        'class': 'Year 12'
    }
}


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


if __name__ == '__main__':
    uvicorn.run('app:app', host=HOST, port=PORT, reload=True)
