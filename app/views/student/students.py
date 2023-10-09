
# students.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.models_students import Students
# from app.models.models_course import models_course

students = Blueprint('students', __name__, template_folder='templates')

@students.route("/students/")
def students_page():
    students = Students.all()
    return render_template("students.html", students=students)

@students.route("/students/add", methods=['POST'])
def add_student():
    # get data from form
    id = request.form['id']
    firstname = request.form['firstName']
    lastname = request.form['lastName']
    coursecode = request.form['courseCode']
    year = request.form['yearLevel']
    gender = request.form['gender']

    # create a new student
    new_student = Students(id=id, firstname=firstname, lastname=lastname, coursecode=coursecode, year=year, gender=gender)
    
    # add the new student to the database
    new_student.add()

    # redirect to the students page
    return redirect(url_for('students.students_page'))

@students.route("/students/edit", methods=['POST'])
def edit_student():
    # get data from form
    id = request.form['id']
    firstname = request.form['firstName']
    lastname = request.form['lastName']
    coursecode = request.form['courseCode']
    year = request.form['yearLevel']
    gender = request.form['gender']

    # update the student in the database
    Students.update(id, firstname, lastname, coursecode, year, gender)

    # redirect to the students page
    return redirect(url_for('students.students_page'))

