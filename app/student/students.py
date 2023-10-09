
# students.py
from flask import Blueprint, render_template, request

students = Blueprint('students', __name__, template_folder='templates')

@students.route("/students/")
def students_page():
    students = [
        {
            "id": "2019-2093",
            "first_name": "John",
            "last_name": "Doe",
            "course_code": "BSCS",
            "college_code": "CCS",
            "year_level": 4,
            "gender": "Male"
        },
        {
            "id": "2019-2094",
            "first_name": "Jane",
            "last_name": "Doe",
            "course_code": "BSCS",
            "college_code": "CCS",
            "year_level": 4,
            "gender": "Female"
        }
    ]
    return render_template("students.html", students=students)

