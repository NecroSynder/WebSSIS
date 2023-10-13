# students.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.models_students import Students


students = Blueprint('students', __name__, template_folder='templates')

@students.route("/students/")
def students_page():
    students_data = Students.get_all()
    return render_template("students.html", students=students_data)

@students.route("/students/add", methods=["POST"])
def add_student():
    id = request.form["id"]
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    college = request.form["college"]
    course_code = request.form["courseCode"]
    year_level = request.form["yearLevel"]
    gender = request.form["gender"]

    Students.add(id, first_name, last_name, college, course_code, year_level, gender)
    return redirect(url_for("students.students_page"))

@students.route("/students/edit/<id>", methods=["GET", "POST"])
def edit_student(id):
    if request.method == "POST":
        first_name = request.form["firstName"]
        last_name = request.form["lastName"]
        college = request.form["college"]
        course_code = request.form["courseCode"]
        year_level = request.form["yearLevel"]
        gender = request.form["gender"]

        Students.update(id, first_name, last_name, college, course_code, year_level, gender)
        return redirect(url_for("students.students_page"))
    else:
        student_data = Students.get_by_id(id)
        return render_template("edit_student.html", student=student_data)

@students.route("/students/delete/<id>", methods=["POST"])
def delete_student(id):
    Students.delete(id)
    return redirect(url_for("students.students_page"))
