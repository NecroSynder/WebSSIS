
# students.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.models_students import Students
from app.models.models_courses import Courses


students = Blueprint('students', __name__, template_folder='templates')

@students.route("/students/")
def students_page():
    students_data = Students.get_all()
    courses_data = Courses.get_all()  # Fetch the college codes
    return render_template("students.html", students=students_data, courses=courses_data)


@students.route('/add', methods=['POST'])
def add_student():
    # Get form data
    id = request.form.get('id')
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    course_code = request.form.get('courseCode')
    year_level = request.form.get('yearLevel')
    gender = request.form.get('gender')
    
    # Check if the student already exists
    existing_student = Students.get_by_id(id)
    if existing_student:
        return jsonify({'success': False, 'message': 'A student with this ID already exists.'})

    # Call the add() method from the Students model
    try:
        Students.add(id, first_name, last_name, course_code, year_level, gender)
        return jsonify({'success': True})
    except:
        return jsonify({'success': False, 'message': 'Error adding student'})

@students.route('/students/delete/<id>', methods=['POST'])
def delete_student(id):
    try:
        # Call the delete() method from the Students model
        Students.delete(id)
        return jsonify({'success': True})
    except:
        return jsonify({'success': False, 'message': 'Error deleting student'})

@students.route("/edit", methods=["POST"])
def edit_student():
    print("Edit route hit")  # Print statement to check if route is hit
    print(request.form)  # Print the request.form data
    new_id = request.form["id"]
    old_id = request.form["old_id"]
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    course_code = request.form["courseCode"]
    year_level = request.form["yearLevel"]
    gender = request.form["gender"]
    if Students.update(old_id, new_id, first_name, last_name, course_code, year_level, gender):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Error updating student'})




